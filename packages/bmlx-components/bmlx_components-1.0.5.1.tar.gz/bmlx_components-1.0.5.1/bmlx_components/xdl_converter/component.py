"""BMLX model converter component definition."""
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
from bmlx_components.xdl_converter.executor import XdlConverterExecutor
from bmlx_components.xdl_converter.launcher import XdlConverterLauncher


class XdlConverterSpec(ComponentSpec):
    """ModelConverter component spec."""

    PARAMETERS = {
        # 导出emb bin 时fea score 的统一过滤阈值, required
        "export_emb_default_threshold": ExecutionParameter(
            type=float, optional=False
        ),
        # 导出emb_bin 时，embedding部分转成fp16，统计特征转成bf16，默认不转
        "half_p": ExecutionParameter(type=bool, optional=True),
        # converted 之后的模型的output路径
        "output_dir": ExecutionParameter(type=(str, Text), optional=True),
        # 转换为在线预测图output 节点名字,如：y_pred = tf.sigmoid(y, name='xxx')。
        # 转化时会自动根据xxx为后缀寻找node 全称，这就要求xxx 在导出图里全局唯一。
        # 默认为 predict_node
        "output_node": ExecutionParameter(type=(str, Text), optional=True),
        "exclude_slots": ExecutionParameter(type=List[Text], optional=True),
        "model_class": ExecutionParameter(type=(str, Text), optional=True),
        "model_file_pattern": ExecutionParameter(type=(list), optional=True),
        "namespace": ExecutionParameter(type=(str, Text), optional=True),
        "optimize_tool_path": ExecutionParameter(
            type=(str, Text), optional=True
        ),
    }

    INPUTS = {
        # xdl 训练出来的原始模型
        "model": ChannelParameter(type=standard_artifacts.Model),
        "fg_conf": ChannelParameter(type=custom_artifacts.FgConf),
        "fg_lib": ChannelParameter(
            type=custom_artifacts.FgCppLib, optional=True
        ),
        # 小样本验证的 original sample 和 model sample
        "validate_origin_samples": ChannelParameter(
            type=custom_artifacts.OriginSamples, optional=True
        ),
        "validate_samples": ChannelParameter(
            type=standard_artifacts.Samples, optional=True
        ),
        "validate_predict_result": ChannelParameter(
            type=custom_artifacts.PredictResult, optional=True
        ),
    }

    OUTPUTS = {
        "output": ChannelParameter(type=custom_artifacts.ConvertedModel),
    }


class XdlConverter(Component):
    SPEC_CLASS = XdlConverterSpec

    EXECUTOR_SPEC = ExecutorClassSpec(XdlConverterExecutor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(
        self,
        model: Channel,
        fg_conf: Channel,
        fg_lib: Optional[Channel] = None,
        validate_origin_samples: Optional[Channel] = None,
        validate_samples: Optional[Channel] = None,
        validate_predict_result: Optional[Channel] = None,
        export_emb_default_threshold: float = 0.0,
        half_p: Optional[bool] = False,
        output_dir: Optional[Text] = None,
        output_node: Optional[Text] = "predict_node",
        exclude_slots: Optional[List[Text]] = [],
        model_class: Optional[Text] = "",
        model_file_pattern: Optional[List[Text]] = [
            "phase0_emb/(.*)",
            "phase0_tf/(.*)",
        ],
        converted_model: Optional[Channel] = None,
        optimize_tool_path: Optional[Text] = None,
        namespace: Optional[Text] = "default",
        instance_name: Optional[Text] = None,
    ):

        if not model:
            raise ValueError("model not provided")

        if not fg_conf:
            raise ValueError("fg_conf not provided")

        converted_model = converted_model or Channel(
            artifact_type=custom_artifacts.ConvertedModel,
            artifacts=[custom_artifacts.ConvertedModel()],
        )

        if not instance_name:
            instance_name = "xdl_convert"

        spec = XdlConverterSpec(
            model=model,
            fg_conf=fg_conf,
            fg_lib=fg_lib,
            validate_origin_samples=validate_origin_samples,
            validate_samples=validate_samples,
            validate_predict_result=validate_predict_result,
            export_emb_default_threshold=export_emb_default_threshold,
            half_p=half_p,
            namespace=namespace,
            output_dir=output_dir,
            output_node=output_node,
            exclude_slots=exclude_slots,
            model_file_pattern=model_file_pattern,
            model_class=model_class,
            output=converted_model,
            optimize_tool_path=optimize_tool_path,
        )

        super(XdlConverter, self).__init__(
            spec=spec, instance_name=instance_name
        )

    def get_launcher_class(self, ctx):
        return XdlConverterLauncher

    def stage(self):
        return "convert"
