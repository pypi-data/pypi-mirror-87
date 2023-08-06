"""bmlx model converter executor."""
import os
import sys
import logging
import tempfile
import re
import json
import xdl
import subprocess
import functools
from typing import Any, Dict, List, Text
import tensorflow as tf
from xdl.python.ops.ps_ops import ps_local_read_variables
from xdl.python.backend.tf.convert_utils import TF2XDL

from bmlx.flow import Executor, Artifact
from bmlx.fs.file_system import LocalFileSystem
from bmlx_components.proto import schema_pb2, model_pb2
from bmlx.utils import import_utils, artifact_utils, io_utils
from bmlx_components.xdl_converter.fg_conf_converter import FgConfConverter
from bmlx_components.xdl_base.executor import XdlExecutor
from bmlx_components.xdl_converter import validate_sample_converter

CONVERTED_MODEL_OUTPUT_DIR = "converted_model"
EMB_BIN_DIR = "emb_bin"
ONLINE_MODEL_DIR = "online_model/"
FG_DIR = "online_model/fg/"
VALIDATE_SAMPLE_DIR = "online_model/validate_sample/"
OPTIMIZED_GRAPH_DIR = "online_model/optimized_graph/"
MODEL_WITH_NEW_TYPE = "XdlV9Model"
RTP_MODEL_CLASS = "RtpXdlV1"


class XdlConverterExecutor(XdlExecutor):
    def _init_output_dir(self, output_dir):
        fs, path = io_utils.resolve_filesystem_and_path(output_dir)
        if not fs.exists(path):
            fs.mkdir(path)
        if not fs.exists(os.path.join(output_dir, EMB_BIN_DIR)):
            fs.mkdir(os.path.join(output_dir, EMB_BIN_DIR))
        if not fs.exists(os.path.join(output_dir, ONLINE_MODEL_DIR)):
            fs.mkdir(os.path.join(output_dir, ONLINE_MODEL_DIR))
        if not fs.exists(os.path.join(output_dir, FG_DIR)):
            fs.mkdir(os.path.join(output_dir, FG_DIR))
        if (
            fs.exists(path)
            and fs.exists(os.path.join(output_dir, EMB_BIN_DIR))
            and fs.exists(os.path.join(output_dir, ONLINE_MODEL_DIR))
            and fs.exists(os.path.join(output_dir, FG_DIR))
        ):
            logging.info(
                "initialize converted model output dir: %s successfully!",
                output_dir,
            )
            return True
        else:
            logging.error(
                "initialize converted model output dir: %s failed!", output_dir
            )
            return False

    def _convert_sparse(
        self, exec_properties, ckpt_dir, origin_model_conf, output_dir
    ):
        emb_bin_info = origin_model_conf["emb_bin_info"]
        filter_str = ";".join(
            [
                var_name + ":" + slot_lst
                for (var_name, slot_lst) in emb_bin_info.items()
            ]
        )

        emb_bin_outputdir = os.path.join(output_dir, EMB_BIN_DIR)
        xdl.convert_sparse(
            ckpt_dir,
            emb_bin_outputdir,
            filter_str,
            default_threshold=exec_properties["export_emb_default_threshold"],
            var_threshold=exec_properties.get("var_threshold", {}),
            worker_id=xdl.get_task_index(),
            worker_num=xdl.get_task_num(),
            file_num=exec_properties.get("file_num", 1024),
            with_slot=exec_properties.get("with_slot", True),
            halfp=exec_properties["half_p"],
        )

    def _drop_unused_slots(self, ori_conf, exclude_slots):
        emb_slot_to_slot_dict = {}
        exclude_emb_slots = []
        for var_name, info in ori_conf["inputs"].items():
            if "emb_slot" in info and "slot" in info:
                emb_slot_str = str(info["emb_slot"])
                if emb_slot_str not in emb_slot_to_slot_dict:
                    emb_slot_to_slot_dict[emb_slot_str] = []
                emb_slot_to_slot_dict[emb_slot_str].append(str(info["slot"]))

        for var_name, _ in ori_conf["emb_bin_info"].items():
            idx = var_name.find("/")
            emb_slot = var_name
            if idx != -1:
                emb_slot = var_name[idx + 1 :]

            need_del = True
            for slot in emb_slot_to_slot_dict[emb_slot]:
                if slot not in exclude_slots:
                    need_del = False
                    break

            if need_del:
                exclude_emb_slots.append(emb_slot)
                del ori_conf["emb_bin_info"][var_name]

        for var_name, info in ori_conf["inputs"].items():
            if (
                "emb_slot" in info
                and str(info["emb_slot"]) in exclude_emb_slots
            ):
                del ori_conf["inputs"][var_name]

        for slot, _ in ori_conf["emb_slot_dim_dict"].items():
            if slot in exclude_emb_slots:
                del ori_conf["emb_slot_dim_dict"][slot]

        return ori_conf

    def _resolve_model_meta(self, model_meta_dir: Text):
        if io_utils.exists(os.path.join(model_meta_dir, "model.pbtxt")):
            model_meta_path = os.path.join(model_meta_dir, "model.pbtxt")
            model_pb = io_utils.parse_pbtxt_file(
                model_meta_path, model_pb2.Model()
            )
            if not (model_pb and model_pb.model_path):
                raise RuntimeError(
                    "invalid model meta info parsed from %s" % model_meta_path
                )
        elif io_utils.exists(model_meta_dir):
            model_meta_dir = model_meta_dir.strip("/")
            model_pb = model_pb2.Model()
            model_pb.model_path = "/".join(model_meta_dir.split("/")[:-1])
            model_pb.model_version = model_meta_dir.split("/")[-1]
        else:
            raise RuntimeError("Empty model meta dir")

        logging.info("parsed model meta info: %s", model_pb)
        return model_pb

    def _resolve_origin_fg_conf(self, origin_fg_conf_path):
        fs, uri = io_utils.resolve_filesystem_and_path(origin_fg_conf_path)
        if not fs.exists(uri):
            raise RuntimeError(
                "Origin fg conf %s does not exist" % origin_fg_conf_path
            )
        return io_utils.read_file_string(origin_fg_conf_path)

    def _get_whole_inputs(self, ori_conf, tf_graph_inputs):
        whole_inputs = []
        for (ori_name, _) in ori_conf["inputs"].items():
            p_name = ori_name[0:-2]
            if p_name in tf_graph_inputs:
                assert ori_conf["inputs"][ori_name]["slot"].isdigit(), (
                    "slot %s must be a digit."
                    % str(ori_conf["inputs"][ori_name]["slot"])
                )

                if ori_conf["inputs"][ori_name]["slot"].isdigit():
                    whole_inputs.append(
                        int(ori_conf["inputs"][ori_name]["slot"])
                    )
        return whole_inputs

    def _rewrite_model_conf(
        self, ori_conf, tf_graph_inputs, output_node, shared_slots, model_class
    ):
        model_conf = {
            "model_class": model_class,
            "inputs": {},
            "output": output_node,
            "embeddings": [],
            "shared_slots": shared_slots,
        }

        # 1.fill inputs
        for (ori_name, info) in ori_conf["inputs"].items():
            p_name = ori_name[0:-2]
            # TODO: 这块转换逻辑太trick，后续需要和在线一块重构
            if p_name in tf_graph_inputs:
                model_conf["inputs"][p_name] = info
                model_conf["inputs"][p_name]["slot"] = int(info["slot"])
                if model_class != MODEL_WITH_NEW_TYPE and model_conf["inputs"][
                    p_name
                ]["type"] in [
                    "embedding",
                    "statistics",
                    "statistis",
                    "sub_graph",
                ]:
                    model_conf["inputs"][p_name]["type"] = "sparse"

                if (
                    model_class != RTP_MODEL_CLASS
                    and "dim" in model_conf["inputs"][p_name]
                ):
                    del model_conf["inputs"][p_name]["dim"]
                else:
                    model_conf["outputs"] = [output_node]

        # 2.fill embeddings
        emb_slot_dim_dict = ori_conf["emb_slot_dim_dict"]
        dim_slots_map = {}

        for (emb_slot, dim) in emb_slot_dim_dict.items():
            emb_slot = str(emb_slot)
            emb_slot_int = int(emb_slot)

            if dim not in dim_slots_map:
                dim_slots_map[dim] = []
            dim_slots_map[dim].append(emb_slot_int)

        for (dim, emb_slots) in dim_slots_map.items():
            model_conf["embeddings"].append(
                {"dim": int(dim), "slots": emb_slots}
            )
        return model_conf

    def _save_model_meta(
        self, output_dir, model_version, model_meta_output_path
    ):
        converted_model = model_pb2.ConvertedModel()
        converted_model.embedding_path = os.path.join(output_dir, EMB_BIN_DIR)
        converted_model.graph_path = os.path.join(output_dir, ONLINE_MODEL_DIR)
        converted_model.fg_path = os.path.join(output_dir, FG_DIR)
        converted_model.model_version = model_version
        logging.info(
            "convert finished, model meta gen to %s" % model_meta_output_path
        )
        io_utils.write_pbtxt_file(
            os.path.join(model_meta_output_path, "converted_model.pbtxt"),
            converted_model,
        )

    def _convert_graph(self, exec_properties, model_meta_pb):
        with tf.compat.v1.Session() as sess:
            # 1. import graph
            tf.compat.v1.train.import_meta_graph(
                os.path.join(
                    model_meta_pb.model_path,
                    model_meta_pb.model_version,
                    "tf_predict_graph_0.pb",
                )
            )
            names = []
            denses = []
            for v in tf.compat.v1.global_variables():
                names.append(v.name[0:-2])
                denses.extend(
                    ps_local_read_variables(
                        os.path.join(
                            model_meta_pb.model_path,
                            model_meta_pb.model_version,
                        ),
                        [v.name[0:-2]],
                        [TF2XDL.convert_type(v.dtype.base_dtype)],
                    )
                )

            # 2. trans dense to const and frozen graph
            assert len(denses) == len(names)

            i = 0
            for v in tf.compat.v1.global_variables():
                if v.name[0:-2] == names[i]:
                    op = v.assign(denses[i])
                    sess.run(op)
                    i += 1
            assert len(denses) == i

            output_node = exec_properties["output_node"]
            real_output_node = None
            # protect_identity = []
            for n in tf.compat.v1.get_default_graph().as_graph_def().node:
                if n.name.endswith(output_node):
                    assert real_output_node is None, (
                        "Node endswith %s doesn't uniq in graph" % output_node
                    )
                    real_output_node = n.name

            assert real_output_node is not None, (
                "Can't find output node endswith %s in tf graph" % output_node
            )

            logging.info("real_output_node: %s", real_output_node)

            frozen_graph = tf.compat.v1.graph_util.convert_variables_to_constants(
                sess,
                tf.compat.v1.get_default_graph().as_graph_def(),
                [real_output_node],
            )

            frozen_graph = tf.compat.v1.graph_util.remove_training_nodes(
                frozen_graph
            )

            return frozen_graph, real_output_node

    def _get_tf_graph_inputs(self, origin_model_conf, frozen_graph):
        trace_vars = []
        for _, info in origin_model_conf["trace_vars"].items():
            trace_vars.append(info["target_tensor"][0:-2])
        logging.info("trace_vars: %s", trace_vars)

        inputs = []
        for n in frozen_graph.node:
            if n.op == "Placeholder" or n.name in trace_vars:
                inputs.append(n.name)
        return inputs

    def _convert_fg_conf(
        self, input_dict, exec_properties, origin_model_conf, inputs
    ):
        origin_fg_conf_content = self._resolve_origin_fg_conf(
            input_dict["fg_conf"][0].meta.uri
        )
        yaml_converter = FgConfConverter(origin_fg_conf_content)

        whole_inputs = self._get_whole_inputs(origin_model_conf, inputs)

        valid_slots = [
            slot
            for slot in whole_inputs
            if str(slot) not in exec_properties["exclude_slots"]
        ]

        converted_fg_yaml = yaml_converter.extract_sub_dag(valid_slots)
        assert len(whole_inputs) > 0, "model inputs is empty."

        return converted_fg_yaml, yaml_converter.get_shared_slots()

    def optimize_graph(
        self,
        optimize_tool_remote_path,
        fronzen_graph,
        model_conf,
        optimized_graph_remote_path,
    ):
        assert io_utils.exists(optimize_tool_remote_path)

        with tempfile.TemporaryDirectory() as tempdir:
            local_graph_path = os.path.join(tempdir, "graph.bin")
            local_conf_path = os.path.join(tempdir, "model.json")

            io_utils.write_string_file(
                local_graph_path, fronzen_graph.SerializeToString()
            )
            io_utils.write_string_file(
                local_conf_path,
                json.dumps(model_conf, indent=4, sort_keys=True).encode(),
            )

            optimize_tool_path = os.path.join(
                tempdir, os.path.basename(optimize_tool_remote_path)
            )
            io_utils.write_string_file(
                optimize_tool_path,
                io_utils.read_file_string(optimize_tool_remote_path),
            )
            # tensorflow 等so lib 在xdl convert 安装的时候，放到了该目录，直接使用
            optimize_lib_path = "/usr/lib/python3.7/site-packages/model_convert-1.0-py3.7.egg/model_convert/"
            command = "chmod +x {} && LD_LIBRARY_PATH={}:$LD_LIBRARY_PATH {} --model_path={} --output_dir ./".format(
                optimize_tool_path,
                optimize_lib_path,
                optimize_tool_path,
                tempdir,
            )

            subprocess.run(command, shell=True, check=True)

            fs = LocalFileSystem()
            result_files = [
                file_path
                for file_path in fs.ls(tempdir)
                if file_path.find("final") >= 0
            ]

            if not io_utils.exists(optimized_graph_remote_path):
                io_utils.mkdirs(optimized_graph_remote_path)

            for file_path in result_files:
                remote_path = os.path.join(
                    optimized_graph_remote_path, os.path.basename(file_path)
                )
                io_utils.write_string_file(
                    remote_path, io_utils.read_file_string(file_path)
                )

    def convert_validate_samples(
        self, input_dict: Dict[Text, List[Artifact]], output_dir: Text
    ):
        if not (
            "validate_samples" in input_dict
            and "validate_origin_samples" in input_dict
            and "validate_predict_result" in input_dict
        ):
            logging.info("Does not need to convert validate samples")
            return

        assert len(input_dict["validate_samples"]) == 1
        assert len(input_dict["validate_origin_samples"]) == 1
        assert len(input_dict["validate_predict_result"]) == 1

        validate_samples_path = input_dict["validate_samples"][0].meta.uri
        validate_origin_samples_path = input_dict["validate_origin_samples"][
            0
        ].meta.uri
        validate_predict_result_path = os.path.join(
            input_dict["validate_predict_result"][0].meta.uri,
            "test.trace.txt.0.1",
        )  # 注意这个的 trace 文件的名称，暂时 hard-code

        if not io_utils.exists(validate_samples_path):
            raise RuntimeError(
                "Invalid validate sample path: %s" % validate_samples_path
            )

        if not io_utils.exists(validate_origin_samples_path):
            raise RuntimeError(
                "Invalid origin validate sample path: %s"
                % validate_origin_samples_path
            )

        if not io_utils.exists(validate_predict_result_path):
            raise RuntimeError(
                "Invalid predict result path: %s" % validate_predict_result_path
            )
        # 将 sample(model sample) 和 predict trace 匹配，得到 sample 和 score的内容
        (
            model_samples_str,
            sample_scores_str,
        ) = validate_sample_converter.convert_model_sample_and_scores(
            io_utils.read_file_string(validate_predict_result_path),
            io_utils.read_file_string(validate_samples_path),
        )
        io_utils.write_string_file(
            os.path.join(output_dir, "original_samples"),
            io_utils.read_file_string(validate_origin_samples_path),
        )
        io_utils.write_string_file(
            os.path.join(output_dir, "model_samples"),
            model_samples_str.encode(),
        )
        io_utils.write_string_file(
            os.path.join(output_dir, "sample_scores"),
            sample_scores_str.encode(),
        )

    def execute_as_worker(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        stage = exec_properties["stage"]
        assert "fg_conf" in input_dict and "model" in input_dict

        logging.info("start xdl %s", stage)

        assert "model" in input_dict and len(input_dict["model"]) == 1

        model_meta_pb = self._resolve_model_meta(
            input_dict["model"][0].meta.uri
        )

        origin_model_conf = json.loads(
            io_utils.read_file_string(
                os.path.join(
                    model_meta_pb.model_path,
                    model_meta_pb.model_version,
                    "tf_predict_model_conf_0.txt",
                )
            )
        )

        if exec_properties["exclude_slots"]:
            origin_model_conf = self._drop_unused_slots(
                origin_model_conf, exec_properties["exclude_slots"]
            )

        output_dir = exec_properties["output_dir"] or os.path.join(
            model_meta_pb.model_path,
            model_meta_pb.model_version,
            CONVERTED_MODEL_OUTPUT_DIR,
        )

        logging.info(
            "start convert, cluster_role: %s, converted model output_dir: %s",
            exec_properties["cluster_role"],
            output_dir,
        )

        if not self._init_output_dir(output_dir):
            raise RuntimeError("Failed to init output dir")

        # all workers include worker-master and worker-slave do convert-sparse
        self._convert_sparse(
            exec_properties,
            os.path.join(model_meta_pb.model_path, model_meta_pb.model_version),
            origin_model_conf,
            output_dir,
        )
        # slave-workers do not do following works
        if exec_properties["cluster_role"] == "worker_slave":
            return

        frozen_graph, real_output_node = self._convert_graph(
            exec_properties, model_meta_pb
        )

        io_utils.write_string_file(
            os.path.join(output_dir, ONLINE_MODEL_DIR, "graph.bin"),
            frozen_graph.SerializeToString(),
        )
        # get all tf inputs
        tf_inputs = self._get_tf_graph_inputs(origin_model_conf, frozen_graph)

        # convert fg conf
        converted_fg_yaml, shared_slots = self._convert_fg_conf(
            input_dict, exec_properties, origin_model_conf, tf_inputs
        )
        # save converted fg conf yaml
        io_utils.write_string_file(
            os.path.join(output_dir, FG_DIR, "fg.yaml"),
            converted_fg_yaml.encode(),
        )
        # save fg so if needed
        if "fg_lib" in input_dict and len(input_dict["fg_lib"]) > 0:
            fg_lib_path = input_dict["fg_lib"][0].meta.uri
            assert io_utils.exists(fg_lib_path)

            file_content = io_utils.read_file_string(fg_lib_path)

            io_utils.write_string_file(
                os.path.join(
                    output_dir, FG_DIR, os.path.basename(fg_lib_path),
                ),
                file_content,
            )

        # convert model conf
        model_conf = self._rewrite_model_conf(
            origin_model_conf,
            tf_inputs,
            real_output_node,
            shared_slots,
            exec_properties["model_class"],
        )
        # save converted model conf
        io_utils.write_string_file(
            os.path.join(output_dir, ONLINE_MODEL_DIR, "model.json"),
            json.dumps(model_conf, indent=4, sort_keys=True).encode(),
        )

        # 转换小样本验证的 original sample, model sample 和 trace 数据
        self.convert_validate_samples(
            input_dict, os.path.join(output_dir, VALIDATE_SAMPLE_DIR)
        )

        # RTP 图优化
        if (
            exec_properties["model_class"] == RTP_MODEL_CLASS
            and exec_properties["optimize_tool_path"]
        ):
            self.optimize_graph(
                exec_properties["optimize_tool_path"],
                frozen_graph,
                model_conf,
                os.path.join(output_dir, OPTIMIZED_GRAPH_DIR),
            )

        # save converted_model meta info
        model_meta_output_path = artifact_utils.get_single_uri(
            output_dict["output"]
        )
        self._save_model_meta(
            output_dir, model_meta_pb.model_version, model_meta_output_path
        )
