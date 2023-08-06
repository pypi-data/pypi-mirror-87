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
from bmlx_components import custom_artifacts
from typing import Text, Optional, List
from bmlx_components.xdl_pusher.executor import PusherExecutor
from bmlx.execution.launcher import Launcher


class PusherSpec(ComponentSpec):
    """ Pusher spec """

    PARAMETERS = {
        "model_name": ExecutionParameter(type=(str, Text), optional=False),
        "emb_collection": ExecutionParameter(type=(str, Text), optional=False),
        "graph_collection": ExecutionParameter(
            type=(str, Text), optional=False
        ),
        "fg_collection": ExecutionParameter(type=(str, Text), optional=False),
        "fg_name": ExecutionParameter(type=(str, Text), optional=False),
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
    }

    INPUTS = {
        "converted_model": ChannelParameter(
            type=custom_artifacts.ConvertedModel
        )
    }
    # TODO: @sunkaicheng, what is this output
    OUTPUTS = {}


class Pusher(Component):
    SPEC_CLASS = PusherSpec

    EXECUTOR_SPEC = ExecutorClassSpec(PusherExecutor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(
        self,
        converted_model: Channel,
        model_name: Text,
        emb_collection: Text,
        graph_collection: Text,
        fg_collection: Text,
        fg_name: Text,
        product_namespace: Text,  # cannon 发布的namespace，业务线+"_" +应用名
        author: Optional[Text] = None,
        resource_processor: Optional[Text] = None,
        namespace: Optional[Text] = "default",
        skip_stale_model_hour: Optional[int] = 72,  # 比当前时间早多少小时的数据训练出来的模型不会发布
        test_env: bool = False,
        instance_name: Optional[Text] = None,
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
        if not fg_collection:
            raise ValueError("Empty fg collection name")
        if not fg_name:
            raise ValueError("Empty fg name")

        resource_processor = resource_processor or "DELIVER-V1"
        author = author or "bmlx@bigo.sg"
        spec = PusherSpec(
            converted_model=converted_model,
            model_name=model_name,
            emb_collection=emb_collection,
            graph_collection=graph_collection,
            fg_collection=fg_collection,
            fg_name=fg_name,
            resource_processor=resource_processor,
            author=author,
            namespace=namespace,
            product_namespace=product_namespace,
            skip_stale_model_hour=skip_stale_model_hour,
            test_env=test_env,
        )

        super(Pusher, self).__init__(spec=spec, instance_name=instance_name)

    def get_launcher_class(self, ctx):
        return Launcher
