import os
import sys
import hashlib
import logging
import yaml
import collections
import tempfile
import subprocess
import gzip
import shutil
from typing import Dict, Text, List, Any
from datetime import datetime, timedelta
from pytz import timezone
from enum import Enum
from bmlx.flow import Executor, Artifact
from bmlx.utils import artifact_utils, io_utils
from bmlx_components.proto import model_pb2
from bmlx_components.validate_sample_gen import fg_main


class SampleGenExecutor(Executor):
    def select_origin_samples(
        self, origin_sample_uri_base, region
    ) -> List[Text]:
        cst_tz = timezone("Asia/Chongqing")
        current_time = datetime.now(cst_tz)
        # select sample started from 30mins ago
        start_time = current_time
        end_time = current_time - timedelta(minutes=30)
        origin_sample_uris = []
        while start_time >= end_time:
            dir_path = os.path.join(
                origin_sample_uri_base,
                f"day={start_time.strftime('%Y-%m-%d')}",
                f"min={start_time.strftime('%H')}{'{:02d}'.format(int(start_time.minute / 10) * 10)}",
                f"region={region}",
            )
            logging.info("try to get origin sample in path: %s", dir_path)
            if not io_utils.exists(dir_path):
                continue
            fs, path = io_utils.resolve_filesystem_and_path(dir_path)
            for (_, _, files) in fs.walk(path):
                for f in files:
                    if not f.endswith(".tmp"):
                        origin_sample_uris.append(os.path.join(dir_path, f))

            start_time -= timedelta(minutes=10)
        return origin_sample_uris

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

    def filter_origin_samples(
        self,
        local_dir: Text,
        origin_sample_uris: List[Text],
        pushed_model: model_pb2.PushedModel,
        sample_count_limit: int,
    ):

        local_origin_samples_path = os.path.join(
            local_dir, "origin_samples.txt"
        )

        sys.path.insert(
            0, os.path.join(os.path.dirname(__file__), "../brec_protos")
        )
        from welog.features import original_feature_pb2

        def filter_by_model_info(
            origin_bytes, pushed_model: model_pb2.PushedModel
        ):
            origin_feature = original_feature_pb2.OriginalFeature()
            origin_feature.ParseFromString(origin_bytes)

            rank_info = origin_feature.scenario.recommend_flow_info.rank_info
            if (
                rank_info.model_name != pushed_model.name
                or rank_info.model_version != pushed_model.version
            ):
                return True
            return False

        with open(local_origin_samples_path, "w") as origin_sample_fp:
            samples_count = 0
            for uri in origin_sample_uris:
                if samples_count >= sample_count_limit:
                    break
                fs, path = io_utils.resolve_filesystem_and_path(uri)
                local_file = os.path.join(local_dir, os.path.basename(path))
                fs.download(uri, local_file)

                with open(local_file, "r") as f:
                    for line in f.readlines():
                        origin_bytes = fg_main.parse_featurelog_line(line)
                        if not origin_bytes:
                            continue
                        if filter_by_model_info(origin_bytes, pushed_model):
                            continue

                        origin_sample_fp.write(line)
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

        pushed_model = io_utils.parse_pbtxt_file(
            model_meta_uri, model_pb2.PushedModel()
        )

        origin_sample_uri_base = exec_properties["origin_sample_uri_base"]
        sample_count_limit = exec_properties["output_sample_limit"]

        region = exec_properties["region"]
        origin_sample_uris = self.select_origin_samples(
            origin_sample_uri_base, region
        )
        if not origin_sample_uris:
            raise RuntimeError("Failed to select origin sample uris")

        assert len(output_dict["samples"]) == 1
        assert len(output_dict["origin_samples"]) == 1

        fg_conf_path = os.path.join(
            pushed_model.origin_model_path,
            "converted_model/online_model/fg/fg.yaml",
        )

        assert len(input_dict["fg_py_lib"]) == 1
        fg_lib_path = input_dict["fg_py_lib"][0].meta.uri

        with tempfile.TemporaryDirectory() as tempdir:
            self.fetch_fg(fg_conf_path, fg_lib_path, tempdir)

            local_origin_samples_path = self.filter_origin_samples(
                tempdir, origin_sample_uris, pushed_model, sample_count_limit
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
