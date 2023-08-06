from bmlx_components.xdl_base.driver import XdlDriver


class XdlConverterDriver(XdlDriver):
    # override super method
    def _rewrite_launch_config(self, exec_properties):
        pass

    def _resolve_model_paths(self, input_dict, exec_properties):
        return "", ""