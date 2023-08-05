"""BMLX XdlEvaluator component definition."""
from typing import Optional, Text, List
from bmlx.flow import (
    Channel,
    Component,
    ComponentSpec,
    ExecutorClassSpec,
    DriverClassSpec,
    ExecutionParameter,
    ChannelParameter,
)
from bmlx.execution.driver import BaseDriver
from bmlx.metadata import standard_artifacts
from bmlx_components import custom_artifacts
from bmlx_components.xdl_evaluator.executor import XdlEvaluatorExecutor
from bmlx_components.xdl_evaluator.launcher import XdlEvalLauncher


class XdlEvaluatorSpec(ComponentSpec):
    """XdlEvaluator component spec."""

    PARAMETERS = {
        "sampling_rate": ExecutionParameter(type=float, optional=True),
        "module": ExecutionParameter(type=(str, Text), optional=True),
        "namespace": ExecutionParameter(type=(str, Text), optional=True),
        "model_file_pattern": ExecutionParameter(type=(list), optional=True),
        "model_uri_base": ExecutionParameter(type=(str, Text), optional=False),
        "enable_trace": ExecutionParameter(type=bool, optional=True),
    }

    INPUTS = {
        "schema": ChannelParameter(type=standard_artifacts.Schema),
        "samples": ChannelParameter(type=standard_artifacts.Samples),
        "model": ChannelParameter(type=standard_artifacts.Model),
    }

    OUTPUTS = {
        "output": ChannelParameter(type=custom_artifacts.ModelEval),
    }


class XdlEvaluator(Component):
    SPEC_CLASS = XdlEvaluatorSpec

    EXECUTOR_SPEC = ExecutorClassSpec(XdlEvaluatorExecutor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(
        self,
        samples: Channel,
        schema: Channel,
        model: Channel,
        sampling_rate: float = 1.0,
        module: Optional[Text] = "",
        model_file_pattern: Optional[List[Text]] = [
            "phase0_emb/(.*)",
            "phase0_tf/(.*)",
        ],
        model_uri_base: Optional[Text] = "",
        namespace: Optional[Text] = "default",
        output: Optional[Text] = None,
        enable_trace: bool = False,
        instance_name: Optional[Text] = None,
    ):
        if not samples:
            raise ValueError("samples not provided")

        if not model:
            raise ValueError("model not provided")

        if not schema:
            raise ValueError("schema not provided")

        output = output or Channel(
            artifact_type=custom_artifacts.ModelEval,
            artifacts=[custom_artifacts.ModelEval()],
        )

        if not instance_name:
            instance_name = "xdl_eval"

        spec = XdlEvaluatorSpec(
            model=model,
            samples=samples,
            schema=schema,
            module=module,
            model_file_pattern=model_file_pattern,
            model_uri_base=model_uri_base,
            sampling_rate=sampling_rate,
            namespace=namespace,
            output=output,
            enable_trace=enable_trace,
        )
        super(XdlEvaluator, self).__init__(
            spec=spec, instance_name=instance_name
        )

    def get_launcher_class(self, ctx):
        return XdlEvalLauncher

    def stage(self):
        return "eval"
