import logging
import copy
import re
import os
import abc
import kubernetes as k8s
import kazoo
from kazoo.client import KazooClient

from bmlx.execution.launcher import Launcher
from bmlx.execution.execution import ExecutionInfo
from bmlx_components.xdl_base.volcano_job_desc import VolcanoJobDescRender
from bmlx_components.xdl_base.executor import XdlExecutor
from kubernetes.client.rest import ApiException
from typing import Text, Tuple
from bmlx.utils import proc_utils, artifact_utils, io_utils, json_utils
from functools import partial
from bmlx.proto.metadata import execution_pb2
from bmlx.config import Configuration


MY_DIR = os.path.dirname(os.path.realpath(__file__))

"""
XDL launcher主要是针对不同的运行需求，启动不同JOB，目前主要包括两个
1. Distribute mode. 这里主要是向k8s发起启动命令。
    bmlx_submitter  -> watcher  -> (ink8s)  scheduler
                                -> (ink8s)  worker
                                -> (ink8s)  parameter server
    在这种运行模式下，会多次运行launcher的代码，通过cluster_role参数，在一次k8s执行中，launcher会有四种角色(watcher, scheduler, ps, worker[master-slave])
2. Local Mode, 本地模式实际上就是启动了xdl的local mode，同时在本地启动ps, worker的角色
"""


class XdlLauncher(Launcher):
    __slots__ = []

    """
    子类需要提供ckpt和modelbank计算逻辑
    """

    @abc.abstractmethod
    def _resolve_model_paths(
        self, input_dict, exec_properties
    ) -> Tuple[Text, Text]:
        raise NotImplementedError("please not use 'XdlLauncher' directly ")

    @abc.abstractmethod
    def _need_launch_xdl(self, input_dict, exec_properties) -> bool:
        raise NotImplementedError("please not use 'XdlLauncher' directly ")

    def _run_as_watcher(self):
        execution_info = self.run_driver()
        self._exec_properties = execution_info.exec_properties
        self.register_component_execution(input_dict=execution_info.input_dict)

        state = execution_pb2.ComponentExecution.State.RUNNING
        if execution_info.use_cached_result:
            logging.info("component %s use cached result", self._component.id)
            state = execution_pb2.ComponentExecution.State.CACHED
        else:
            watcher_status_2_execution_state = {
                proc_utils.PollWaitStatus.SUCC: execution_pb2.ComponentExecution.State.COMPLETED,
                proc_utils.PollWaitStatus.FAIL: execution_pb2.ComponentExecution.State.FAILED,
                proc_utils.PollWaitStatus.CANCEL: execution_pb2.ComponentExecution.State.CANCELED,
                proc_utils.PollWaitStatus.TIMEOUT: execution_pb2.ComponentExecution.State.FAILED,
            }

            logging.info("execute %s", self._component.id)
            if self._need_launch_xdl(
                execution_info.input_dict, self._exec_properties
            ):
                # wait until all pods finished
                watcher_status = self._launch_k8s_watcher(execution_info)
                state = watcher_status_2_execution_state[watcher_status]
            else:
                logging.info("does not need to launch xdl job")
                state = execution_pb2.ComponentExecution.State.COMPLETED
        # persist result
        self.publish_component_execution(
            execution_info=execution_info, state=state
        )

    # 修改launch volcano job时候的参数，比如 xdl-predict中，将 worker instance设置为1
    def _rewrite_launch_config(self, exec_properties):
        pass

    def _launch_k8s_watcher(self, execution_info: ExecutionInfo):
        (core_api, custom_obj_api) = self._init_api()

        self._rewrite_launch_config(self._exec_properties)

        namespace = self._exec_properties["namespace"]
        if not self._resolve_namespace(core_api, namespace):
            raise RuntimeError("Failed to prepare namespace %s" % namespace)

        self._create_job(custom_obj_api, execution_info)

        def _check_job_status(self):
            try:
                resource = custom_obj_api.get_namespaced_custom_object(
                    group="batch.volcano.sh",
                    version="v1alpha1",
                    plural="jobs",
                    namespace=self._exec_properties["namespace"],
                    name=self._job_id,
                )
                try:
                    status_desc = resource["status"]["state"]["phase"]
                    logging.info(
                        "job %s in %s state" % (self._job_id, status_desc)
                    )
                    if "Failed" == status_desc:
                        raise proc_utils.UnexpectedErrorException()
                    elif "Completed" == status_desc:
                        logging.info("job %s completed" % self._job_id)
                        return True
                    else:
                        return False
                except KeyError as e:
                    logging.warning(
                        "unexpect response from server, except: %s, resource content: %s"
                        % (e, resource)
                    )
                    # 这里raise exception， 目的是为了尽快clean up ，避免影响 xdl 集群
                    # raise proc_utils.UnexpectedErrorException()

            except ApiException as e:
                if str(e.status) == "404":
                    logging.info(
                        "record was deleted by someone else, we choose to return"
                    )
                    raise RuntimeError("external deleted")
                logging.exception("call k8s error")
                return False

        timeout = self._exec_properties["runtime_configs"][
            "timeout"
        ].as_number()
        logging.info(
            "launched xdl jobs, we start to polling it's status, timeout: %s"
            % timeout
        )

        return proc_utils.poll_wait_until(
            check_end=partial(_check_job_status, self),
            cleanup=partial(self._cleanup_k8s_watcher, custom_obj_api),
            timeout=timeout,
            poll_period=12,
        )

    def _cleanup_k8s_watcher(
        self, custom_object_api, ret=False, exec_info=None, throwError=True,
    ):
        @proc_utils.retry(3, allowed_exceptions=(ApiException))
        def remove_job(namespace, job_id):
            try:
                custom_object_api.delete_namespaced_custom_object(
                    group="batch.volcano.sh",
                    version="v1alpha1",
                    plural="jobs",
                    namespace=namespace,
                    name=job_id,
                    body=k8s.client.V1DeleteOptions(),
                )
                logging.info("cleanup job %s" % job_id)
            except ApiException as e:
                if str(e.status) == "404":
                    logging.info("record was deleted already")

        def remove_zk_key():
            zk = KazooClient(
                hosts=",".join(
                    self._exec_properties["runtime_configs"][
                        "zk_addr"
                    ].as_str_seq()
                )
            )
            zk.start()
            try:
                zk.delete(f"/mlplat/bmlx/xdl-k8s/ps/{self._job_id}")
            except kazoo.exceptions.NoNodeError:
                pass

        logging.info("cleanup received: %s %s" % (ret, exec_info))
        if exec_info:
            logging.warn("run %s error: %s" % (self._job_id, exec_info))
        else:
            if ret:
                logging.info("job %s success" % self._job_id)
            else:
                logging.warning("job %s failed" % self._job_id)

        logging.info("remove job %s" % self._job_id)

        remove_job(
            namespace=self._exec_properties["namespace"], job_id=self._job_id,
        )

        remove_zk_key()

        if not ret or exec_info:
            if throwError:
                raise RuntimeError("run component error: %s" % exec_info)
            else:
                logging.warning(
                    "run component error, ret：%d, exec info: %s", ret, exec_info
                )
                return f"run component error, ret：{ret}, exec info: {exec_info}"
        return "success"

    def _run_in_cluster(self):
        cluster_role = self._exec_properties["cluster_role"]

        # 给xdl 各个pod 分配 task_index
        vk_role_index = int(os.environ["HOSTNAME"].split("-")[-1])
        self._exec_properties["task_index"] = (
            vk_role_index
            if cluster_role != "worker_slave"
            else vk_role_index + 1
        )

        assert cluster_role in (
            "scheduler",
            "ps",
            "worker_master",
            "worker_slave",
        )

        # 在dist 模式下，execution_info 从 exec_properties 中获得。
        # 因为在dist 模式下，xdl 会分散出很多节点。 为了避免所有节点都再次从metaserver
        # 获取一次 input_artifacts 信息(在 run_driver阶段)，所以将 execution_info
        # 放在xdl任务提交命令行中.
        execution_info = json_utils.loads(
            self._exec_properties["execution_info"]
        )
        self._exec_properties.update(execution_info.exec_properties)
        self._exec_properties.update(
            {
                "is_local": False,
                "zk_addr": self._zk_addr(),
                "app_id": self._job_id,
            }
        )
        model_bank, ckpt = self._resolve_model_paths(
            input_dict=execution_info.input_dict,
            exec_properties=self._exec_properties,
        )

        self._exec_properties.update(
            {"model_bank": model_bank, "ckpt": ckpt,}
        )

        # convert does not need ps and scheduler
        if self._exec_properties["stage"] != "convert":
            self._exec_properties.update(
                {
                    "ps_num": str(
                        self._exec_properties["runtime_configs"]["resources"][
                            "ps"
                        ]["instances"].as_number()
                    ),
                    "ps_memory_m": "%.f"
                    % self._exec_properties["runtime_configs"]["resources"][
                        "ps"
                    ]["memory"]
                    .as_sunit()
                    .to_mega_i(),
                    "ps_cpu_cores": str(
                        self._exec_properties["runtime_configs"]["resources"][
                            "ps"
                        ]["cpu"].as_number()
                    ),
                }
            )

        super(XdlLauncher, self).run_executor(
            execution_info.input_dict,
            execution_info.output_dict,
            self._exec_properties,
        )

    def _run_local_worker(self):
        execution_info = super(XdlLauncher, self).run_driver()
        self._exec_properties = copy.deepcopy(execution_info.exec_properties)
        self.register_component_execution(input_dict=execution_info.input_dict)

        self._exec_properties.update(
            {"is_local": True, "cluster_role": "worker_master",}
        )
        model_bank, ckpt = self._resolve_model_paths(
            input_dict=execution_info.input_dict,
            exec_properties=self._exec_properties,
        )

        self._exec_properties.update(
            {"model_bank": model_bank, "ckpt": ckpt,}
        )

        logging.info(
            "run local worker, ckdir: [%s], model_bank: [%s]"
            % (ckpt, model_bank)
        )
        super(XdlLauncher, self).run_executor(
            execution_info.input_dict,
            execution_info.output_dict,
            self._exec_properties,
        )

        state = execution_pb2.ComponentExecution.State.COMPLETED
        self.publish_component_execution(
            execution_info=execution_info, state=state
        )

    def _get_model_bank_uri(self, model_uri, model_file_pattern):
        # get model bank infos
        # xdl的model bank传参格式为 {regex}@{uri}, 比较奇怪，这里暂时兼容格式，之后有时间再改
        regex_str = ",".join(
            ["re#%s" % file_pattern for file_pattern in model_file_pattern]
        )

        model_bank_format = "{regex}@{uri}"
        fs, path = io_utils.resolve_filesystem_and_path(model_uri)
        if not fs.exists(path):
            raise RuntimeError(
                "resolved model uri %s does not exist!" % model_uri
            )

        logging.info("get_model_bank: resolved model uri %s", model_uri)
        if not re.match(
            r"^hdfs:\/\/[0-9a-zA-Z-_\.,\/]+\/[0-9]{8}\/[0-9]{2}\/?$", model_uri
        ) and not re.match(
            r"^hdfs:\/\/[0-9a-zA-Z-_\.,\/]+\/[0-9]{8}\/?$", model_uri
        ):
            raise ValueError("invalid model uri %s", model_uri)

        return model_bank_format.format(regex=regex_str, uri=model_uri)

    def launch(self):
        # 用户xdl的配置文件位置
        param_view = self._exec_properties["runtime_configs"]["parameters"]
        user_config = []
        if param_view.exists():
            user_config = param_view.as_filename(relative_to="project")

            # xdl_base 级别的配置
            self._exec_properties["parameters"] = Configuration(
                os.path.join(MY_DIR, "default.yml"), user_config,
            )

        if "job_id" in self._exec_properties:
            # get job_id from exec_properties in 'execute' stage
            self._job_id = self._exec_properties["job_id"]
        else:
            # generate job_id by other infos in 'submit' stage
            # job id and task index are required for distributed xdl running
            self._job_id = (
                "bmlx-%s-%s-%s"
                % (
                    self._pipeline.meta.name.replace("_", "-"),
                    self._component.id.replace("_", "-"),
                    str(self._driver_args.pipeline_execution.context_id)[:8],
                )
            ).lower()

        self._exec_properties["stage"] = self._component.stage()

        if not self._ctx.local_mode:
            if "cluster_role" not in self._exec_properties:
                # this means we are in emit stage
                self._run_as_watcher()
            else:
                self._run_in_cluster()
        else:
            self._run_local_worker()

    def cleanup(self, component_execution_state):
        if (
            component_execution_state
            == execution_pb2.ComponentExecution.State.COMPLETED
            or component_execution_state
            == execution_pb2.ComponentExecution.State.UNKNOWN
        ):
            return "ignore"

        self._job_id = "bmlx-%s-%s-%s" % (
            self._pipeline.meta.name,
            self._component.id.replace("_", "-"),
            str(self._driver_args.pipeline_execution.context_id)[:8],
        )

        _, custom_obj_api = self._init_api()
        return self._cleanup_k8s_watcher(
            custom_obj_api, False, "cleaned up", False
        )

    def _init_api(self):
        """
        初始化k8s api, 主要为了提交volcano jobs
        """
        try:
            k8s_context = self._exec_properties["runtime_configs"][
                "k8s_context"
            ].as_str()
            k8s.config.load_kube_config(context=k8s_context)
        except Exception as e:
            logging.error(
                "loading kubeconfig error!, please check you kube env: %s" % e
            )
            raise RuntimeError()

        core_api = k8s.client.CoreV1Api()
        custom_obj_api = k8s.client.CustomObjectsApi()
        return (core_api, custom_obj_api)

    @proc_utils.retry(retry_count=3, delay=5, allowed_exceptions=(ApiException))
    def _create_job(self, custom_object_api, execution_info) -> None:
        def command_generator(**kwargs):
            cmd = self._ctx.generate_component_run_command(
                component_id=self._component.id,
                collect_log=True,
                execution_name=self._driver_args.pipeline_execution.name,
                extra=kwargs,
                sub_component=True,
            )

            return cmd

        namespace = self._exec_properties["namespace"]

        render = VolcanoJobDescRender(
            namespace=namespace,
            image=self._ctx.image(),
            runtime_configs=self._exec_properties["runtime_configs"],
            job_name=self._job_id,
            execution_info=json_utils.dumps(execution_info),
            command_generator=command_generator,
            dns_policy=self._ctx.dnsPolicy(),
            dns_config=self._ctx.dnsConfig(),
            labels=self._job_labels(),
        )
        custom_object_api.create_namespaced_custom_object(
            group="batch.volcano.sh",
            version="v1alpha1",
            namespace=namespace,
            plural="jobs",
            body=render.spec(stage=self._exec_properties["stage"]),
        )

        logging.info("xdl train k8s job %s submitted" % self._job_id)

    def _zk_addr(self) -> Text:
        return "zfs://%s/mlplat/bmlx/xdl-k8s/ps/%s" % (
            ",".join(
                self._exec_properties["runtime_configs"]["zk_addr"].as_str_seq()
            ),
            self._job_id,
        )

    def _job_labels(self):
        """
        k8s的labels，这些labels会被volcano inject到各个pods里面。promethues和日志收集器会根据这些label，去追踪此次执行
        所以如果删除这些labels，需要确认
        1. promethues没有依赖
        2. logcollector没有依赖
        3. api-service等服务没有依赖
        所以更改这些labels请务必小心
        """
        return {
            "bmlx_experiment": self._ctx.experiment,
            "bmlx_pipeline": self._pipeline.meta.name,
            "bmlx_pipeline_version": self._ctx.checksum,
            "bmlx_pipeline_exe_id": self._driver_args.pipeline_execution.id,
            "bmlx_component": self._component.id,
            "bmlx_workflow_id": self._ctx.workflow_id,
        }

    def _resolve_namespace(self, core_api, ns_name):
        try:
            ns_list = core_api.list_namespace()
        except ApiException as e:
            logging.error("Failed to list namespace, error: %s", e)
            return False

        for ns in ns_list.items:
            if ns.metadata.name == ns_name:
                return True

        try:
            body = k8s.client.V1Namespace(
                metadata=k8s.client.V1ObjectMeta(name=ns_name)
            )
            core_api.create_namespace(body)
            return True
        except ApiException as e:
            logging.error("Failed to create namespace, error: %s", e)
            return False
