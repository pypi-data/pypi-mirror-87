"""BMLX Trainer component definition."""
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
from bmlx_components.xdl_trainer.executor import XdlTrainerExecutor
from bmlx_components.xdl_trainer.launcher import XdlTrainerLauncher


class XdlTrainerSpec(ComponentSpec):
    """Trainer component spec."""

    PARAMETERS = {
        "sampling_rate": ExecutionParameter(type=float, optional=True),
        "module": ExecutionParameter(type=(str, Text), optional=True),
        "model_uri_base": ExecutionParameter(type=(str, Text), optional=True),
        "namespace": ExecutionParameter(type=(str, Text), optional=True),
        "model_file_pattern": ExecutionParameter(type=(list), optional=True),
        "warmup_model_bank": ExecutionParameter(
            type=(str, Text), optional=True
        ),
        "enable_trace": ExecutionParameter(type=bool, optional=True),
    }

    INPUTS = {
        "schema": ChannelParameter(type=standard_artifacts.Schema),
        "samples": ChannelParameter(type=standard_artifacts.Samples),
        "previous_model": ChannelParameter(
            type=standard_artifacts.Model, optional=True
        ),
    }

    OUTPUTS = {
        "output": ChannelParameter(type=standard_artifacts.Model),
    }


class XdlTrainer(Component):
    SPEC_CLASS = XdlTrainerSpec

    EXECUTOR_SPEC = ExecutorClassSpec(XdlTrainerExecutor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(
        self,
        samples: Channel,
        schema: Channel,
        model_uri_base: Text,
        previous_model: Optional[Channel] = None,
        model_file_pattern: Optional[List[Text]] = [
            "phase0_emb/(.*)",
            "phase0_tf/(.*)",
        ],
        warmup_model_bank: Optional[Text] = None,
        sampling_rate: float = 1.0,
        module: Optional[Text] = "",
        namespace: Optional[Text] = "default",
        output: Optional[Channel] = None,
        enable_trace: bool = False,
        instance_name: Optional[Text] = None,
    ):
        if not model_uri_base:
            raise ValueError("model_uri_base does not set")

        if not samples:
            raise ValueError("samples not provided")

        if not isinstance(model_file_pattern, list):
            raise ValueError("previous model pattern must be list of str")

        output = output or Channel(
            artifact_type=standard_artifacts.Model,
            artifacts=[standard_artifacts.Model()],
        )

        if not instance_name:
            instance_name = "xdl_train"

        spec = XdlTrainerSpec(
            samples=samples,
            schema=schema,
            sampling_rate=sampling_rate,
            previous_model=previous_model,
            model_uri_base=model_uri_base,
            module=module,
            namespace=namespace,
            output=output,
            model_file_pattern=model_file_pattern,
            warmup_model_bank=warmup_model_bank,
            enable_trace=enable_trace,
        )

        super(XdlTrainer, self).__init__(spec=spec, instance_name=instance_name)

    def get_launcher_class(self, ctx):
        return XdlTrainerLauncher

    def stage(self):
        return "train"
