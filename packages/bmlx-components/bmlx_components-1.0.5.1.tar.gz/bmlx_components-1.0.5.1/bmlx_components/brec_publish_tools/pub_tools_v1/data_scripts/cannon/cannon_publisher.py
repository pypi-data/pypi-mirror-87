import os
import sys
import requests
import json
import threading
import time
import random
import argparse
from copy import copy, deepcopy

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


def check_task_status(url):
    i = 1
    while i < 400:
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
            elif "success" in resp_json["data"]["status"]:
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
    job_conf_str, task_conf_str, job_dict, task_dict, job_url, task_url, round_robin_url
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
    rec = check_task_status(round_robin_url + str(task_id))
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
        "--is_test", type=str, help="cantain test string while use test env"
    )
    args = parser.parse_args()

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

    round_robin_url = "http://202.63.35.230:8787/api/v1/tasks/"
    task_url = "http://202.63.35.230:8787/api/v1/tasks/"
    job_url = "http://202.63.35.230:8787/api/v1/jobs/"
    if args.is_test and "test" in args.is_test:
        round_robin_url = "http://164.90.76.189:8787/api/v1/tasks/"
        task_url = "http://164.90.76.189:8787/api/v1/tasks/"
        job_url = "http://164.90.76.189:8787/api/v1/jobs/"

    if args.srv_addr:
        task_url = args.srv_addr
        job_url = None

    try:
        rec = worker(
            job_conf_str,
            task_conf_str,
            job_dict,
            task_dict,
            job_url,
            task_url,
            round_robin_url,
        )
        sys.exit(rec)
    except Exception as e:
        print(e)
