#!/usr/bin/env python3

import os

from requests.api import request

import sys
import requests
import json
import threading
import time
import random
import argparse
from copy import copy, deepcopy
import itertools

PARE_PATH = os.path.join(sys.path[0], os.pardir)
sys.path.append(PARE_PATH)
sys.path.append(PARE_PATH + "/data_scripts/")

from hdfs_helper import hdfs_distcp

# DEAMON_URL = "http://daemon.welog.bigo.sg:3000/daemonquery"
DEAMON_URL = "http://157.119.233.204:3000/daemonquery"

service_name = "brpc.brec_cyclone_meta_d_v1_sg"

master_path = "/CycloneMetaService/GetMasterInfo"

publish_path = "/CycloneMetaService/PublishModel"


def number_to_ip(number):
    return ".".join(map(str, number.to_bytes(4, "little")))


def get_ips_from_service():
    r = requests.get(DEAMON_URL, params={"name": service_name})
    namings = filter(lambda x: x["regionId"] != 99, r.json()["favours"])
    hosts = set(
        itertools.chain(
            *map(
                lambda naming: list(
                    map(
                        lambda ip: number_to_ip(ip["ip"])
                        + ":"
                        + str(naming["favor3"]["port"]),
                        naming["favor3"]["ips"],
                    )
                ),
                namings,
            )
        )
    )
    return list(hosts)


def get_meta_master_host(master_ip):
    r = requests.get("http://" + master_ip + master_path)
    j = r.json()
    if j["status"] == "OK":
        return "http://" + number_to_ip(j["master_ip"]) + ":" + str(j["master_port"])


base_url = "http://43.224.67.124:8787/"
data_url = base_url + "api/v1/datas/"

print("start to publish sg cyclone")
data_id = 511714
data_rep = requests.get(
    url=data_url + str(data_id),
    params="",
    headers={"content-type": "application/json"},
)
print(data_rep.text)
resp_json = data_rep.json()
data = resp_json["data"]
param = data["params"]
name = data["name"]
version = data["version"]
ns = "test"
print("start cp embs hdfs from hk to sg")
hdfs_distcp(
    data["path"].replace("bigocluster", "hk-bigocluster"),
    "hdfs://bigocluster/data/models/" + ns + "/" + name,
)
mask = param["mask"]
dup_count = param["dup_count"]
class_name = param["class_name"]
publish_time = param["publish_time"]
shards = []
for shard in param["shards"]:
    shards.append(
        {
            "shard_idx": shard["shard_idx"],
            "tail_number_start": shard["shard_tail_number_start"],
            "tail_number_end": shard["shard_tail_number_end"],
            "sub_models": [
                {
                    "sub_version": str(version),
                    "data_size": shard["shard_size"],
                    "keys_count": shard["shard_item_count"],
                    "model_uri": "hdfs://bigocluster/data/models/"
                    + ns
                    + "/"
                    + name
                    + "/"
                    + str(version)
                    + "/"
                    + str(version)
                    + "_"
                    + str(shard["shard_idx"])
                    + "/",
                    "publish_time": param["publish_time"],
                }
            ],
        }
    )
cyclone_req = {
    "basic_info": {
        "name": name,
        "version": str(version),
        "mask": mask,
        "dup_count": dup_count,
        "publish_time": publish_time,
        "class_name": class_name,
    },
    "shards": shards,
}
print("cyclone request is", cyclone_req)
cyclone_ips = get_ips_from_service()
sg_online_meta_url = get_meta_master_host(cyclone_ips[0]) + publish_path
print("cyclone sg meta url is", sg_online_meta_url)
r = requests.get(sg_online_meta_url, json=cyclone_req)
j = r.json()
