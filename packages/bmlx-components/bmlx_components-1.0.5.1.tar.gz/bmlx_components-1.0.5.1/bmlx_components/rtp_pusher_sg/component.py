"""
相比于 xdl_pusher， 去掉了检查并发布 fg.yml的功能， 适配RTP
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
from bmlx_components.rtp_pusher_sg.executor import PusherExecutor
from bmlx.execution.launcher import Launcher


class PusherSpec(ComponentSpec):
    """ Pusher spec """

    PARAMETERS = {
        "model_name": ExecutionParameter(type=(str, Text), optional=False),
        "emb_collection": ExecutionParameter(type=(str, Text), optional=False),
        "graph_collection": ExecutionParameter(
            type=(str, Text), optional=False
        ),
        "resource_processor": ExecutionParameter(
            type=(str, Text), optional=True
        ),
        "author": ExecutionParameter(type=(str, Text), optional=False),
        "namespace": ExecutionParameter(type=(str, Text), optional=True),
        "product_namespace": ExecutionParameter(
            type=(str, Text), optional=False
        ),
        "test_env": ExecutionParameter(type=bool, optional=True),
        # 比当前时间早多少小时的数据训练出来的模型不会发布
        "skip_stale_model_hour": ExecutionParameter(type=int, optional=True),
        # 是否将发布信息送到配置中心
        "use_config_center": ExecutionParameter(type=bool, optional=True),
        # 是否发送到新加坡
        "send_sg": ExecutionParameter(type=bool, optional=True),
    }

    INPUTS = {
        "converted_model": ChannelParameter(
            type=custom_artifacts.ConvertedModel
        )
    }
    OUTPUTS = {}


class RtpPusherSg(Component):
    SPEC_CLASS = PusherSpec

    EXECUTOR_SPEC = ExecutorClassSpec(PusherExecutor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(
        self,
        converted_model: Channel,
        model_name: Text,
        emb_collection: Text,
        graph_collection: Text,
        product_namespace: Text,  # cannon 发布的namespace，业务线+"_" +应用名
        author: Optional[Text] = None,
        resource_processor: Optional[Text] = None,
        namespace: Optional[Text] = "default",
        skip_stale_model_hour: Optional[int] = 72,  # 比当前时间早多少小时的数据训练出来的模型不会发布
        test_env: bool = False,
        use_config_center: bool = False,
        instance_name: Optional[Text] = None,
        send_sg: bool = True,
    ):
        if not product_namespace:
            raise ValueError("Empty product_namespace, should be {业务线}_{应用名}")
        if not converted_model:
            raise ValueError("Empty pushed model")
        if not model_name:
            raise ValueError("Empty model name")
        if not emb_collection:
            raise ValueError("Empty emb_collection name")
        if not graph_collection:
            raise ValueError("Empty graph collection name")

        resource_processor = resource_processor or "DELIVER-V1"
        author = author or "bmlx@bigo.sg"
        spec = PusherSpec(
            converted_model=converted_model,
            model_name=model_name,
            emb_collection=emb_collection,
            graph_collection=graph_collection,
            resource_processor=resource_processor,
            author=author,
            namespace=namespace,
            product_namespace=product_namespace,
            skip_stale_model_hour=skip_stale_model_hour,
            test_env=test_env,
            use_config_center=use_config_center,
            send_sg=send_sg,
        )

        super(RtpPusherSg, self).__init__(
            spec=spec, instance_name=instance_name
        )

    def get_launcher_class(self, ctx):
        return Launcher
