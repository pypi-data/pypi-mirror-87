#!/usr/bin/env python3

import http.client
import json
import argparse
import os
import re
import subprocess
import sys
import time

TEST_SERVER = "139.5.110.64"
MAIN_SERVER_1 = "139.5.110.80"
MAIN_SERVER_2 = "139.5.110.75"
INDIGO_SERVER = "103.240.148.124"
COMMON_SERVER = "103.240.148.137"

RELAY_SERVER = {"EU": "5.182.63.87", "US": "172.96.115.46", "SG": "169.136.115.2"}

PUBLISH_SERVERS = {
    "RANK_COLLECTION": MAIN_SERVER_1,
    "RECALL_COLLECTION": MAIN_SERVER_2,
    "INDIGO_RANK_COLLECTION": INDIGO_SERVER,
    "INDIGO_RECALL_COLLECTION": INDIGO_SERVER,
    "LIVE_RANK_COLLECTION": COMMON_SERVER,
    "LIVE_RECALL_COLLECTION": COMMON_SERVER,
}

PUBLISH_SERVER_PORT = 8997

HADOOP_BIN = "/usr/bin/hadoop"
HDFS_PREFIX = "hdfs://bigocluster/user/hadoop/dispatching/models"

PTN_HDFS_ADDR = re.compile("^hdfs://[0-9a-zA-Z-_\.,/]+$")
PTN_STRICT_NAME = re.compile("^[0-9a-zA-Z_]+$")
PTN_PLAIN_NAME = re.compile("^[0-9a-zA-Z-_]+$")


def http_json_post(host, port, api, data):
    data = json.dumps(data)
    print(("POST http://%s:%d%s : %s" % (host, port, api, data)))
    try:
        conn = http.client.HTTPConnection(host, port)
        headers = {"Content-type": "application/json"}
        conn.request("POST", api, data, headers)
        resp = conn.getresponse()
        data = resp.read().decode("utf-8")
        conn.close()
    except BaseException as e:
        print(("fail to access service: ", e))
        return None
    if resp.status != 200:
        print(("unexpected http code: " + str(resp.status)))
        return None
    try:
        return json.loads(data)
    except ValueError:
        print(("unexpected response: ", data))
    return None


def hdfs_upload(local_src, hdfs_src):
    print(("upload:", local_src, "->", hdfs_src))
    try:
        hdfs_dir = os.path.dirname(hdfs_src)
        assert 0 == subprocess.call((HADOOP_BIN, "fs", "-mkdir", "-p", hdfs_dir))
        assert 0 == subprocess.call((HADOOP_BIN, "fs", "-chmod", "777", hdfs_dir))
        assert 0 == subprocess.call((HADOOP_BIN, "fs", "-put", local_src, hdfs_src))
    except AssertionError:
        print("=== fail ===")
        return False
    return True


def do_publish(srv_ip, data, err_hint):
    resp = http_json_post(srv_ip, PUBLISH_SERVER_PORT, "/", data)
    if resp is None:
        return False
    try:
        if resp["code"] != 200:
            print((err_hint, resp["err_msg"]))
            return False
    except KeyError:
        print(("unexpected response:", resp))
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--srv_ip", dest="srv_ip")
    parser.add_argument("--processor", dest="processor", default="DELIVER")
    parser.add_argument("--collection", required=True, dest="collection")
    parser.add_argument("-n", "--name", required=True, help="model name")
    parser.add_argument(
        "-v",
        "--version",
        type=int,
        default=int(time.time()),
        help="model version(default is current timestamp)",
    )
    parser.add_argument("--extra_info", dest="extra_info")
    parser.add_argument("--hdfs_src", dest="hdfs_src")
    parser.add_argument("--local_src", dest="local_src")
    parser.add_argument("--overseas", dest="overseas")

    options = parser.parse_args()

    overseas_nodes = []
    if options.overseas is not None:
        for key in options.overseas.split(","):
            ip = RELAY_SERVER.get(key, None)
            if ip is None:
                print(("area not found: ", key))
                return False
            overseas_nodes.append((key, ip))

    if PTN_STRICT_NAME.match(options.collection) is None:
        print("collection is illegal")
        return False

    if PTN_STRICT_NAME.match(options.name) is None:
        print("name is illegal")
        return False

    if PTN_PLAIN_NAME.match(options.processor) is None:
        print("processor is illegal")
        return False

    if options.processor == "DELIVER" and options.local_src is not None:
        # 允许使用local_src取代hdfs_src
        if not os.path.isdir(options.local_src):
            print("local_src should be directory")
            return False
        options.hdfs_src = "%s/%s/%s/%d" % (
            HDFS_PREFIX,
            options.collection,
            options.name,
            options.version,
        )
        if not hdfs_upload(options.local_src, options.hdfs_src):
            return False

    if options.hdfs_src is None:
        print("hdfs_src is unset")
        return False
    elif PTN_HDFS_ADDR.match(options.hdfs_src) is None:
        print("hdfs_src is illegal")
        return False

    data = {
        "processor": options.processor,
        "collection": options.collection,
        "name": options.name,
        "version": options.version,
        "hdfs_src": options.hdfs_src,
    }

    if options.extra_info is not None:
        data["extra_info"] = options.extra_info

    if options.srv_ip is None:
        srv_ip = PUBLISH_SERVERS.get(options.collection, COMMON_SERVER)
    else:
        srv_ip = options.srv_ip

    if not do_publish(srv_ip, data, "publish fail:"):
        return False

    done = True
    data["processor"] = "RELAY"
    if options.processor != "DELIVER":
        data["hdfs_src"] = "%s/%s/%s/%d" % (
            HDFS_PREFIX,
            options.collection,
            options.name,
            options.version,
        )
    for area, ip in overseas_nodes:
        data["collection"] = "_".join((options.collection, area))
        if not do_publish(ip, data, area + " relay fail:"):
            done = False

    return done


if __name__ == "__main__":
    if not main():
        sys.exit(1)
