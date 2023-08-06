import logging
import os
import time
import re
import hashlib
from datetime import datetime, timedelta
from pytz import timezone
from typing import Dict, Text, Any, Optional

from bmlx.flow import Driver, DriverArgs, Channel, Pipeline, Component, Artifact
from bmlx.metadata.metadata import Metadata
from bmlx.utils import io_utils
from bmlx.execution.execution import ExecutionInfo
from bmlx_components.importer_node.import_checker import (
    check_succ_flag,
    check_skip_flag,
)
from bmlx_components.utils.config_center_gw import ConfigCenterGw
from bmlx_components.proto import model_pb2

from bmlx.metadata import standard_artifacts
from bmlx_components import custom_artifacts

MODEL_PARSE_PATTERN = (
    ".*(hdfs:[a-zA-Z0-9\/\-_]*\/[0-9]{8}\/[0-9]{2})\/[\s\S]*version\: ([\d]+).*"
)


class ModelSelectorDriver(Driver):
    def __init__(self, metadata: Metadata):
        self._metadata = metadata
        self._cc_gw = ConfigCenterGw()

    def _parse_pushed_model(self, config_info) -> model_pb2.PushedModel:
        pushed_model = model_pb2.PushedModel()
        ret = re.match(MODEL_PARSE_PATTERN, config_info["value"])

        pushed_model.origin_model_path = ret.group(1)
        pushed_model.name = config_info["name"]
        pushed_model.version = int(ret.group(2))
        return pushed_model

    def _save_pushed_model_meta(
        self,
        pushed_model: model_pb2.PushedModel,
        pushed_model_storage_base_path: Text,
    ):
        if not io_utils.exists(pushed_model_storage_base_path):
            io_utils.mkdirs(pushed_model_storage_base_path)

        hasher = hashlib.md5()
        hasher.update(pushed_model.SerializeToString())
        checksum = hasher.hexdigest()
        meta_path = os.path.join(
            pushed_model_storage_base_path, checksum, "pushed_model.pbtxt"
        )
        if not io_utils.exists(meta_path):
            io_utils.write_pbtxt_file(meta_path, pushed_model)
        return meta_path

    def pre_execution(
        self,
        input_dict: Dict[Text, Channel],
        output_dict: Dict[Text, Channel],
        exec_properties: Dict[Text, Any],
        pipeline: Pipeline,
        component: Component,
        driver_args: DriverArgs,
        artifact_base_uri: Optional[Text] = "",
    ) -> ExecutionInfo:
        logging.info(
            "online_model_selector exec properties: %s", exec_properties
        )

        min_serve_minutes = exec_properties["min_serve_minutes"]
        model_collection = exec_properties["model_collection"]
        model_name = exec_properties["model_name"]

        published_configs = self._cc_gw.get_published_configs(
            namespace="RESOURCE",
            group=model_collection,
            conf_name=model_name,
            num=1,
        )

        if not (
            len(published_configs)
            == 1
            # and published_configs[0]["status"] == 2
        ):
            raise RuntimeError(
                "Failed to get published configs using model_collection: %s, model_name: %s"
                % (model_collection, model_name)
            )

        config = published_configs[0]
        assert config["name"] == model_name

        while (
            int(datetime.now().timestamp()) - config["mtime"] / 1000
            <= min_serve_minutes * 60
        ):
            logging.info(
                "waiting until model to be served more than %d minutes"
                % min_serve_minutes
            )
            time.sleep(60)

        output_artifacts = {}
        assert len(output_dict) == 2

        pushed_model_storage_base_path = os.path.join(
            artifact_base_uri, "pushed_model"
        )
        pushed_model = self._parse_pushed_model(config)

        if pushed_model.origin_model_path:
            # generate pushed model artifact
            artifact = Artifact(
                type_name=custom_artifacts.PushedModel.TYPE_NAME
            )
            artifact.meta.uri = self._save_pushed_model_meta(
                pushed_model, pushed_model_storage_base_path
            )
            artifact.meta.import_only = True
            artifact.meta.producer_component = component.id
            output_artifacts["pushed_model"] = [artifact]
            # generate model artifact
            artifact = Artifact(type_name=standard_artifacts.Model.TYPE_NAME)
            artifact.meta.uri = pushed_model.origin_model_path
            artifact.meta.producer_component = component.id
            artifact.meta.import_only = True
            output_artifacts["model"] = [artifact]

        logging.info(
            "selected pushed model: %s, origin model: %s",
            pushed_model,
            pushed_model.origin_model_path,
        )
        return ExecutionInfo(
            input_dict={},
            output_dict=output_artifacts,
            exec_properties=exec_properties,
        )
