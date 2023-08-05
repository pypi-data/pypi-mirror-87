import os
import sys
import logging
import re
import functools
import time
import hashlib
import tempfile
from datetime import datetime, timedelta
from pytz import timezone
from typing import Any, Dict, List, Text

from bmlx.flow import Executor, Artifact
from bmlx_components.proto import schema_pb2, model_pb2
from bmlx.utils import import_utils, artifact_utils, io_utils

from bmlx_components.utils import resource_publisher, cannon_publisher


class PusherExecutor(Executor):
    def _resolve_model_meta(self, model_meta_path):
        fs, path = io_utils.resolve_filesystem_and_path(model_meta_path)
        if not fs.exists(path):
            raise RuntimeError(
                "model_meta_path %s does not exist!" % model_meta_path
            )

        model_pb = io_utils.parse_pbtxt_file(
            os.path.join(model_meta_path, "converted_model.pbtxt"),
            model_pb2.ConvertedModel(),
        )

        if not (model_pb and model_pb.embedding_path and model_pb.graph_path):
            raise RuntimeError(
                "invalid model meta info parsed from %s" % model_meta_path
            )
        logging.info("parsed pushed model meta info: %s", model_pb)

        fs, path = io_utils.resolve_filesystem_and_path(model_pb.embedding_path)
        if not fs.exists(path):
            raise RuntimeError(
                "model embedding path %s does not exist!"
                % model_pb.embedding_path
            )

        fs, path = io_utils.resolve_filesystem_and_path(model_pb.graph_path)
        if not fs.exists(path):
            raise RuntimeError(
                "model graph path %s does not exist!" % model_pb.graph_path
            )

        fs, path = io_utils.resolve_filesystem_and_path(model_pb.fg_path)
        if not fs.exists(path):
            raise RuntimeError(
                "model fg path %s does not exist!" % model_pb.fg_path
            )
        return model_pb

    def _resolve_fg_confs(self, new_fg_path, fg_collection, fg_name):
        """
        临时逻辑，判断是否需要发布 fg.yaml
        """

        def get_file_checksum(path):
            hasher = hashlib.md5()
            hasher.update(io_utils.read_file_string(path))
            return hasher.hexdigest()

        try:
            new_checksum = get_file_checksum(new_fg_path)

            DISP_MODEL_PATH = (
                "hdfs://bigocluster/user/hadoop/dispatching/models"
            )
            fg_dir = f"{DISP_MODEL_PATH}/{fg_collection}/{fg_name}"
            fs, path = io_utils.resolve_filesystem_and_path(fg_dir)

            if not fs.exists(path):
                return (new_fg_path, new_checksum, "", "")

            assert fs.isdir(path)
            version_list = [f for f in fs.ls(path) if fs.isdir(f)]
            if not version_list:
                return (new_fg_path, new_checksum, "", "")

            assert version_list and version_list[-1].split("/")[-1].isdigit()
            last_fg_path = f"{version_list[-1]}/{fg_name}.yml"
            last_checksum = get_file_checksum(last_fg_path)

            return (new_fg_path, new_checksum, last_fg_path, last_checksum)
        except Exception as e:
            logging.error("Failed with exception %s", e)
            return -1

    def skip_publish_model(self, model_meta_pb, skip_stale_model_hour):
        if re.match("^[0-9]{8}\/[0-9]{2}$", model_meta_pb.model_version):
            cst_tz = timezone("Asia/Chongqing")
            model_time = datetime.strptime(
                f"{model_meta_pb.model_version} +0800", "%Y%m%d/%H %z"
            )
            if datetime.now(cst_tz) - model_time > timedelta(
                hours=skip_stale_model_hour
            ):
                return True
        return False

    def publish_embeddings(self, exec_properties, model_version, emb_bin_path):
        def get_all_dims(emb_bin_path):
            fs, path = io_utils.resolve_filesystem_and_path(emb_bin_path)
            assert fs.isdir(path)
            emb_dir_list = [f for f in fs.ls(path) if fs.isdir(f)]
            if not emb_dir_list:
                raise RuntimeError("Invalid emb_bin_path %s" % emb_bin_path)

            emb_dims = [int(d.split("/")[-1]) for d in emb_dir_list]
            return emb_dims

        emb_dims = get_all_dims(emb_bin_path)

        emb_collection = exec_properties["emb_collection"]
        for emb_dim in emb_dims:
            input_path = os.path.join(emb_bin_path, str(emb_dim))
            cannon_pub_opts = cannon_publisher.PublishOptions(
                build_type="embed",
                input_path=input_path,
                data_name=exec_properties["model_name"],
                dim=emb_dim,
                version=model_version,
                collection=emb_collection,
                creator=exec_properties["author"],
                namespace=exec_properties["product_namespace"],
                other_args=f"{emb_collection},{emb_dim},{model_version}",
                test_env=exec_properties["test_env"],
            )
            ret = cannon_publisher.publish_resource(cannon_pub_opts)
            if ret < 0:
                raise RuntimeError(
                    "Failed to publish embedding using cannon_publisher, input path: %s"
                    % input_path
                )
            if not cannon_publisher.check_resource(cannon_pub_opts):
                raise RuntimeError("Publish embedding %s failed!" % input_path)
            else:
                logging.info("Publish embedding %s successfully!", input_path)

    def publish_graph(self, exec_properties, model_version, graph_path):
        # publish graph
        resource_pub_opts = resource_publisher.PublishOptions(
            processor=exec_properties["resource_processor"],
            collection=exec_properties["graph_collection"],
            name=exec_properties["model_name"],
            version=model_version,
            hdfs_src=graph_path,
        )

        ret = resource_publisher.publish_resouce(resource_pub_opts)
        if not ret:
            raise RuntimeError(
                "Failed to publish graph using resource_publisher"
            )
        else:
            logging.info("Publish graph successfully!")

    def publish_fg_conf(self, exec_properties, model_version, fg_path):
        # publish fg yaml if needed
        # 临时逻辑，后续上了RTP 可以去掉这块
        (
            new_fg_path,
            new_checksum,
            last_fg_path,
            last_checksum,
        ) = self._resolve_fg_confs(
            fg_path,
            exec_properties["fg_collection"],
            exec_properties["fg_name"],
        )

        if new_checksum != last_checksum:
            logging.info(
                "%s(%s) != %s(%s), need to update fg conf",
                last_fg_path,
                last_checksum,
                new_fg_path,
                new_checksum,
            )
            with tempfile.TemporaryDirectory() as temp_dir:
                fs, _ = io_utils.resolve_filesystem_and_path(fg_path)
                fs.download(
                    fg_path,
                    os.path.join(temp_dir, exec_properties["fg_name"] + ".yml"),
                )
                resource_pub_opts = resource_publisher.PublishOptions(
                    processor="DELIVER",
                    collection=exec_properties["fg_collection"],
                    name=exec_properties["fg_name"],
                    version=model_version,
                    local_src=temp_dir,
                )
                ret = resource_publisher.publish_resouce(resource_pub_opts)

            if not ret:
                raise RuntimeError(
                    "Failed to publish fg conf using resource_publisher"
                )
            else:
                logging.info("Publish fg conf successfully!")
        else:
            logging.info(
                "%s(%s) == %s(%s), fg conf yaml does not need to update",
                last_fg_path,
                last_checksum,
                new_fg_path,
                new_checksum,
            )

    def execute(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        self._log_startup(input_dict, output_dict, exec_properties)

        assert (
            "converted_model" in input_dict
            and len(input_dict["converted_model"]) == 1
        )
        model_meta_pb = self._resolve_model_meta(
            input_dict["converted_model"][0].meta.uri
        )
        skip_stale_model_hour = exec_properties["skip_stale_model_hour"]

        if self.skip_publish_model(model_meta_pb, skip_stale_model_hour):
            cst_tz = timezone("Asia/Chongqing")
            logging.info(
                "model is %d hours earlier, model time: %s, "
                "current time: %s, skip to publish this model !!!!",
                skip_stale_model_hour,
                model_meta_pb.model_version,
                datetime.now(cst_tz).strftime("%Y%m%d/%H"),
            )
            return

        fg_conf_path = os.path.join(model_meta_pb.fg_path, "fg.yaml")
        model_version = int(time.time())

        # publish embedding
        self.publish_embeddings(
            exec_properties, model_version, model_meta_pb.embedding_path
        )
        self.publish_fg_conf(exec_properties, model_version, fg_conf_path)
        self.publish_graph(
            exec_properties, model_version, model_meta_pb.graph_path
        )
