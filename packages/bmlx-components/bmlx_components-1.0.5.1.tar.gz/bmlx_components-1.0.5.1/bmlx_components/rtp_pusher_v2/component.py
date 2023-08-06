"""
rtp_pusher 将embedding 数据发布到分布式cyclone服务器；rtp_pusher_v2 build 单机版本的embedding并发布到每台rtp 服务器
rtp_pusher_v2 适合小规模的模型发布使用
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
from bmlx_components import custom_artifacts
from typing import Text, Optional, List
from bmlx_components.rtp_pusher_v2.executor import PusherExecutor
from bmlx.execution.launcher import Launcher


class PusherSpec(ComponentSpec):
    """ Pusher spec """

    PARAMETERS = {
        "model_name": ExecutionParameter(type=(str, Text), optional=False),
        "product_namespace": ExecutionParameter(
            type=(str, Text), optional=False
        ),
        "embedding_build_tool_dir": ExecutionParameter(type=str, optional=True),
    }

    INPUTS = {
        "converted_model": ChannelParameter(
            type=custom_artifacts.ConvertedModel
        )
    }
    OUTPUTS = {}


class Pusher(Component):
    SPEC_CLASS = PusherSpec

    EXECUTOR_SPEC = ExecutorClassSpec(PusherExecutor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(
        self,
        converted_model: Channel,
        model_name: Text,
        product_namespace: Text,
        embedding_build_tool_dir: Text,
        instance_name: Optional[Text] = None,
    ):
        if not product_namespace:
            raise ValueError("Empty product_namespace, should be {业务线}_{应用名}")
        if not converted_model:
            raise ValueError("Empty pushed model")
        if not model_name:
            raise ValueError("Empty model name")
        if not embedding_build_tool_dir:
            raise ValueError("Empty embedding_build_tool_dir")

        spec = PusherSpec(
            converted_model=converted_model,
            model_name=model_name,
            product_namespace=product_namespace,
            embedding_build_tool_dir=embedding_build_tool_dir,
        )

        super(Pusher, self).__init__(spec=spec, instance_name=instance_name)

    def get_launcher_class(self, ctx):
        return Launcher
