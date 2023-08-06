import requests
import json
import logging
import sys
import time

HK_CYCLONE_GET_MASTER_URL = (
    "http://169.136.88.180:6210/CycloneMetaService/GetMasterInfo"
)
SG_CYCLONE_GET_MASTER_URL = (
    "http://169.136.88.180:6210/CycloneMetaService/GetMasterInfo"
)
CYCLONE_PUBLISH_MODEL_URI = "http://{}:6210/CycloneMetaService/PublishModel"


class CycloneOptions(object):
    __slots__ = [
        "model_name",
        "model_version",
        "model_class",
        "mask",
        "dup_cnt",
    ]

    def __init__(
        self,
        model_name,
        model_version,
        model_class="EmbeddingZmapModel",
        mask=65535,
        dup_cnt=3,
    ):
        self.model_name = model_name
        self.model_version = model_version
        self.model_class = model_class
        self.mask = mask
        self.dup_cnt = dup_cnt


def get_cyclone_master(is_hk=False, try_limit=3):
    url = HK_CYCLONE_GET_MASTER_URL if is_hk else SG_CYCLONE_GET_MASTER_URL

    def convert_netaddr(x):
        return ".".join([str(x // (256 ** i) % 256) for i in range(0, 4)])

    ret = None
    for i in range(try_limit):
        r = requests.get(url, headers={"content-type": "application/json"})
        if r.status_code != 200 or r.json().get("status") != "OK":
            logging.info(
                "get_cyclone_master, retry %d, status: %s, response: %s"
                % (i + 1),
                r.status_code,
                r.text,
            )
            time.sleep(0.1)
            continue
        ret = convert_netaddr(r.json().get("master_ip"))
        break
    return ret


def publish_model_to_cyclone(options, shards, is_hk=False, try_limit=3):
    master_ip = get_cyclone_master(is_hk, try_limit)
    if not master_ip:
        logging.error("Failed to get ip of cyclone meta master")
        return False

    basic_info = {
        "dup_count": options.dup_cnt,
        "publish_time": options.model_version,
        "name": options.model_name,
        "class_name": options.model_class,
        "mask": options.mask,
        "version": str(options.model_version),
    }

    body = {"basic_info": basic_info, "shards": shards}
    for try_cnt in range(try_limit):
        resp = requests.get(
            CYCLONE_PUBLISH_MODEL_URI.format(master_ip),
            headers={"content-type": "application/json"},
            data=json.dumps(body),
        )
        if resp.status_code == 200 and resp.json().get("status") == "OK":
            return True
        time.sleep(1)
    logging.error(
        "Failed to publish model to cyclone, cyclone master ip: %s, cyclone options: %s, shards: %s",
        master_ip,
        options,
        shards,
    )
    return False
