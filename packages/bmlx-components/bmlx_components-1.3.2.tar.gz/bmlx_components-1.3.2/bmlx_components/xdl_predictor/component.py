"""BMLX XdlPredictor component definition."""
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
from bmlx_components.xdl_predictor.executor import XdlPredictorExecutor
from bmlx_components.xdl_predictor.launcher import XdlPredictorLauncher


class XdlPredictorSpec(ComponentSpec):
    """XdlPredictor component spec."""

    PARAMETERS = {
        "sampling_rate": ExecutionParameter(type=float, optional=False),
        "module": ExecutionParameter(type=(str, Text), optional=True),
        "namespace": ExecutionParameter(type=(str, Text), optional=True),
        "model_file_pattern": ExecutionParameter(type=(list), optional=True),
        # 是否保证样本文件和最终的trace结果中的 item 顺序一致。
        # 保证顺序一致，常用于 RTP的小样本验证，此时bmlx 会设置xdl predict的 batch size = 1，且设置worker instance= 1
        "keep_order": ExecutionParameter(type=bool, optional=False),
        "enable_trace": ExecutionParameter(type=bool, optional=True),
    }

    INPUTS = {
        "schema": ChannelParameter(type=standard_artifacts.Schema),
        "samples": ChannelParameter(type=standard_artifacts.Samples),
        "model": ChannelParameter(type=standard_artifacts.Model),
    }

    OUTPUTS = {
        "output": ChannelParameter(type=custom_artifacts.PredictResult),
    }


class XdlPredictor(Component):
    SPEC_CLASS = XdlPredictorSpec

    EXECUTOR_SPEC = ExecutorClassSpec(XdlPredictorExecutor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(
        self,
        samples: Channel,
        schema: Channel,
        model: Channel,
        keep_order: bool = True,
        module: Optional[Text] = "",
        sampling_rate: float = 1.0,
        model_file_pattern: Optional[List[Text]] = [
            "phase0_emb/(.*)",
            "phase0_tf/(.*)",
        ],
        namespace: Optional[Text] = "default",
        enable_trace: bool = True,
        instance_name: Optional[Text] = None,
    ):
        if not samples:
            raise ValueError("samples not provided")

        if not model:
            raise ValueError("model not provided")

        if not schema:
            raise ValueError("schema not provided")

        if not instance_name:
            instance_name = "xdl_predict"

        output = Channel(
            artifact_type=custom_artifacts.PredictResult,
            artifacts=[custom_artifacts.PredictResult()],
        )

        spec = XdlPredictorSpec(
            model=model,
            samples=samples,
            schema=schema,
            module=module,
            output=output,
            namespace=namespace,
            model_file_pattern=model_file_pattern,
            sampling_rate=sampling_rate,
            keep_order=keep_order,
            enable_trace=enable_trace,
        )
        super(XdlPredictor, self).__init__(
            spec=spec, instance_name=instance_name
        )

    def get_launcher_class(self, ctx):
        return XdlPredictorLauncher

    def stage(self):
        return "predict"
