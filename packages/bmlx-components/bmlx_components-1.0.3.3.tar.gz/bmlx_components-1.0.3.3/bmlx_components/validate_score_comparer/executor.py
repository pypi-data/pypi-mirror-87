import logging
import os
import math
import tempfile
import base64
import sys
import zlib
from typing import Dict, Text, List, Any
from bmlx.flow import Executor, Artifact
from bmlx.utils import artifact_utils, io_utils


class ScoreComparerExecutor(Executor):
    def download_to_local(self, remote_path, local_dir):
        fs, path = io_utils.resolve_filesystem_and_path(remote_path)
        local_path = os.path.join(local_dir, os.path.basename(remote_path))
        fs.download(
            remote_path, local_path,
        )
        return local_path

    def parse_featurelog_line(self, line):
        (
            region,
            country,
            scene,
            uid,
            device_id,
            dispatcher_id,
            timestamp,
            abflagv3_str,
            _os,
            pb_msg,
        ) = line.strip().split("\t")
        try:
            compressed_bytes = base64.b64decode(pb_msg)
        except Exception as e:
            logging.error(
                "Failed to decode base64 featurelog, exception: %d", e
            )
            return None
        if device_id.endswith("#1"):
            origin_bytes = zlib.decompress(compressed_bytes)
        else:
            origin_bytes = compressed_bytes

        sys.path.insert(
            0, os.path.join(os.path.dirname(__file__), "../brec_protos")
        )
        from welog.features import original_feature_pb2

        origin_feature = original_feature_pb2.OriginalFeature()
        origin_feature.ParseFromString(origin_bytes)

        ret = {}
        for item in origin_feature.items:
            rank_multi_scores = []
            rank_score = item.item_online.ranker_judgement.score
            for tt in item.item_online.ranker_multi_judgement:
                rank_multi_scores.append(tt.score)
            if len(rank_multi_scores) == 0 and float(rank_score) > 1000.0:
                continue
            if len(rank_multi_scores) == 0:
                rank_multi_scores = [float(rank_score)]
            rank_multi_scores = ",".join(map(str, rank_multi_scores))
            vid = str(item.item_inherent.post_id)

            ret[f"{dispatcher_id}_{uid}_{vid}"] = [
                float(v) for v in rank_multi_scores.split(",")
            ]
        return ret

    def parse_online_scores(self, path):
        ret = {}
        with open(path, "r") as f:
            for line in f.readlines():
                ret.update(self.parse_featurelog_line(line))
        return ret

    def parse_offline_scores(self, path):
        ret = {}
        with open(path, "r") as f:
            for line in f.readlines():
                try:
                    sampleinfo, y_pred, y_true = line.strip().split("|")
                    sampledict = {
                        item.split(":")[0]: item.split(":")[1]
                        for item in sampleinfo.split("#")
                    }
                    ret[
                        f'{sampledict["disp_id"]}_{sampledict["uid"]}_{sampledict["vid"]}'
                    ] = [float(v) for v in y_pred.split(",")]
                except Exception as e:
                    logging.error(
                        "Failed to parse offline score data with exception %s",
                        e,
                    )
                    continue
        return ret

    def compare_scores(self, online_score, offline_score):
        diff_nums = [0, 0, 0, 0]
        anum = 0
        top_que = []
        for k, v in online_score.items():
            if k in offline_score:
                if len(v) != len(offline_score[k]) or len(v) == 0:
                    # logging.warning(
                    #     "{} score dims not match {}:{}".format(
                    #         k, len(v), len(offline_score[k])
                    #     )
                    # )
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
