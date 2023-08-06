import os
import sys
import logging
import re
import math
import functools
import time
import pathlib
import subprocess
import shutil
import tempfile
from datetime import datetime, timedelta
from pytz import timezone
from typing import Any, Dict, List, Text

from bmlx.flow import Executor, Artifact
from bmlx_components.proto import schema_pb2, model_pb2
from bmlx.utils import import_utils, artifact_utils, io_utils

from bmlx_components.utils import cannon_publisher
from bmlx_components.rtp_pusher_v2 import resource_uploader


class PusherExecutor(Executor):
    def _resolve_model_meta(self, model_meta_path):
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

    def fetch_build_tools(self, remote_dir: Text, local_dir: Text):
        fs, uri = io_utils.resolve_filesystem_and_path(remote_dir)
        for tool in ["partition.exe", "build.exe"]:
            with open(os.path.join(local_dir, tool), "wb") as o:
                with fs.open(os.path.join(remote_dir, tool), "rb") as i:
                    o.write(i.read())

    def build_embedding(
        self, local_embedding_path: Text, tool_path: Text, result_path: Text
    ):
        def get_all_dims(emb_bin_path):
            fs, path = io_utils.resolve_filesystem_and_path(emb_bin_path)
            assert fs.isdir(path)
            emb_dir_list = [f for f in fs.ls(path) if fs.isdir(f)]
            if not emb_dir_list:
                raise RuntimeError("Invalid emb_bin_path %s" % emb_bin_path)
            emb_dims = [int(d.split("/")[-1]) for d in emb_dir_list]
            return emb_dims

        def calculate_partiton_level(emb_dir):
            total_size = sum(
                f.stat().st_size
                for f in pathlib.Path(emb_dir).glob("**/*")
                if f.is_file()
            )
            if total_size > 1024 * 1024 * 1024 * 30:
                raise RuntimeError(
                    "Too large embedding data, total size: %d", total_size
                )

            level = int(math.log(total_size / 671088640, 2))
            if level > 7:
                return 7
            elif level < 0:
                return 0
            else:
                return level

        def partiton_and_build(
            tool_path, dim, partiton_level, input_dir, output_dir
        ):
            partiton_tool_path = os.path.join(tool_path, "partition.exe")
            build_tool_path = os.path.join(tool_path, "build.exe")
            tmp_dir = os.path.join(tool_path, "embedding_tmp_{}".format(dim))
            os.mkdir(tmp_dir)

            partition_command = f"chmod a+x {partiton_tool_path} && {partiton_tool_path} --dim={dim} --level={partiton_level} --input={input_dir} --output_dir={tmp_dir}"
            logging.info("executing %s", partition_command)
            ret = subprocess.run(
                partition_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if ret.returncode != 0:
                raise RuntimeError(
                    "Failed to partition embedding, command: %s, return code: %d, logs: %s"
                    % (partition_command, ret.returncode, ret.stdout)
                )

            build_command = f"chmod a+x {build_tool_path} && {build_tool_path} --dim={dim} --thread_level=4 --level={partiton_level} --input_dir={tmp_dir} --output={output_dir}/dim-{dim}.emb"
            logging.info("executing %s", build_command)
            ret = subprocess.run(
                build_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if ret.returncode != 0:
                raise RuntimeError(
                    "Failed to build embedding, command: %s, return code: %d, logs: %s"
                    % (build_command, ret.returncode, ret.stdout)
                )

        if not os.path.exists(result_path):
            os.mkdir(result_path)

        emb_dims = get_all_dims(local_embedding_path)

        for dim in emb_dims:
            emb_dir = os.path.join(local_embedding_path, str(dim))

            logging.info("build embedding with dimension %d", dim)

            partition_level = calculate_partiton_level(emb_dir)

            partiton_and_build(
                tool_path, dim, partition_level, emb_dir, result_path
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
        model_meta_pb = self._resolve_model_meta(
            input_dict["converted_model"][0].meta.uri
        )

        model_version = int(time.time())

        with tempfile.TemporaryDirectory() as tempdir:
            # download model folder from remote
            model_path = os.path.dirname(model_meta_pb.graph_path.strip("/"))
            local_model_dir = os.path.join(tempdir, "raw_model")
            io_utils.download_dir(model_path, local_model_dir)

            # download build tools
            self.fetch_build_tools(
                exec_properties["embedding_build_tool_dir"], tempdir
            )

            # build model embedding
            converted_model_dir = os.path.join(tempdir, "converted_model")

            # copy online model part
            shutil.copytree(
                os.path.join(local_model_dir, "online_model"),
                converted_model_dir,
            )

            self.build_embedding(
                os.path.join(local_model_dir, "emb_bin"),
                tempdir,
                converted_model_dir,
            )

            if not resource_uploader.upload_and_sync(
                ns=exec_properties["product_namespace"],
                local_dir=converted_model_dir,
                name=exec_properties["model_name"],
                version=model_version,
            ):
                raise RuntimeError(
                    "Failed to upload and sync resource to ceto platform"
                )
