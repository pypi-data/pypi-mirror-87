# -*- coding: UTF-8 -*-

"""
借助HDFS以及发布服务发布模型，不再使用FTP
copied from
https://git.sysop.bigo.sg/xulei/brec_build_service/blob/master/pub_tools_v1/update_resource_v3.py
with little modification
"""

import re
import os
import sys
import time
import json
import requests
import optparse
import subprocess
import logging
from typing import Text


TEST_SERVER = "139.5.110.64"
MAIN_SERVER_1 = "139.5.110.80"
MAIN_SERVER_2 = "139.5.110.75"
MAIN_SERVER_3 = "103.240.149.131"
INDIGO_SERVER = "103.240.148.124"
COMMON_SERVER = "103.240.148.137"

RELAY_SERVER = {
    "EU": "5.182.63.87",
    "US": "172.96.115.46",
}

PUBLISH_SERVERS = {
    "RANK_COLLECTION": MAIN_SERVER_1,
    "RECALL_COLLECTION": MAIN_SERVER_2,
    "OFFLINE_COLLECTION": MAIN_SERVER_3,
    "RANK_4RECALL_COLLECTION": MAIN_SERVER_3,
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


class PublishOptions(object):
    def __init__(
        self,
        processor: Text,
        collection: Text,
        name: Text,
        version: int,
        hdfs_src: Text = None,
        srv_ip: Text = None,
        extra_info: Text = None,
        local_src: Text = None,
        overseas: Text = None,
    ):

        assert bool(local_src) != bool(hdfs_src)
        self.srv_ip = srv_ip or COMMON_SERVER
        self.processor = processor or "DELIVER"
        self.collection = collection
        self.name = name
        self.version = version
        self.extra_info = extra_info
        self.hdfs_src = hdfs_src
        self.local_src = local_src
        self.overseas = overseas


def http_json_post(host, port, api, data_dict):
    data = json.dumps(data_dict)
    logging.info("POST http://%s:%d%s : %s" % (host, port, api, data))
    try:
        resp = requests.post(
            f"http://{host}:{port}/",
            headers={"Content-type": "application/json"},
            data=data,
        )
    except Exception as e:
        logging.error("fail to access service: %s", e)
        return None

    if resp.status_code != 200:
        logging.error("unexpected http code: %s", str(resp.status_code))
        return None
    try:
        return json.loads(resp.content)
    except ValueError:
        logging.error("unexpected response: %s", resp.content)
    return None


def hdfs_upload(local_src, hdfs_src):
    logging.info("upload: %s -> %s", local_src, hdfs_src)
    try:
        hdfs_dir = os.path.dirname(hdfs_src)
        assert 0 == subprocess.call(
            (HADOOP_BIN, "fs", "-mkdir", "-p", hdfs_dir)
        )
        assert 0 == subprocess.call(
            (HADOOP_BIN, "fs", "-chmod", "777", hdfs_dir)
        )
        assert 0 == subprocess.call(
            (HADOOP_BIN, "fs", "-put", local_src, hdfs_src)
        )
    except AssertionError as e:
        logging.error("hdfs upload failed with error: %s", e)
        return False
    return True


def do_publish(srv_ip, data, err_hint):
    resp = http_json_post(srv_ip, PUBLISH_SERVER_PORT, "/", data)
    if resp is None:
        logging.error("do publish failed!")
        return False
    if resp["code"] != 200:
        logging.error("Failed to publish, error: %s", resp["err_msg"])
        return False
    logging.info("publish successfully!")
    return True


def publish_resouce(options: PublishOptions):
    overseas_nodes = []
    if options.overseas is not None:
        for key in options.overseas.split(","):
            ip = RELAY_SERVER.get(key, None)
            if ip is None:
                logging.warning("area not found: %s", key)
                return False
            overseas_nodes.append((key, ip))

    if options.collection is None:
        logging.warning("collection is unset")
        return False
    elif PTN_STRICT_NAME.match(options.collection) is None:
        logging.warning("collection is illegal")
        return False

    if options.name is None:
        logging.warning("name is unset")
        return False
    elif PTN_STRICT_NAME.match(options.name) is None:
        logging.warning("name %s is illegal", options.name)
        return False

    if PTN_PLAIN_NAME.match(options.processor) is None:
        logging.warning("processor is illegal")
        return False

    if options.version is None:
        options.version = int(time.time())
    else:
        try:
            options.version = int(options.version)
            assert options.version != 0
        except BaseException:
            logging.warning("version is illegal")
            return False

    if options.processor == "DELIVER" and options.local_src is not None:
        # 允许使用local_src取代hdfs_src
        if not os.path.isdir(options.local_src):
            logging.warning("local_src should be directory")
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
        logging.warning("hdfs_src is unset")
        return False
    elif PTN_HDFS_ADDR.match(options.hdfs_src) is None:
        logging.warning("hdfs_src is illegal")
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
    if options.processor.endswith("-FORK"):
        data["processor"] = "FORK-RELAY"
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
