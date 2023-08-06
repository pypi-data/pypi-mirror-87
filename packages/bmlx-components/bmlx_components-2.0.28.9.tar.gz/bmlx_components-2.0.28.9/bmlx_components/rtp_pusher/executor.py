import os
import sys
import logging
import re
import functools
import time
import hashlib
import tempfile
from datetime import datetime, timedelta
from pytz import timezone
from typing import Any, Dict, List, Text

from bmlx.flow import Executor, Artifact
from bmlx_components.proto import schema_pb2, model_pb2
from bmlx.utils import import_utils, artifact_utils, io_utils

from bmlx_components.utils import ceto_publisher, cyclone_publisher

CETO_MODEL_BASE_DIR = "hdfs://bigocluster/data/models"


class PusherExecutor(Executor):
    def _resolve_converted_model_meta(self, model_meta_path):
        fs, path = io_utils.resolve_filesystem_and_path(model_meta_path)
        if not fs.exists(path):
            raise RuntimeError(
                "model_meta_path %s does not exist!" % model_meta_path
            )

        model_pb = io_utils.parse_pbtxt_file(
            os.path.join(model_meta_path, "converted_model.pbtxt"),
            model_pb2.ConvertedModel(),
        )

        if not (model_pb and model_pb.embedding_path and model_pb.graph_path):
            raise RuntimeError(
                "invalid model meta info parsed from %s" % model_meta_path
            )
        logging.info("parsed pushed model meta info: %s", model_pb)

        fs, path = io_utils.resolve_filesystem_and_path(model_pb.embedding_path)
        if not fs.exists(path):
            raise RuntimeError(
                "model embedding path %s does not exist!"
                % model_pb.embedding_path
            )

        fs, path = io_utils.resolve_filesystem_and_path(model_pb.graph_path)
        if not fs.exists(path):
            raise RuntimeError(
                "model graph path %s does not exist!" % model_pb.graph_path
            )

        return model_pb

    def _parse_shard_info(self, emb_bin_path, model_version):
        shards = {}

        fs, path = io_utils.resolve_filesystem_and_path(emb_bin_path)
        for fpath in fs.ls(path):
            if fpath.find("emb_bin/meta_") < 0:
                raise ValueError(
                    "Invalid emb bin meta file %s, should contains 'emb_bin/meta_'"
                    % fpath
                )
            part = int(fpath.split("emb_bin/meta_")[1])
            # 头 8 个字节为文件长度
            file_content = io_utils.read_file_string(fpath).decode()[8:]
            for line in file_content.split("\n"):
                dim, misc = line.split("|", 1)

                shards.setdefault(dim, [])

                path, start, end, count, size = misc.split(",", 4)
                shard = {
                    "shard_idx": part,
                    "tail_number_start": int(start),
                    "tail_number_end": int(end),
                    "sub_models": [
                        {
                            "model_uri": os.path.join(
                                CETO_MODEL_BASE_DIR, path
                            ),
                            "publish_time": model_version,
                            "hdfs_path": os.path.join(
                                CETO_MODEL_BASE_DIR, path
                            ),
                            "sub_version": str(model_version),
                            "keys_count": int(count),
                            "data_size": int(size),
                        }
                    ],
                }

                shards[dim].append(shard)

        return shards

    def publish_embeddings(self, model_name, model_version, emb_bin_path):
        all_shards = self._parse_shard_info(emb_bin_path, model_version)
        for dim, shards in all_shards.items():
            cyclone_options = cyclone_publisher.CycloneOptions(
                f"{model_name}_{dim}", model_version  # 构造model name = name_dim
            )

            if not cyclone_publisher.publish_model_to_cyclone(
                cyclone_options, shards
            ):
                raise RuntimeError(
                    "Failed to publish model to cyclone, dim: %d",
                )
        logging.info("publish model to cyclone server successfully!")

    def publish_graph(self, model_name, model_version, namespace, graph_path):
        # copy file to ceto"s model dir
        graph_dir_name = os.path.basename(graph_path)
        ceto_model_path = (
            f"{CETO_MODEL_BASE_DIR}/{namespace}/{model_name}/{model_version}"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            io_utils.download_dir(
                graph_path, os.path.join(tmpdir, graph_dir_name)
            )
            io_utils.upload_dir(
                os.path.join(tmpdir, graph_dir_name), ceto_model_path
            )
        # update meta to ceto
        ret = ceto_publisher.publish_model_to_ceto(
            model_name, namespace, model_version, ceto_model_path
        )
        if not ret:
            logging.error(
                "Failed to publish model to ceto, model name: %s, namespace: %s, model_version: %s, ceto_model_path: %s",
                model_name,
                namespace,
                model_version,
                ceto_model_path,
            )
            raise RuntimeError("Failed to publish model to ceto!")
        else:
            logging.info(
                "Successfully publish model to ceto, model name: %s, namespace: %s, model_version: %s, ceto_model_path: %s",
                model_name,
                namespace,
                model_version,
                ceto_model_path,
            )

    def save_meta(
        self, meta_output_path, model_name, model_version, origin_model_path
    ):
        logging.info("push finished, model meta gen to %s" % meta_output_path)
        pushed_model = model_pb2.PushedModel()
        pushed_model.version = model_version
        pushed_model.name = model_name
        pushed_model.origin_model_path = origin_model_path
        pushed_model.pushed_time = int(time.time())
        io_utils.write_pbtxt_file(
            os.path.join(meta_output_path, "pushed_model.pbtxt"), pushed_model
        )

    def execute(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        self._log_startup(input_dict, output_dict, exec_properties)

        assert (
            "converted_model" in input_dict
            and len(input_dict["converted_model"]) == 1
        )
        converted_model_meta = self._resolve_converted_model_meta(
            input_dict["converted_model"][0].meta.uri
        )

        model_name = exec_properties["model_name"]
        namespace = exec_properties["namespace"]
        # 在xdl convert 中, 指定了model version, 并且将embedding数据转换成zmap格式，存放在了ceto指定的embedding目录下的 model_version子目录下
        # 这里的model version 和 converted_model 的 model version 保持一致
        model_version = converted_model_meta.converted_model_version

        # publish embedding
        self.publish_embeddings(
            model_name, model_version, converted_model_meta.embedding_path
        )

        self.publish_graph(
            model_name,
            model_version,
            namespace,
            converted_model_meta.graph_path,
        )

        self.save_meta(
            artifact_utils.get_single_uri(output_dict["output"]),
            model_name,
            model_version,
            os.path.dirname(converted_model_meta.graph_path),
        )
