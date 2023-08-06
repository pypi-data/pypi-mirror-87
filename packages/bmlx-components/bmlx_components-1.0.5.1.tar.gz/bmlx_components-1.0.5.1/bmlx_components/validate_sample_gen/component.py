from typing import Text, Optional, List
from bmlx.flow import (
    Component,
    ComponentSpec,
    ExecutorClassSpec,
    DriverClassSpec,
    ExecutionParameter,
    ChannelParameter,
    Channel,
)
from bmlx.execution.driver import BaseDriver
from bmlx.metadata import standard_artifacts
from bmlx_components import custom_artifacts
from bmlx.execution.launcher import Launcher
from bmlx_components.validate_sample_gen.executor import SampleGenExecutor

"""
从原始数据example (original feature), 特征预处理得到 sample

执行逻辑：
1. 从hdfs上获取当前时间附近的 original featurelog
2. 根据pushed_model 信息进行过滤，只保留需要进行一致性校验的 origin featurelog
3. 将origin featurelog 进行预处理，得到samples
4. 保存步骤2 产生的 origin sample 和 步骤3 产生的sample

NOTE:
由于目前这个component 只是用于一致性校验，一致性校验需要的sample数量很小. 所以直接
从hdfs 拉取original feature log，然后利用 fg.so 处理

如果需要处理大量数据，需要改造成提交到spark上执行
"""


class SampleGenSpec(ComponentSpec):
    """ sample gen spec """

    PARAMETERS = {
        "origin_sample_uri_base": ExecutionParameter(type=str, optional=False),
        "region": ExecutionParameter(type=str, optional=False),
        "output_sample_limit": ExecutionParameter(type=int, optional=True),
    }

    INPUTS = {
        "fg_py_lib": ChannelParameter(type=custom_artifacts.FgPyLib),
        "pushed_model": ChannelParameter(type=custom_artifacts.PushedModel),
    }

    OUTPUTS = {
        "origin_samples": ChannelParameter(type=custom_artifacts.OriginSamples),
        "samples": ChannelParameter(type=standard_artifacts.Samples),
    }


class SampleGen(Component):
    SPEC_CLASS = SampleGenSpec
    EXECUTOR_SPEC = ExecutorClassSpec(SampleGenExecutor)
    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(
        self,
        pushed_model: Channel,
        fg_py_lib: Channel,
        origin_sample_uri_base: Text,
        region: Text,
        output_sample_limit: int = 1000,
        instance_name: Optional[Text] = None,
    ):
        samples = Channel(
            artifact_type=standard_artifacts.Samples,
            artifacts=[standard_artifacts.Samples()],
        )
        origin_samples = Channel(
            artifact_type=custom_artifacts.OriginSamples,
            artifacts=[custom_artifacts.OriginSamples()],
        )
        spec = SampleGenSpec(
            pushed_model=pushed_model,
            fg_py_lib=fg_py_lib,
            samples=samples,
            origin_samples=origin_samples,
            origin_sample_uri_base=origin_sample_uri_base,
            region=region,
            output_sample_limit=output_sample_limit,
        )

        super(SampleGen, self).__init__(spec=spec, instance_name=instance_name)

    def get_launcher_class(self, ctx):
        return Launcher
