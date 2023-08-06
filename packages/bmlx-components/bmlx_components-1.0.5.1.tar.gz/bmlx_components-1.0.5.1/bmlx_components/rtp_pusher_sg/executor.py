import os
import sys
import logging
import re
import functools
import time
import hashlib
import subprocess
import tempfile
from datetime import datetime, timedelta
from pytz import timezone
from typing import Any, Dict, List, Text

from bmlx.flow import Executor, Artifact
from bmlx_components.proto import schema_pb2, model_pb2
from bmlx.utils import import_utils, artifact_utils, io_utils

from bmlx_components.utils import cannon_publisher


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

    def skip_publish_model(self, model_meta_pb, skip_stale_model_hour):
        if re.match("^[0-9]{8}\/[0-9]{2}$", model_meta_pb.model_version):
            cst_tz = timezone("Asia/Chongqing")
            model_time = datetime.strptime(
                f"{model_meta_pb.model_version} +0800", "%Y%m%d/%H %z"
            )
            if datetime.now(cst_tz) - model_time > timedelta(
                hours=skip_stale_model_hour
            ):
                return True
        return False

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
        skip_stale_model_hour = exec_properties["skip_stale_model_hour"]

        if self.skip_publish_model(model_meta_pb, skip_stale_model_hour):
            cst_tz = timezone("Asia/Chongqing")
            logging.info(
                "model is %d hours earlier, model time: %s, "
                "current time: %s, skip to publish this model !!!!",
                skip_stale_model_hour,
                model_meta_pb.model_version,
                datetime.now(cst_tz).strftime("%Y%m%d/%H"),
            )
            return

        pub_tool_path = os.path.join(
            os.path.dirname(__file__), "../brec_publish_tools/pub_tools_v1"
        )
        converted_model_path = os.path.join(model_meta_pb.graph_path, "../")

        command = f"""cd {pub_tool_path} && bash -x run_xdl.sh --convert_pub_hdfs={converted_model_path} --model_name={exec_properties["model_name"]} \
            --graph_collection={exec_properties["graph_collection"]} --namespace={exec_properties["product_namespace"]} \
            --creator={exec_properties["author"]} --is_sg={exec_properties["send_sg"]}"""

        logging.info("start to publish, command: %s", command)
        ret = subprocess.run(command, shell=True)
        if ret.returncode != 0:
            raise RuntimeError("Failed to publish model using rtp_pusher_sg")
