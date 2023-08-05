"""bmlx xdl base executor."""
import os
import logging
import re
import socket
import functools
import abc
from typing import Any, Dict, List, Text, Tuple

from bmlx.config import Configuration
from bmlx.flow import Executor, Artifact
from bmlx.utils import import_utils, artifact_utils, io_utils
from bmlx_components.proto import schema_pb2


MY_DIR = os.path.dirname(os.path.realpath(__file__))


class XdlExecutor(Executor):
    __slots__ = []

    def _resolve_schema(self, schema_artifact) -> schema_pb2.Schema:
        # 获取schema信息
        schema_uri = io_utils.get_only_uri_in_dir(
            artifact_utils.get_single_uri(schema_artifact)
        )
        return io_utils.parse_pbtxt_file(schema_uri, schema_pb2.Schema())

    def _resolve_latest_sample_meta(
        self, samples_artifacts
    ) -> Tuple[Text, Text]:
        # 最新的样本
        latest_sample_uri = max(
            samples_artifacts, key=lambda x: x.meta.uri
        ).meta.uri

        # 目前机制，限制输出必须为YYYYMMDD/HH的格式，之后再fix这个限制 TODO by zhangguanxing@bigo.sg
        if re.match(r".*\/[0-9]{8}\/[0-9]{2}$", latest_sample_uri):
            latest_sample_hour = latest_sample_uri[-11:]
        elif re.match(r".*\/[0-9]{8}$", latest_sample_uri):
            latest_sample_hour = latest_sample_uri[-8:]
        else:
            raise RuntimeError(
                "last_sample_uri %s does not match valid pattern %s or %s",
                latest_sample_uri,
                r".*\/[0-9]{8}\/[0-9]{2}$",
                r".*\/[0-9]{8}$",
            )

        return (latest_sample_uri, latest_sample_hour)

    def init_worker_env(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        try:
            import xdl.python.training.env as xdl_env
            from xdl.python.utils.config import parse_from_raw
        except ImportError:
            raise RuntimeError("please run bmlx in docker_env with xdl env")
        is_local = exec_properties["is_local"]
        if is_local:
            args = [
                "--run_mode",
                "local",
                "--model_bank",
                exec_properties["model_bank"],
                "--ckpt_dir",
                exec_properties["ckpt"],
            ]
        else:
            args = [
                "--run_mode",
                "dist",
                "--task_name",
                "worker",
                "--zk_addr",
                exec_properties["zk_addr"],
                "--app_id",
                exec_properties["job_id"],
                "--task_num",
                str(exec_properties["task_num"]),
                "--task_index",
                str(exec_properties["task_index"]),
                "--model_bank",
                exec_properties["model_bank"],
                "--ckpt_dir",
                exec_properties["ckpt"],
            ]

        if exec_properties["stage"] == "convert":
            args.extend(["--ps_mode", False])
        parse_from_raw(args)

        logging.info("startup commands is %s" % args)
        xdl_env.init_env()

    def init_ps_or_scheduler_env(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ) -> None:
        try:
            import xdl.python.training.env as xdl_env
            from xdl.python.utils.config import parse_from_raw
        except ImportError:
            raise RuntimeError("please run bmlx in docker_env with xdl env")

        parse_from_raw(
            [
                "--run_mode",
                "dist",
                "--task_name",
                exec_properties["cluster_role"],
                "--zk_addr",
                exec_properties["zk_addr"],
                "--app_id",
                exec_properties["job_id"],
                "--task_num",
                str(exec_properties["task_num"]),
                "--task_index",
                str(exec_properties["task_index"]),
                "--ps_num",
                str(exec_properties["ps_num"]),
                "--ps_memory_m",
                exec_properties["ps_memory_m"],
                "--ps_cpu_cores",
                exec_properties["ps_cpu_cores"],
                "--model_bank",
                exec_properties["model_bank"],
                "--ckpt_dir",
                exec_properties["ckpt"],
            ]
        )

        xdl_env.init_env()

    def execute(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        self._log_startup(input_dict, output_dict, exec_properties)
        logging.info(
            "running xdl in host : %s",
            socket.gethostbyname(socket.gethostname()),
        )

        cluster_role = exec_properties["cluster_role"]
        if cluster_role in ("worker_master", "worker_slave"):
            self.init_worker_env(input_dict, output_dict, exec_properties)
            self.modify_xdl_config(exec_properties)
            self.execute_as_worker(input_dict, output_dict, exec_properties)
        elif cluster_role in ("scheduler", "ps"):
            self.init_ps_or_scheduler_env(
                input_dict, output_dict, exec_properties
            )
            self.execute_as_ps_or_scheduler(
                input_dict, output_dict, exec_properties
            )
        else:
            raise RuntimeError("Invalid cluster role %s" % cluster_role)

    def modify_xdl_config(self, exec_properties: Dict[Text, Any]):
        """
        运行时修改xdl.yml 文件，通过xdl.yml 配置文件传递信息给一些 无法从提交命令行获知信息 的地方。比如:
        xdl 的convert 脚本需要获知 stage 信息从而针对train和predict 有不同的处理，而xdl IOAnt 没法获得stage信息也就无法传递给 用户态的convert 脚本。
        convert 脚本会读取 xdl.yml 配置文件，于是，这里在执行xdl worker/ps/sc 等角色之前，修改 xdl.yml 来传递相应信息.
        """
        # 注意这里的配置文件不一定使用 xdl.yml 。但是，我这里想偷懒，等重构版本的launcher merge之后，再从 bmlx.yml中获得使用的配置文件
        # TODO: @sunkaicheng
        import yaml

        with open("./xdl.yml", "r") as fr:
            xdl_dct = yaml.load(fr, yaml.Loader)

        xdl_dct["stage"] = exec_properties["stage"]
        with open("./xdl.yml", "w") as fw:
            yaml.dump(xdl_dct, fw)
        logging.info("final xdl.yml content: %s", xdl_dct)

    """
    worker的执行，在不同的阶段，worker的初始化和执行逻辑不同，子类主要设置
    1. exec_properties["model_bank"], exec_properties["ckpt"]
    """

    @abc.abstractmethod
    def execute_as_worker(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        raise NotImplementedError()

    @abc.abstractmethod
    def execute_as_ps_or_scheduler(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        raise NotImplementedError()
