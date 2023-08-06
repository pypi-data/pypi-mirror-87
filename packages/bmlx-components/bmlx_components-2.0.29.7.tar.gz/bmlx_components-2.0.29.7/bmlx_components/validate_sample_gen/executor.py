import os
import sys
import hashlib
import logging
import yaml
import collections
import tempfile
import subprocess
import gzip
import json
import shutil
from typing import Dict, Text, List, Any
from datetime import datetime, timedelta
from pytz import timezone
from enum import Enum

from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from kafka.vendor import six

from bmlx.flow import Executor, Artifact
from bmlx.utils import artifact_utils, io_utils
from bmlx_components.proto import model_pb2
from bmlx_components.validate_sample_gen import fg_main

BMLX_KAFKA_CONSUMER_GROUP = "bmlx_consumer"


class SampleGenExecutor(Executor):
    def fetch_fg(self, fg_conf_path, fg_lib_path, local_dir):
        file_content = io_utils.read_file_string(fg_conf_path)
        io_utils.write_string_file(
            os.path.join(local_dir, os.path.basename(fg_conf_path)),
            file_content,
        )

        file_content = io_utils.read_file_string(fg_lib_path)
        io_utils.write_string_file(
            os.path.join(local_dir, os.path.basename(fg_lib_path)), file_content
        )

        fg_cpp_lib_path = os.path.join(
            os.path.dirname(fg_lib_path), "libfg_operators.so"
        )
        file_content = io_utils.read_file_string(fg_cpp_lib_path)
        io_utils.write_string_file(
            os.path.join(local_dir, os.path.basename(fg_cpp_lib_path)),
            file_content,
        )

    def filter_origin_samples(
        self,
        kafka_brokers: Text,
        kafka_topic: Text,
        local_dir: Text,
        pushed_model: model_pb2.PushedModel,
        sample_count_limit: int,
    ):

        local_origin_samples_path = os.path.join(
            local_dir, "origin_samples.txt"
        )

        sys.path.insert(
            0, os.path.join(os.path.dirname(__file__), "../mlplat-protos")
        )
        from mlplat.feature.example_pb2 import SequenceExample
        from mlplat.feature.original_feature_pb2 import OriginalFeature

        def filter_by_model_info(
            origin_bytes, pushed_model: model_pb2.PushedModel
        ):
            origin_feature = OriginalFeature()
            origin_feature.ParseFromString(origin_bytes)
            if (
                origin_feature.flow_info.feature[
                    "rank_info.model_name"
                ].bytes.decode()
                != pushed_model.name
                or origin_feature.flow_info.feature[
                    "rank_info.model_version"
                ].int32
                != pushed_model.version
            ):
                return True
            return False

        with open(local_origin_samples_path, "w") as origin_sample_fp:
            samples_count = 0
            consumer = KafkaConsumer(
                kafka_topic,
                group_id=BMLX_KAFKA_CONSUMER_GROUP,
                bootstrap_servers=kafka_brokers,
                auto_offset_reset="latest",
                enable_auto_commit=True,
            )
            consumer.poll(1)
            consumer.seek_to_end()

            for msg in consumer:
                line = msg.value.decode("latin1")
                line = line[line.find("{") : line.rfind("}") + 1]
                try:
                    line = json.loads(line).get("pb_msg")
                except json.decoder.JSONDecodeError:
                    continue

                origin_bytes = fg_main.parse_featurelog_line(line)
                if not origin_bytes:
                    continue
                if filter_by_model_info(origin_bytes, pushed_model):
                    continue
                origin_sample_fp.write(line)
                origin_sample_fp.write("\n")
                samples_count += 1
                if samples_count >= sample_count_limit:
                    break
        return local_origin_samples_path

    def process_origin_samples(
        self,
        fg_dir: Text,
        local_origin_samples_path: Text,
        local_processed_samples_path: Text,
    ):
        fg_py_path = os.path.join(os.path.dirname(__file__), "fg_main.py")
        fg_proc = subprocess.Popen(
            [
                "python",
                fg_py_path,
                "--fg_dir",
                fg_dir,
                "--origin_samples_path",
                local_origin_samples_path,
                "--processed_samples_path",
                local_processed_samples_path,
            ],
        )
        fg_proc.wait()
        return fg_proc.returncode

    def upload_to_remote(self, local_path, remote_dir):
        # upload to hdfs
        if io_utils.exists(remote_dir):
            io_utils.mkdirs(remote_dir)

        fs, path = io_utils.resolve_filesystem_and_path(remote_dir)
        fs.upload(
            local_path, os.path.join(remote_dir, os.path.basename(local_path)),
        )

    def execute(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        self._log_startup(input_dict, output_dict, exec_properties)

        assert len(input_dict["pushed_model"]) == 1
        model_meta_uri = input_dict["pushed_model"][0].meta.uri
        assert io_utils.exists(model_meta_uri)
        assert len(input_dict["fg_py_lib"]) == 1

        pushed_model = io_utils.parse_pbtxt_file(
            model_meta_uri, model_pb2.PushedModel()
        )

        sample_count_limit = exec_properties["output_sample_limit"]

        assert len(output_dict["samples"]) == 1
        assert len(output_dict["origin_samples"]) == 1
        # 这里有个trick的地方，fg.yaml 是根据模型的路径，找到的模型转换之后的yaml；
        # 而 fglib_py3.so 的地址 是fg-importer 获得的, 有可能两者对不上 (比如，模型发布完了之后，有人突然发布了新的 fg 版本。这样会导致使用了新的 fglib_py3.so)
        # 但是，鉴于模型端到端校验 工具使用的不是很频繁，因此这种case可以忽略
        fg_conf_path = os.path.join(
            pushed_model.origin_model_path, "output/online_model/fg/fg.yaml",
        )
        fg_lib_path = input_dict["fg_py_lib"][0].meta.uri

        with tempfile.TemporaryDirectory() as tempdir:
            self.fetch_fg(fg_conf_path, fg_lib_path, tempdir)

            local_origin_samples_path = self.filter_origin_samples(
                exec_properties["kafka_brokers"],
                exec_properties["kafka_topic"],
                tempdir,
                pushed_model,
                sample_count_limit,
            )

            local_processed_samples_path = os.path.join(
                tempdir, "processed_samples.tmp"
            )

            ret = self.process_origin_samples(
                tempdir, local_origin_samples_path, local_processed_samples_path
            )
            if ret != 0:
                raise RuntimeError("Failed to process origin samples")

            gziped_processed_samples = os.path.join(
                tempdir, "processed_samples.gz"
            )
            # gzip the file, to feed xdl
            with open(local_processed_samples_path, "rb") as f_in:
                with gzip.open(gziped_processed_samples, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            self.upload_to_remote(
                gziped_processed_samples, output_dict["samples"][0].meta.uri
            )

            self.upload_to_remote(
                local_origin_samples_path,
                output_dict["origin_samples"][0].meta.uri,
            )
