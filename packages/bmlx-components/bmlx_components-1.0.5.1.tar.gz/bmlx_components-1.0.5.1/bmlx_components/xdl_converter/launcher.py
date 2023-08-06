from bmlx_components.xdl_base.launcher import XdlLauncher
from bmlx.utils import artifact_utils


class XdlConverterLauncher(XdlLauncher):
    def _resolve_model_paths(self, input_dict, exec_properties):
        return "", ""

    def _need_launch_xdl(self, input_dict, exec_properties):
        return True
