from bmlx.utils import io_utils
import xdl
import datetime
import logging

from xdl.python.framework.session import Hook
from xdl.python.training.training_utils import get_global_step


class XdlMetricsHook(Hook):
    def __init__(
        self, ts_tensor, other_tensors, collect_interval, log_interval
    ):
        super(XdlMetricsHook, self).__init__()
        self._names = []
        self._values = []
        self._collect_interval = collect_interval
        self._log_interval = log_interval
        self._ts_tensor = ts_tensor
        self._other_tensors = []
        self._metrics = {}

        for val in xdl.get_all_metrics():
            self._names.append(val.name)
            self._values.append(val.value)
            self._metrics[val.name] = []

        for name, tensor in other_tensors:
            self._names.append(name)
            self._values.append(tensor)
            self._metrics[name] = []

    def before_run(self, v):
        return [get_global_step().value] + [self._ts_tensor] + self._values

    def after_run(self, v):
        current_step = v[0]
        current_sample_ts = sum(v[1]) / len(v[1])  # 这里对样本求的平均时间戳, 可能有更好的方法

        if xdl.get_task_index() == 0 and self._collect_interval.reached_threshold(
            current_ts=current_sample_ts, current_step=current_step
        ):
            for name, value in zip(self._names, v[2:]):
                self._metrics[name].append([current_sample_ts, value])

        if self._log_interval.reached_threshold(
            current_ts=current_sample_ts, current_step=current_step
        ):
            ts_str = ",".join(
                [
                    "%s:%s" % (name, value)
                    for name, value in zip(self._names, v[2:])
                ]
            )
            logging.info(
                "ts:%s gstep:%s sample_ts:%d\t%s"
                % (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s"),
                    current_step,
                    current_sample_ts,
                    ts_str,
                )
            )

    def end(self):
        pass
