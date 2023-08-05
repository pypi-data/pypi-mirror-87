"""bmlx xdl evaluator executor."""
import os
import logging
import re
import xdl
import functools
import random
from typing import Any, Dict, List, Text

from bmlx.flow import Executor, Artifact
from bmlx_components.proto import schema_pb2, model_pb2
from bmlx.utils import import_utils, artifact_utils, io_utils
from bmlx_components.xdl_base.runner import XdlRunner
from bmlx_components.xdl_base.executor import XdlExecutor


class XdlPredictorExecutor(XdlExecutor):
    def execute_as_worker(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        """
        XDL Predictor Executor invokes a training_fn callback function provided by
        the user via the module_file parameter.
        """
        schema = self._resolve_schema(input_dict["schema"])
        assert (
            exec_properties.get("parameters") is not None
        ), "please call _load_xdl_parameters first"

        # resolve train func
        stage = exec_properties["stage"]
        module = exec_properties.get("module")
        parameters = exec_properties["parameters"]
        # predict 模式phase = 1
        updated_dict = {"phases": 1, "reader.enable_state": False}

        if exec_properties["enable_trace"]:
            meta_output_path = artifact_utils.get_single_uri(
                output_dict["output"]
            )
            updated_dict.update({"hooks.trace.output_dir": meta_output_path})

        if exec_properties["keep_order"]:
            updated_dict["reader.batch_size"] = 1

        parameters.set_args(updated_dict)

        module = exec_properties.get("module")

        if not module:
            raise ValueError(
                "'module_file' or 'module' field not set in 'exec_properties'."
            )

        runner = XdlRunner(
            model_module=module,
            parameters=parameters,
            stage=stage,
            is_training=False,
            schema=schema,
            is_local=exec_properties["is_local"],
        )

        reader = XdlRunner.get_xdl_reader(
            conf=parameters["reader"],
            name="xdl_reader",
            input_dict=input_dict,
            schema=schema,
            sampling_rate=exec_properties["sampling_rate"],
        )

        runner.run(reader=reader)
