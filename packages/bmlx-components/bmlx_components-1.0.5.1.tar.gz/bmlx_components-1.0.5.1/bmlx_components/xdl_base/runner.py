import xdl
import tensorflow as tf
import numpy as np
import random
import logging
import functools
import datetime

from typing import Dict, Text, List
from bmlx_components.proto import schema_pb2
from bmlx.flow import Artifact
from bmlx.utils import var_utils, import_utils, io_utils
from xdl.python.framework.session import Hook
from xdl.python.training.training_utils import get_global_step
from bmlx_components.xdl_base.hooks import TimelineHook, XdlMetricsHook
from bmlx_components.xdl_base.interval import Interval
from xdl.python.sparse_engine.embedding import (
    _EMBEDDING_SLOT_UPDATERS,
    _EMBEDDING_DECAY,
    _EMBEDDING_SCORE_FILTER,
    _EMBEDDING_STEP_FILTER,
    _EMBEDDING_TIMESTAMP_FILTER,
    EMBEDDING_INFOS,
)
from xdl.python.training.trace import trace_collection

SET_NOTIFY_BARRIER_SLAVE_HOOK = False


class XdlRunner(object):
    def __init__(
        self,
        model_module,
        parameters,
        schema,
        stage,
        is_training,
        is_local=False,
        model_version="",
    ):
        self._parameters = parameters
        self._schema = schema
        self._stage = stage
        self._is_training = is_training
        self._is_local = is_local
        self._model_version = model_version

        self._model = import_utils.import_class_by_path(model_module)(
            parameters, schema, stage, is_training
        )

        if not self._model:
            raise RuntimeError(
                "Failed to import model by module name %s" % model_module
            )

        if is_training and not model_version:
            raise RuntimeError("train mode must set model_version")

    @classmethod
    def get_xdl_reader(
        cls,
        name: Text,
        conf,
        schema: schema_pb2.Schema,
        input_dict: Dict[Text, List[Artifact]],
        sampling_rate: float,
    ):
        def is_valid_sample_file(file_path):
            if file_path.split("/")[-1] == "_SUCCESS":
                return False
            elif file_path.find("origin_samples") >= 0:
                return False
            elif file_path.find(".inprogress.") >= 0:
                return False
            return True

        cur_fs = None
        pathlist = []
        for sample in input_dict["samples"]:
            fs, uri = io_utils.resolve_filesystem_and_path(sample.meta.uri)
            if cur_fs is not None and type(fs) != type(cur_fs):
                raise RuntimeError(
                    "you could only passing hdfs or local file, not both!"
                )
            cur_fs = fs
            if cur_fs.isdir(uri):
                pathlist.append(uri)
            else:
                pathlist.append(sample.meta.uri)

        file_list = []
        for path in pathlist:
            if cur_fs.isdir(path):
                for f in cur_fs.ls(path):
                    if is_valid_sample_file(f):
                        file_list.append(f)
            elif is_valid_sample_file(path):
                file_list.append(path)

        # sorted 是为了保证顺序
        sampled_files = sorted(
            random.sample(
                file_list, max(1, int(len(file_list) * sampling_rate))
            )
        )
        logging.info(
            "got %s file, sampleing with rate %.4f, left files: %s"
            % (len(file_list), sampling_rate, sampled_files)
        )

        fs_type, namenode, rpath = xdl.DataReader.decode_path(sampled_files[0])

        fmt = xdl.pybind.parsers.txt
        if conf["parser"].as_str() == "pb":
            fmt = xdl.pybind.parsers.pb

        reader = xdl.DataReader(
            name,
            paths=sampled_files,
            fs_type=fs_type,
            file_type=fmt,
            enable_state=bool(conf["enable_state"]),
            global_schedule=False
            if xdl.get_run_mode() == "local"
            else conf["global_schedule"],
        )
        reader.epochs(conf["epoch"].as_number()).threads(
            conf["threads"]["packer"].as_number(),
            conf["threads"]["reader"].as_number(),
        ).batch_size(conf["batch_size"].as_number(),).label_count(
            len(schema.labels)
        )

        if conf["ztype"].as_str() == "gz":
            reader.ztype(xdl.ztypes.gz)
        elif conf["ztype"].as_str() == "zlib":
            reader.ztype(xdl.ztypes.zlib)
        elif conf["ztype"].as_str() == "pb":
            reader.ztype(xdl.ztypes.pb)

        reader.keep_skey(bool(conf["keep_skey"]))
        if conf["shuffle_file"]:
            reader.shuffle_file()
        if conf["shuffle_sample"]:
            reader.shuffle_sample()
        if conf["shuffle_queue_min_batch"].exists():
            reader.shuffle_sample_min_batch_num(
                conf["shuffle_queue_min_batch"].as_number()
            )

        for sparse_feature in schema.sparse_features:
            reader.feature(
                name=sparse_feature.name,
                type=xdl.features.sparse,
                serialized=True,
            )

        for dense_feature in schema.dense_features:
            reader.feature(
                name=dense_feature.name,
                type=xdl.features.dense,
                nvec=dense_feature.length,
            )
        reader.set_script(conf["script"].as_str())
        reader.unique_ids(bool(conf["unique_ids"]))

        if not bool(conf["enable_state"]):
            reader.startup()

        return reader

    def gen_hash_slots_update_hook(self):
        update_dict = _EMBEDDING_SLOT_UPDATERS
        hooks = []
        for k, v in update_dict.items():
            v.sort()
            slot_names = [elem.slot_name for elem in v]
            updaters = [elem.updater for elem in v]
            slot_values = [elem.slot_value for elem in v]
            hooks.append(
                xdl.HashSlotsUpdateHook(
                    var_name=k.emb_name,
                    slot_names=slot_names,
                    ids=k.unique_ids,
                    updaters=updaters,
                    slot_values=slot_values,
                )
            )
        return hooks

    def gen_global_step_filter_hook(self):
        filter_dict = _EMBEDDING_STEP_FILTER
        hooks = []
        if xdl.get_task_index() != 0:
            return hooks
        interval_dict = {}
        for name, info in filter_dict.items():
            interval = int(info["interval_steps"])
            threshold = int(info["threshold"])
            interval_dict.setdefault(interval, [[], []])
            interval_dict[interval][0].append(name)
            interval_dict[interval][1].append(threshold)
        for interval, lists in interval_dict.items():
            hooks.append(
                xdl.GlobalStepFilterHookV2(lists[0], lists[1], interval)
            )
        return hooks

    def gen_timestamp_filter_hook(self, ts_tensor):
        filter_dict = _EMBEDDING_TIMESTAMP_FILTER
        hooks = []
        if xdl.get_task_index() != 0:
            return hooks
        interval_dict = {}
        for name, info in filter_dict.items():
            interval = info["interval_hours"]
            threshold = info["threshold"]
            interval_dict.setdefault(interval, [[], []])
            interval_dict[interval][0].append(name)
            interval_dict[interval][1].append(threshold)
        for interval, lists in interval_dict.items():
            hooks.append(
                xdl.TimestampFilterHook(lists[0], lists[1], interval, ts_tensor)
            )
        return hooks

    def gen_hash_feature_decay_hook(self, ts_tensor):
        decay_dict = _EMBEDDING_DECAY
        hooks = []
        interval_dict = {}
        if xdl.get_task_index() != 0:
            return hooks
        for key, info in decay_dict.items():
            if info["decay_interval_hours"] is not None:
                interval_key = "decay_interval_hours"
            else:
                interval_key = "decay_interval_steps"
            break
        for key, info in decay_dict.items():
            emb_name = key.emb_name
            slot_name = key.slot_name
            decay_rate = info["decay_rate"]
            interval = info[interval_key]
            interval_dict.setdefault(interval, {})
            interval_dict[interval].setdefault(
                emb_name, xdl.VarDecay(emb_name, [], [])
            )
            interval_dict[interval][emb_name].slot_list.append(slot_name)
            interval_dict[interval][emb_name].decay_rate_list.append(decay_rate)
        for interval, vars in interval_dict.items():
            var_decay_list = []
            for key, var_decay in vars.items():
                var_decay_list.append(var_decay)

            if interval_key == "decay_interval_hours":
                hooks.append(
                    xdl.HashFeatureDecayHook(
                        var_decay_list,
                        interval_hours=interval,
                        ts_tensor=ts_tensor,
                    )
                )
            else:
                hooks.append(
                    xdl.HashFeatureDecayHook(
                        var_decay_list, interval_steps=interval
                    )
                )
        return hooks

    def gen_hash_feature_score_filter_hook(self, ts_tensor):
        filter_dict = _EMBEDDING_SCORE_FILTER
        hooks = []
        if xdl.get_task_index() != 0:
            return hooks
        interval_dict = {}
        for name, info in filter_dict.items():
            if info["interval_hours"] is not None:
                interval_key = "interval_hours"
            else:
                interval_key = "interval_steps"
            break
        for name, info in filter_dict.items():
            interval = info[interval_key]
            nonclk_weight = float(info["nonclk_weight"])
            clk_weight = float(info["clk_weight"])
            threshold = float(info["threshold"])
            interval_dict.setdefault(interval, [[], [], [], []])
            interval_dict[interval][0].append(name)
            interval_dict[interval][1].append(nonclk_weight)
            interval_dict[interval][2].append(clk_weight)
            interval_dict[interval][3].append(threshold)
        for interval, lists in interval_dict.items():
            if interval_key == "interval_hours":
                hooks.append(
                    xdl.HashFeatureScoreFilterHook(
                        lists[0],
                        lists[1],
                        lists[2],
                        lists[3],
                        interval_hours=interval,
                        ts_tensor=ts_tensor,
                    )
                )
            else:
                hooks.append(
                    xdl.HashFeatureScoreFilterHook(
                        lists[0],
                        lists[1],
                        lists[2],
                        lists[3],
                        interval_steps=interval,
                    )
                )
        return hooks

    def gen_hash_feature_import_filter(self):
        if self._parameters["hooks"]["hash_feature_import"].exists(
            use_default=False
        ):
            conf = self._parameters["hooks"]["hash_feature_import"]

            hooks = []
            include_vars = conf["var_list"].as_str_seq()
            exclude_vars = conf["exclude_vars"].as_str_seq()
            import_threshold = float(conf["import_threshold"].as_number())
            vars_list = var_utils.wildcard_vars(include_vars, exclude_vars)
            if len(vars_list):
                hooks.append(
                    xdl.HashFeatureImportFilterHook(
                        vars_list, import_threshold, xdl.get_task_index()
                    )
                )
            else:
                logging.warning(
                    "WARNING: HashFeatureImportFilterHook does not match any variable"
                )
            return hooks
        return []

    def gen_worker_finish_hook(self):
        finish_rate = self._parameters["min_finish_worker_rate"].as_number()
        return [
            xdl.WorkerFinishHook(
                xdl.get_task_index(), xdl.get_task_num(), finish_rate
            )
        ]

    def gen_checkpoint_hook(self, ts_tensor):
        if xdl.get_task_index() != 0:
            return []

        if self._parameters["hooks"]["checkpoint"].exists():
            conf = self._parameters["hooks"]["checkpoint"]
            interval_steps = conf["interval_steps"].as_number()
            interval_hours = conf["interval_hours"].as_number()

            if bool(conf["sync_before_save"]):
                return [
                    xdl.CheckpointHook(
                        index=xdl.get_task_index(),
                        worker_count=xdl.get_task_num(),
                        finish_rate=self._parameters[
                            "min_finish_worker_rate"
                        ].as_number(),
                        interval_steps=interval_steps,
                        interval_hours=interval_hours,
                        ts_tensor=ts_tensor,
                        end_version=self._model_version,
                    )
                ]
            else:
                return [
                    xdl.CheckpointHook(
                        interval_steps=interval_steps,
                        interval_hours=interval_hours,
                        ts_tensor=ts_tensor,
                        end_version=self._model_version,
                    )
                ]
        else:
            return []

    def gen_notify_barrier_slave_hook(self):
        if xdl.get_task_index() != 0:
            return [
                xdl.NotifyBarrierSlaveHook(
                    xdl.get_task_index(), xdl.get_task_num()
                )
            ]
        else:
            return []

    def gen_vars_sync_hook(self, ts_tensor):
        if self._parameters["hooks"]["var_sync"].exists(use_default=False):
            finish_rate = self._parameters["min_finish_worker_rate"].as_number()
            conf = self._parameters["hooks"]["var_sync"]
            interval_steps = conf["interval_steps"].as_number()
            interval_hours = conf["interval_hours"].as_number()
            rules = conf["rules"].as_str()
            index = xdl.get_task_index()
            worker_count = xdl.get_task_num()

            if index != 0:
                return []
            else:
                return [
                    xdl.VariableSyncChiefHook(
                        rules=rules,
                        index=index,
                        worker_count=worker_count,
                        finish_rate=finish_rate,
                        interval_steps=interval_steps,
                        interval_hours=interval_hours,
                        ts_tensor=ts_tensor,
                    )
                ]
        else:
            return []

    def gen_metrics_hook(self, ts_tensor, additional_metrics=[]):
        log_interval = Interval.create_interval(
            time=self._parameters["log_interval"].as_number()
        )
        collect_interval = Interval.create_interval(
            time=self._parameters["metrics_interval"].as_number()
        )
        return [
            XdlMetricsHook(
                ts_tensor=ts_tensor,
                other_tensors=additional_metrics,
                collect_interval=collect_interval,
                log_interval=log_interval,
            )
        ]

    def timeline_hook(self):
        if self._parameters["hooks"]["timeline"].exists(use_default=False):
            hook_config = self._parameters["hooks"]["timeline"]
            interval = hook_config["interval"].as_number()
            worker_list = hook_config["worker_list"].as_str_seq()
            total_count = hook_config["total_count"].as_number()
            output_dir = hook_config["output_dir"].as_filename(
                relative_to="artifacts"
            )

            if str(xdl.get_task_index()) in worker_list:
                return TimelineHook(interval, total_count, output_dir)
        return None

    def gen_trace_hook(self):
        if self._parameters["hooks"]["trace"].exists(use_default=False):
            hc = self._parameters["hooks"]["trace"]
            c = {
                "output_dir": hc["output_dir"].as_str(),
                "max_file_m_size": hc["max_file_m_size"].as_number(),
                "output_file_name": hc["output_file_name"].as_str(),
                "log_type": hc["format"].as_str("pb"),
            }
            scope_list = []
            from xdl.python.backend.model_scope import get_model_scopes

            for scope in list(get_model_scopes()):
                if scope and not scope.startswith("tf_export_graph_scope"):
                    scope_list.append(scope)
            # 默认trace embedding 信息，embedding trace 帮助排查得分不一致原因
            xdl.trace_collection(EMBEDDING_INFOS, scope="")

            logging.info("trace generated to %s, scopes: %s", c, scope_list)
            return [
                xdl.TraceHook(
                    c, is_training=self._is_training, scope=scope_list
                )
            ]
        return []

    def run(self, reader: xdl.DataReader):
        batch = reader.read()

        log_str = "gstep: [{0}], timestamp: [{1}]"
        global_step = get_global_step().value
        timestamp, _ = xdl.split(
            batch["_timestamp"],
            np.array(
                [
                    1,
                    self._parameters["reader"]["batch_size"].as_number(1024)
                    - 1,
                ]
            ),
            0,
            2,
        )
        log_tensors = [global_step, timestamp]

        train_ops = []
        hooks = []
        metric_tensors = []

        first_global_optimizer = True
        logging.info("xdl begin with phase %s" % self._parameters["phases"])
        for phase in range(self._parameters["phases"].as_number(2)):
            with xdl.model_scope("phase%s" % phase):
                ret = self._model.process(batch=batch, phase=phase,)

                for name, tensor in ret.tensor_map.items():
                    metric_tensors.append(
                        ("phase%s_%s" % (phase, name), tensor)
                    )
                    log_str += ", p%d_%s:{%d}" % (phase, name, len(log_tensors))
                    log_tensors.append(tensor)

                if ret.additional_hooks:
                    hooks.extend(ret.additional_hooks)

                if self._is_training:
                    # append optimizers
                    optimizer = self._model.get_optimizer()
                    optvar = optimizer.optimize(
                        update_global_step=first_global_optimizer
                    )
                    first_global_optimizer = False
                    train_ops.append(optvar)

                    # update xdl ops
                    update_ops = xdl.get_collection(xdl.UPDATE_OPS)
                    if update_ops is not None:
                        train_ops.extend(update_ops)

        # add log hooks
        hooks.append(
            xdl.LoggerHook(
                log_tensors[:],
                log_str,
                interval=self._parameters["log_interval"].as_number(),
            )
        )

        ts_tensor = batch["_timestamp"]
        if not self._is_local:
            hooks.extend(self.gen_worker_finish_hook())

        if self._is_training:
            hooks.extend(self.gen_hash_slots_update_hook())
            hooks.extend(self.gen_checkpoint_hook(ts_tensor))
            hooks.extend(self.gen_vars_sync_hook(ts_tensor))
            hooks.extend(self.gen_notify_barrier_slave_hook())
            hooks.extend(self.gen_global_step_filter_hook())
            hooks.extend(self.gen_timestamp_filter_hook(ts_tensor))
            hooks.extend(self.gen_hash_feature_decay_hook(ts_tensor))
            hooks.extend(self.gen_hash_feature_score_filter_hook(ts_tensor))

        if self._stage in ("predict" "train", "eval"):
            hooks.extend(self.gen_trace_hook())

        hooks.extend(
            self.gen_metrics_hook(ts_tensor, additional_metrics=metric_tensors,)
        )

        timeline_hook = self.timeline_hook()
        if timeline_hook:
            hooks.append(timeline_hook)

        sess = xdl.TrainSession(hooks=hooks)
        while not sess.should_stop():
            if timeline_hook:
                run_option = timeline_hook.run_option()
                run_option.timeout_second = self._parameters[
                    "timeout"
                ].as_number()
                sess.run(
                    train_ops,
                    run_option=run_option,
                    run_statistic=timeline_hook.run_statistic(),
                )
            else:
                run_option = xdl.RunOption()
                run_option.timeout_second = self._parameters[
                    "timeout"
                ].as_number()
                sess.run(train_ops, run_option=run_option)
