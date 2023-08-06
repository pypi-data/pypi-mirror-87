import logging
import xdl
import datetime
from xdl.python.framework.session import Hook
from xdl.python.training.training_utils import (
    get_global_step,
    get_global_floor_interval,
)
from xdl.python.lib.graph import execute
from bmlx.utils import io_utils


# 临时使用，和老流程打平，之后metrics server ready之后替换掉
class SaveMetricsHook(Hook):
    def __init__(
        self,
        metrics,
        output_file_path,
        interval_steps,
        interval_hours=0,
        need_clear=False,
        ts_tensor=None,
    ):
        super(SaveMetricsHook, self).__init__()
        self._names = []
        self._values = []
        self._clear_ops = []
        self.value_res = []
        for val in metrics:
            self._names.append(val.name)
            self._values.append(val.value)
            self._clear_ops.append(val.clear_ops)

        self._last_run = 0

        assert interval_steps or interval_hours
        if interval_steps:
            self._mark = get_global_step().value
            self._interval = interval_steps
            self._floor_interval = 1
            self._use_step = True
        else:
            self._mark = ts_tensor
            self._interval = int(float(interval_hours) * 60 * 60)
            self._floor_interval = get_global_floor_interval()
            self._use_step = False

        self.mark_value = 0

        self._need_clear = need_clear

        if not output_file_path.startswith("hdfs://"):
            raise ValueError(
                "only support hdfs metric path now, but have output_file_path %s",
                output_file_path,
            )

        self._writer, uri = io_utils.resolve_filesystem_and_path(
            output_file_path
        )

        self._app_id = xdl.get_app_id()
        if self._app_id is None:
            self._app_id = "xdl-xxx"
        self.value_res = None

    def before_run(self, v):
        return [self._mark] + self._values

    def after_run(self, v):
        self.mark_value = v[0] if isinstance(v, list) else v
        self.mark_value = self.mark_value.flatten()[0]
        self.mark_value = (
            self.mark_value // self._floor_interval * self._floor_interval
        )
        self.value_res = v[1:]

        if self._last_run == 0:
            self._last_run = self.mark_value
        if self.mark_value - self._last_run > self._interval:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mark_str = (
                ("gstep" if self._use_step else "timestamp")
                + ":"
                + str(self.mark_value)
            )
            index_str = "|".join(
                [
                    "{}:{}".format(k, v)
                    for k, v in zip(self._names, self.value_res)
                ]
            )
            content = "{} metrics {}|{}".format(date_str, mark_str, index_str)
            logging.info(content)
            if self._writer is not None:
                self._writer.write(content, len(content))
            if self._need_clear:
                execute(self._clear_ops)
            self._last_run = self.mark_value

    def end(self):
        if not self.value_res:
            return
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mark_str = (
            ("gstep" if self._use_step else "timestamp")
            + ":"
            + str(self.mark_value)
        )
        if len(self._names) != len(self.value_res):
            logging.info("worker 0 never run!")
            return
        index_str = "|".join(
            ["{}:{}".format(k, v) for k, v in zip(self._names, self.value_res)]
        )

        content = "{} metrics {}|{}".format(date_str, mark_str, index_str)

        logging.info(
            "=======================save metrics in the end==================="
        )
        logging.info(content)

        if self._writer is not None:
            self._writer.write(content, len(content))
