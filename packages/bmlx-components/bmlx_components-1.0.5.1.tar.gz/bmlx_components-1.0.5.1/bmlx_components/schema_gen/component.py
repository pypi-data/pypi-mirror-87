""" schema generater
目前生成schema 是根据 pipeline project 中携带的 xdl.yml (或者其他的配置文件) 和
hdfs 上存放的 feature-processor.yml 全集文件 生成的。 生成逻辑
1. xdl.yml 中feature_group 字段会设置 model 使用到的所有的 slots
2. feature-processor.yml 中根据步骤1 得到的slots 去获得对应的dimension
3. xdl.yml 中的 reader.label_count 字段设置了 label size
    (xdl.DataReader 只需要知道label size 而不需要知道具体的每个label 含义)
根据以上信息，生成 schema
"""
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
from typing import Text, Optional, List
from bmlx_components.schema_gen.executor import SchemaExecutor
from bmlx_components.schema_gen.driver import SchemaGenDriver
from bmlx_components import custom_artifacts
from bmlx.execution.launcher import Launcher


class SchemaGenSpec(ComponentSpec):
    """ schema gen spec """

    PARAMETERS = {
        # model 的配置文件，一般是 xdl.yml
        "model_input_conf": ExecutionParameter(
            type=(str, Text), optional=False
        ),
    }

    INPUTS = {
        # 全集 fg.yml 的hdfs 路径
        "fg_conf": ChannelParameter(type=custom_artifacts.FgConf),
    }

    OUTPUTS = {
        "output": ChannelParameter(type=standard_artifacts.Schema),
    }


class SchemaGen(Component):
    SPEC_CLASS = SchemaGenSpec

    EXECUTOR_SPEC = ExecutorClassSpec(SchemaExecutor)

    DRIVER_SPEC = DriverClassSpec(SchemaGenDriver)

    def __init__(
        self,
        fg_conf: Channel,
        model_input_conf: Text = "xdl.yml",
        output: Text = None,
        instance_name: Optional[Text] = None,
    ):
        if not fg_conf:
            raise ValueError("empty fg_conf artifact")

        output = output or Channel(
            artifact_type=standard_artifacts.Schema,
            artifacts=[standard_artifacts.Schema()],
        )

        spec = SchemaGenSpec(
            fg_conf=fg_conf, model_input_conf=model_input_conf, output=output,
        )

        super(SchemaGen, self).__init__(spec=spec, instance_name=instance_name)

    def get_launcher_class(self, ctx):
        return Launcher
