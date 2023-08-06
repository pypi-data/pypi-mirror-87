import os
import logging
from bmlx.utils import artifact_utils, io_utils
from bmlx_components.proto import model_pb2
from bmlx_components.xdl_base.driver import XdlDriver


class XdlPredictorDriver(XdlDriver):
    # override super method
    def _rewrite_launch_config(self, exec_properties):
        # 如果需要保持顺序，只保留一个worker instance，且设置batch size = 1 (在 executor.py中设置)
        if exec_properties["keep_order"]:
            self._exec_properties["runtime_configs"].set_args(
                {"resources.worker.instances": 1}
            )
            
    def _resolve_model_uri(self, model_meta_path):
        model_pb = io_utils.parse_pbtxt_file(model_meta_path, model_pb2.Model())
        if not (model_pb and model_pb.model_path):
            raise RuntimeError(
                "invalid model meta info parsed from %s" % model_meta_path
            )
        logging.info("parsed model meta info: %s", model_pb)

        return os.path.join(model_pb.model_path, model_pb.model_version)

    def _resolve_model_paths(self, input_dict, exec_properties):
        model_uri = ""
        if "model" in input_dict:
            # TODO @sunkaicheng: 这块 uri的管理有点乱，需要重构
            if len(input_dict["model"]) > 0:
                # 使用 input-dcit 传入的uri，可能是meta 信息 （比如train之后的结果）
                model_uri = artifact_utils.get_single_uri(input_dict["model"])
                # 通过bmlx的 meta 文件获取model uri
                if io_utils.exists(os.path.join(model_uri, "model.pbtxt")):
                    model_uri = self._resolve_model_uri(
                        os.path.join(model_uri, "model.pbtxt")
                    )

        if not model_uri:
            raise RuntimeError("predictor must have model input")

        model_bank_uri = self._get_model_bank_uri(
            model_uri, exec_properties["model_file_pattern"]
        )
        # eval 阶段内存优化，强制只加载phase0 的 embedding 数据
        # TDOO: find a better way to handle model bank uri for different job types
        model_bank_uri = (
            "re#phase0.*,xdl_global_step@" + model_bank_uri.split("@")[1]
        )
        return model_bank_uri, exec_properties.get("model_uri_base", "")