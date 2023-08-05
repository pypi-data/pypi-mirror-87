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


class XdlEvaluatorExecutor(XdlExecutor):
    def execute_as_worker(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        """
        XDL Evaluator Executor invokes a training_fn callback function provided by
        the user via the module_file parameter.
        """
        _, model_version = self._resolve_latest_sample_meta(
            input_dict["samples"]
        )
        if "model" not in input_dict or not input_dict["model"]:
            logging.info("no model to eval, return")
            return

        stage = exec_properties["stage"]
        parameters = exec_properties["parameters"]
        schema = self._resolve_schema(input_dict["schema"])

        module = exec_properties.get("module")

        if not module:
            raise ValueError("'module' field not set in 'exec_properties'.")

        # eval模式phase = 1
        updated_dict = {"phases": 1, "reader.enable_state": False}

        if exec_properties["enable_trace"]:
            meta_output_path = artifact_utils.get_single_uri(
                output_dict["output"]
            )
            updated_dict.update({"hooks.trace.output_dir": meta_output_path})

        parameters.set_args(updated_dict)

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
