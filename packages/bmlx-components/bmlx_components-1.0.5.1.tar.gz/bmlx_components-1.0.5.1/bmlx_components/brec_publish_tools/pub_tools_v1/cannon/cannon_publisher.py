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

fpath = os.path.dirname(os.path.abspath(__file__))

PARE_PATH = os.path.join(fpath, os.pardir)

sys.path.append(PARE_PATH)
sys.path.append(PARE_PATH + "/data_scripts/")

from hdfs_helper import hdfs_distcp
from update_resource_k8s import sync

# DEAMON_URL = "http://daemon.welog.bigo.sg:3000/daemonquery"
DEAMON_URL = "http://157.119.233.204:3000/daemonquery"

hk_service_name = "brpc.brec_cyclone_meta_d_v1"
sg_service_name = "brpc.brec_cyclone_meta_d_v1_sg"


cyclone_base = "/CycloneMetaService"
master_path = cyclone_base + "/GetMasterInfo"
publish_path = cyclone_base + "/PublishModel"


def number_to_ip(number):
    return ".".join(map(str, number.to_bytes(4, "little")))


def get_ips_from_service(service_name):
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


tools_dir = os.environ.get("tools_dir")
if not tools_dir:
    print("cannot find tools dir")
    os._exit(-1)


class create_job:
    def __init__(self, job_conf, job_dict, job_url):
        self.url = job_url
        job_json = None
        with open(tools_dir + "/cannon/" + job_conf, "r") as job_f:
            job_json = json.load(job_f)
        ts = time.time()
        self.data = deepcopy(job_json)
        self.data["create_time"] = int(ts)
        self.data["update_time"] = int(ts)
        if job_dict:
            for key in job_dict:
                self.data[key] = job_dict[key]

        if not self.data["creator"]:
            print("Creator is none")
            return -1
        self.data = json.dumps(self.data)
        self.headers = {"content-type": "application/json"}

    def post(self):
        try:
            r = requests.post(self.url, self.data, headers=self.headers)
            resJs = json.loads(r.text)
            if not "success" in resJs["errmsg"]:
                print(r.text)
                return -1
            job_id_str = resJs["data"]["id"]
            job_id = int(job_id_str)
            return job_id
        except Exception as e:
            print(e)
            return -1


class create_task:
    def __init__(self, job_id, task_conf, task_dict, task_url):
        self.url = task_url
        task_json = None
        with open(tools_dir + "/cannon/" + task_conf, "r") as task_f:
            task_json = json.load(task_f)
        self.data = deepcopy(task_json)
        if task_dict:
            for key in task_dict:
                if isinstance(task_dict[key], dict):
                    for sub_key in task_dict[key]:
                        self.data[key][sub_key] = task_dict[key][sub_key]
                else:
                    self.data[key] = task_dict[key]

        ts = time.time()
        self.data["create_time"] = int(ts)
        self.data["job_id"] = job_id
        self.headers = {"content-type": "application/json"}
        self.data = json.dumps(self.data)
        print(self.data)

    def post(self):
        try:
            r = requests.post(self.url, self.data, headers=self.headers)
            resJs = json.loads(r.text)
            if not "success" in resJs["errmsg"]:
                print(r.text)
                return -1
            task_id_str = resJs["data"]["id"]
            task_id = int(task_id_str)
            return task_id
        except Exception as e:
            print(e)
            return -1


def check_task_status(url, data_url, deliver, ns, dt):
    print("start check status")
    i = 0
    while i < 400:
        print(i)
        i += 1
        try:
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            resp = requests.get(
                url=url, params="", headers={"content-type": "application/json"}
            )
            print(resp.text)
            resp_json = json.loads(resp.text)
            if resp_json["data"] is None:
                return 1
            elif (
                "success" in resp_json["data"]["status"]
                and resp_json["data"]["data_id"] != 0
            ):
                print("get success with deliver:", deliver, "data_type", dt)
                if deliver != "":
                    print("start to publish sg")
                    data_id = resp_json["data"]["data_id"]
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

                    service_name = sg_service_name
                    if deliver == "hk2sg":
                        print("start cp hdfs from hk to sg")
                        hdfs_distcp(
                            data["path"].replace("bigocluster", "hk-bigocluster"),
                            "hdfs://bigocluster/data/models/"
                            + ns
                            + "/"
                            + name
                            + "/"
                            + str(version),
                        )
                    elif deliver == "sg2hk":
                        service_name = hk_service_name
                        print("start cp hdfs from sg to hk")
                        hdfs_distcp(
                            data["path"],
                            "hdfs://hk-bigocluster/data/models/"
                            + ns
                            + "/"
                            + name
                            + "/"
                            + str(version),
                        )
                    if dt == "embed":
                        print("start to publish sg cyclone")
                        mask = param["mask"]
                        dup_count = param["dup_count"]
                        class_name = param["class_name"]
                        publish_time = param["publish_time"]
                        shards = []
                        for shard in param["shards"]:
                            shards.append(
                                {
                                    "shard_idx": shard["shard_idx"],
                                    "tail_number_start": shard[
                                        "shard_tail_number_start"
                                    ],
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
                        cyclone_ips = get_ips_from_service(service_name)
                        sg_online_meta_url = (
                            get_meta_master_host(cyclone_ips[0]) + publish_path
                        )
                        print("cyclone sg meta url is", sg_online_meta_url)
                        r = requests.get(sg_online_meta_url, json=cyclone_req)
                        j = r.json()
                        if j["status"] == "OK":
                            print("sent publish cyclone to sg")
                            return 0
                        else:
                            return 4
                    elif dt == "deliver_graph":
                        sync(ns, name, version, ["sg"])
                return 0
            elif "fail" in resp_json["data"]["status"]:
                return 2
            else:
                time.sleep(10)
        except Exception as e:
            print(e)
            return 4
    return 3


def worker(
    job_conf_str,
    task_conf_str,
    job_dict,
    task_dict,
    job_url,
    task_url,
    data_url,
    deliver,
):
    job_id = 1
    if job_url:
        job = create_job(job_conf_str, job_dict, job_url)
        job_id = job.post()
    print("---job_id is %d" % job_id)
    if job_id == -1:
        return -1
    task = create_task(job_id, task_conf_str, task_dict, task_url)
    task_id = task.post()
    print("---task_id is %d" % task_id)
    if task_id == -1:
        return -1
    print(deliver)
    print(job_dict["namespace"])
    print(task_dict["params"]["data_type"])
    rec = check_task_status(
        task_url + str(task_id),
        data_url,
        deliver,
        job_dict["namespace"],
        task_dict["params"]["data_type"],
    )

    return rec


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--srv_addr", type=str, help="service address")
    parser.add_argument(
        "--job_conf_str", type=str, default="job.json", help="job conf file"
    )
    parser.add_argument(
        "--task_conf_str", type=str, default="task.json", help="task conf file"
    )
    parser.add_argument("--build_type", type=str, help="build type")
    parser.add_argument("--input_path", type=str, help="input hdfs path")
    parser.add_argument("--output_path", type=str, help="output hdfs path")
    parser.add_argument("--data_name", type=str, help="name of data")
    parser.add_argument("--class_name", type=str, help="class name")
    parser.add_argument("--version", type=str, help="data version")
    parser.add_argument(
        "--collection", type=str, default="CYCLONE_COLLECTION", help="data version"
    )
    parser.add_argument("--other_args", type=str, help="other args")
    parser.add_argument("--creator", type=str, help="user_email")
    parser.add_argument("--namespace", type=str, help="app namespace")
    parser.add_argument("--phase", type=str, help="final , cyclone or intermediate")
    parser.add_argument(
        "--overseas", type=str, help="whether publish to overseas cyclone"
    )
    parser.add_argument(
        "--hdfs_sync", type=int, help="whether synchronize to localhdfs"
    )
    parser.add_argument("--type", type=int, help="full or increment")
    parser.add_argument("--dup_cnt", type=int, help="data dup count in cyclone")
    parser.add_argument("--min_dup_cnt", type=int, help="data min dup count in cyclone")
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        choices=["test", "hk", "sg"],
        default="hk",
        help="where the origion data is",
    )

    parser.add_argument(
        "-d",
        "--destination",
        choices=["hk", "sg"],
        type=str,
        nargs="*",
        default=["hk", "sg"],
        help="model publish destination data center multiple choice(default hk & sg)",
    )

    args = parser.parse_args()
    print(args.destination)

    job_conf_str = "job.json"
    task_conf_str = "task.json"
    if args.srv_addr and args.task_conf_str:
        task_conf_str = args.task_conf_str
    elif args.job_conf_str and args.task_conf_str:
        job_conf_str = args.job_conf_str
        task_conf_str = args.task_conf_str

    job_dict = dict()
    task_dict = dict()
    task_dict["params"] = dict()
    if args.creator:
        job_dict["creator"] = args.creator
    if args.namespace:
        job_dict["namespace"] = args.namespace
        task_dict["namespace"] = args.namespace
    if args.build_type:
        task_dict["params"]["data_type"] = args.build_type
    if args.data_name:
        task_dict["params"]["data_name"] = args.data_name
    if args.input_path:
        task_dict["params"]["input_path"] = args.input_path
    if args.output_path:
        task_dict["params"]["output_path"] = args.output_path
    if args.class_name:
        task_dict["params"]["class_name"] = args.class_name
    if args.version:
        task_dict["params"]["version"] = args.version
    if args.overseas:
        task_dict["params"]["overseas"] = args.overseas
    if args.collection:
        task_dict["params"]["collection"] = args.collection
    if args.other_args:
        task_dict["params"]["args"] = args.other_args
    if args.phase:
        task_dict["phase"] = args.phase
    if args.hdfs_sync:
        task_dict["hdfs_sync"] = args.hdfs_sync
    if args.type:
        task_dict["type"] = args.type
    if args.dup_cnt:
        task_dict["params"]["dup_cnt"] = args.dup_cnt
    if args.min_dup_cnt:
        task_dict["params"]["min_dup_cnt"] = args.min_dup_cnt
    base_url = "http://43.224.67.124:8787/"
    if args.source == "test":
        base_url = "http://164.90.76.189:8787/"
    elif args.source == "sg":
        base_url = "http://202.63.35.230:8787/"
    task_url = base_url + "api/v1/tasks/"
    job_url = base_url + "api/v1/jobs/"
    data_url = base_url + "api/v1/datas/"

    if args.srv_addr:
        task_url = args.srv_addr
        job_url = None

    deliver = ""
    if args.source == "hk" or args.source == "test" and "sg" in args.destination:
        deliver = "hk2sg"
    elif args.source == "sg" and "hk" in args.destination:
        deliver = "sg2hk"

    try:
        rec = worker(
            job_conf_str,
            task_conf_str,
            job_dict,
            task_dict,
            job_url,
            task_url,
            data_url,
            deliver,
        )
        sys.exit(rec)
    except Exception as e:
        print(e)
