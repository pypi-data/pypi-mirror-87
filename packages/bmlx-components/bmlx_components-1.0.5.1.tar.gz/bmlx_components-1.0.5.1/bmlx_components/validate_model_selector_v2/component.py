from bmlx_components.validate_model_selector_v2.driver import (
    ModelSelectorDriver,
)
from bmlx.flow import Node, Artifact, Channel
from bmlx.flow.driver_spec import DriverClassSpec
from typing import Union, List, Text, Type, Optional, Dict, Any
from bmlx.metadata import standard_artifacts
from bmlx_components import custom_artifacts


class ModelSelector(Node):
    DRIVER_SPEC = DriverClassSpec(ModelSelectorDriver)

    def __init__(
        self,
        instance_name,
        namespace: Text,
        model_name: Text,
        min_serve_minutes: int = 15,  # 模型至少serve 15min
    ):
        """
        SampleSelector 会查询guardian，找出来当前线上正在使用的模型信息。
        通过模型信息，得到模型在hdfs上的路径
        """
        assert namespace and model_name

        self._namespace = namespace
        self._model_name = model_name
        self._min_serve_minutes = min_serve_minutes

        self._output_dict = {
            "model": Channel(
                artifact_type=standard_artifacts.Model,
                artifacts=[standard_artifacts.Model()],
            ),
            "pushed_model": Channel(
                artifact_type=custom_artifacts.PushedModel,
                artifacts=[custom_artifacts.PushedModel()],
            ),
        }
        super(ModelSelector, self).__init__(instance_name=instance_name)

    def __repr__(self):
        return "ModelSelector: name:%s namespace:%s, model_name: %s" % (
            self._instance_name,
            self._namespace,
            self._model_name,
        )

    def to_json_dict(self) -> Dict[Text, Any]:
        return {
            "instance_name": self._instance_name,
            "output_dict": self._output_dict,
            "driver_spec": self.driver_spec,
            "executor_spec": self.executor_spec,
            "namespace": self._namespace,
            "model_name": self._model_name,
            "min_serve_minutes": self._min_serve_minutes,
        }

    @property
    def inputs(self) -> Dict[str, Channel]:
        return {}

    @property
    def outputs(self) -> Dict[str, Channel]:
        return self._output_dict

    @property
    def exec_properties(self) -> Dict[Text, Any]:
        return {
            "namespace": self._namespace,
            "model_name": self._model_name,
            "min_serve_minutes": self._min_serve_minutes,
        }
