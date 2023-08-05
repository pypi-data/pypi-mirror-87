import logging
import os
from bmlx_components.xdl_base.launcher import XdlLauncher
from bmlx.utils import artifact_utils, io_utils
from bmlx_components.proto import model_pb2


class XdlTrainerLauncher(XdlLauncher):
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
        if "previous_model" in input_dict:
            if len(input_dict["previous_model"]) > 0:
                model_uri = artifact_utils.get_single_uri(
                    input_dict["previous_model"]
                )

        # 优先通过bmlx的 meta 文件获取model uri(如果路径下有 model.pbtxt，则认为使用 model.pbtxt 去获得model 实际路径)
        if model_uri and io_utils.exists(
            os.path.join(model_uri, "model.pbtxt")
        ):
            model_uri = self._resolve_model_uri(
                os.path.join(model_uri, "model.pbtxt")
            )

        if "model_file_pattern" not in exec_properties:
            raise RuntimeError("model file pattern must set")

        warmup_opened = False
        # 如果选到了基础模型，则使用基础模型
        if model_uri:
            model_bank_uri = self._get_model_bank_uri(
                model_uri, exec_properties["model_file_pattern"]
            )
            warmup_opened = False
        # 如果没有基础模型，且设置了 warmup_model_bank
        elif exec_properties.get("warmup_model_bank"):
            model_bank_uri = exec_properties["warmup_model_bank"]
            warmup_opened = True
        else:
            model_bank_uri = ""
            warmup_opened = False

        logging.info(
            "warmup %s, selected model bank uri: %s",
            "opened" if warmup_opened else "closed",
            model_bank_uri,
        )
        return model_bank_uri, exec_properties.get("model_uri_base", "")

    def _need_launch_xdl(self, input_dict, exec_properties):
        return True
