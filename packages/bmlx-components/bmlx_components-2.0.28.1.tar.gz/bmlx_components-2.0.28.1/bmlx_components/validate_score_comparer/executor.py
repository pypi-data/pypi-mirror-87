import logging
import os
import struct
import math
import tempfile
import base64
import sys
import zlib
from typing import Dict, Text, List, Any
from bmlx.flow import Executor, Artifact
from bmlx.utils import artifact_utils, io_utils
from xdl.python.proto import trace_pb2
import numpy as np


def trace2nptype(tp):
    if tp == trace_pb2.Int8:
        return np.int8
    elif tp == trace_pb2.Int16:
        return np.int16
    elif tp == trace_pb2.Int32:
        return np.int32
    elif tp == trace_pb2.Int64:
        return np.int64
    elif tp == trace_pb2.Float:
        return np.float32
    elif tp == trace_pb2.Double:
        return np.float64
    elif tp == trace_pb2.Bool:
        return np.bool
    elif tp == trace_pb2.Byte:
        return np.byte
    else:
        raise RuntimeError("unknown trace data type: {}".format(tp))


def getDct(infostr):
    dct = {}
    for iter_str in infostr.split("#"):
        if len(iter_str) == 0:
            continue
        fd_pos = iter_str.find(":")
        if fd_pos == -1:
            continue
        key = iter_str[:fd_pos]
        val = iter_str[fd_pos + 1 :]
        dct[key] = val
    return dct


def parse_column(key, col):
    val = np.frombuffer(col.data, dtype=trace2nptype(col.dtype)).reshape(
        col.shape
    )[0]
    if key == "sampleid":
        val = getDct("".join(chr(v) for v in val))
    else:
        val = list(val)
    return val


class ScoreComparerExecutor(Executor):
    def download_to_local(self, remote_path, local_dir):
        fs, path = io_utils.resolve_filesystem_and_path(remote_path)
        local_path = os.path.join(local_dir, os.path.basename(remote_path))
        fs.download(
            remote_path, local_path,
        )
        return local_path

    def parse_featurelog_line(self, line):
        try:
            compressed_bytes = base64.b64decode(line)
        except Exception as e:
            logging.error(
                "Failed to decode base64 featurelog, exception: %d", e
            )
            return None

        origin_bytes = zlib.decompress(compressed_bytes)

        sys.path.insert(
            0, os.path.join(os.path.dirname(__file__), "../mlplat-protos")
        )
        from mlplat.feature import original_feature_pb2

        origin_feature = original_feature_pb2.OriginalFeature()
        origin_feature.ParseFromString(origin_bytes)

        ret = {}
        dispatcher_id = origin_feature.scenario.feature[
            "dispatcher_id"
        ].bytes.decode()
        for (vid, s_list, final_score) in zip(
            origin_feature.items.item_ids,
            origin_feature.items.items_online.feature_list[
                "rank_judgements_score"
            ].feature,
            origin_feature.items.items_online.feature_list[
                "ranker_judgement_score"
            ].feature,
        ):
            multi_score_list = s_list.float_list.value
            if (
                len(multi_score_list) == 0
                and float(final_score.double) > 1000.0
            ):
                continue
            if len(multi_score_list) == 0:
                multi_score_list = [float(final_score.double)]
            ret[f"{dispatcher_id}_{vid}"] = multi_score_list

        return ret

    def parse_online_scores(self, path):
        ret = {}
        with open(path, "r") as f:
            for line in f.readlines():
                ret.update(self.parse_featurelog_line(line))
        return ret

    def getDct(self, infostr):
        dct = {}
        for iter_str in infostr.split("#"):
            if len(iter_str) == 0:
                continue
            fd_pos = iter_str.find(":")
            if fd_pos == -1:
                continue
            key = iter_str[:fd_pos]
            val = iter_str[fd_pos + 1 :]
            dct[key] = val
        return dct

    def parse_column(key, col):
        val = np.frombuffer(col.data, dtype=trace2nptype(col.dtype)).reshape(
            col.shape
        )[0]
        if key == "sampleid":
            val = getDct("".join(chr(v) for v in val))
        else:
            val = list(val)
        return val

    def parse_offline_scores(self, path):
        with open(path, "rb") as f:
            trace_content = f.read()
            content_len = len(trace_content)
            sz = struct.unpack("<I", trace_content[:4])[0]
            buf = trace_content[4 : 4 + sz]
            hdrs = trace_pb2.Header()
            hdrs.ParseFromString(buf)

            readed = 4 + sz
            ret = {}
            while readed < content_len:
                buf = trace_content[readed : readed + 4]
                if not buf:
                    break
                readed += 4
                sz = struct.unpack("<I", buf)[0]
                buf = trace_content[readed : readed + sz]
                record = trace_pb2.Record()
                record.ParseFromString(buf)
                readed += sz

                dispatch_id = None
                vid = None
                y_pred = None
                for key, col in dict(zip(hdrs.key, record.column)).items():
                    key = str(key)
                    val = parse_column(key, col)
                    if key == "sampleid":
                        dispatch_id = str(val["dispatch_id"])
                        vid = str(val["vid"])
                    elif key == "y_pred":
                        y_pred = val
                ret[f"{dispatch_id}_{vid}"] = [float(v) for v in y_pred]
            return ret

    def compare_scores(self, online_score, offline_score):
        diff_nums = [0, 0, 0, 0]
        anum = 0
        top_que = []
        for k, v in online_score.items():
            if k in offline_score:
                if len(v) != len(offline_score[k]) or len(v) == 0:
                    continue

                res_list = []
                diff = math.fabs(v[0] - offline_score[k][0])
                if diff < 0.00001:
                    diff_nums[3] += 1
                elif diff < 0.0001:
                    diff_nums[2] += 1
                elif diff < 0.001:
                    diff_nums[1] += 1
                elif diff < 0.01:
                    diff_nums[0] += 1
                for idx in range(len(v)):
                    delta = v[idx] - offline_score[k][idx]
                    res_list.append(
                        "{}:{}:{}".format(v[idx], offline_score[k][idx], delta)
                    )
                top_que.append((diff, k, v[0], offline_score[k][0]))
                anum += 1

        assert anum > 0, "anum = 0!!!"

        logging.info(sorted(top_que, key=lambda x: x[0], reverse=True)[:100])
        anum = float(anum)
        other_num = anum - sum(diff_nums)
        msg = "score diff [>=0.01,<0.01,<0.001,<0.0001,<0.00001]: {:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(
            other_num / anum,
            diff_nums[0] / anum,
            diff_nums[1] / anum,
            diff_nums[2] / anum,
            diff_nums[3] / anum,
        )
        logging.info(msg)

    def execute(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
    ):
        self._log_startup(input_dict, output_dict, exec_properties)
        assert len(input_dict["origin_samples"]) == 1
        assert len(input_dict["predict_result"]) == 1

        with tempfile.TemporaryDirectory() as tempdir:
            online_scores = self.parse_online_scores(
                self.download_to_local(
                    os.path.join(
                        input_dict["origin_samples"][0].meta.uri,
                        "origin_samples.txt",
                    ),
                    tempdir,
                )
            )

            offline_scores = self.parse_offline_scores(
                self.download_to_local(
                    os.path.join(
                        input_dict["predict_result"][0].meta.uri,
                        "test.trace.txt.0.1",
                    ),
                    tempdir,
                )
            )
            logging.info("##### online scores: %s", online_scores)
            logging.info("##### offline scores: %s", offline_scores)
            self.compare_scores(online_scores, offline_scores)
