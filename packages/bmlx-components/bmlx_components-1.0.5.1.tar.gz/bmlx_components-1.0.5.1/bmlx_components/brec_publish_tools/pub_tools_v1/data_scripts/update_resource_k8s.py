#!/usr/bin/env python3

import argparse
import http.client
import json
import logging
import os
import sys
import time
import logging
from hdfs_helper import *

TOKEN = "access_token=eyJJbmZvIjoiZXlKVmMyVnlJam9pY205aWIzUXhJaXdpUlhod2FYSmhkR2x2YmtSaGRHVWlPams1T1RZMk1qazRNamw5IiwiSG1hYyI6Ik54ajBUcEhubGo1OFIxWkxWNFRaOVh1cUJyaHRDTVd1STlRWkpoWUd3bjg9In0="


logger = logging.getLogger("update resource k8s")


def upload_data_to_platform_json_builder(name, path, ns, version, size):
    return {
        "name": name,
        "path": path,
        "ns": ns,
        "version": version,
        "type": "model",
        "size": size,
    }


def http_json_post(host, port, api, data, is_auth=False):
    data = json.dumps(data)
    print("POST http://%s:%d%s : %s" % (host, port, api, data))
    try:
        conn = http.client.HTTPConnection(host, port)
        if is_auth:
            headers = {"Content-type": "application/json", "Cookie": TOKEN}
        else:
            headers = {"Content-type": "application/json"}
        conn.request("POST", api, data, headers)
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
    except BaseException as e:
        print("fail to access service: ", e)
        return None
    if resp.status != 200:
        print("unexpected http code: " + str(resp.status))
        return None
    try:
        return json.loads(data.decode("utf-8"))
    except ValueError:
        print("unexpected response: ", data)
    return None


def sync(ns, name, version, dest):
    """
    sync data to k8s
    """
    try:
        publish = publishToCetos(ns, name, version)
        if "hk" in dest:
            if not publish("ceto.recsys.bigo.inner"):
                return False
        if "sg" in dest:
            publish("sg.ceto.recsys.bigo.inner")
    except AssertionError:
        return False
    print("success")
    return True


def upload_and_sync(ns, local_src, name, version, dest):

    src = "/%s/%s/%d" % (ns, name, version)

    """
    upload data to localhdfs
    """
    if local_src is not None:
        if not os.path.isdir(local_src):
            print("local_src should be directory")
            return False
        if not os.listdir(local_src):
            print("local_src have no files")
            return False
        if not hdfs_upload(local_src, src, dest):
            return False
    else:
        print("not local src")
        return False
    return sync(ns, name, version, dest)


def publishToCetos(ns, name, version):
    def inner(baseUrl):
        src = "%s/%s/%s/%d" % (FOLDER_PREFIX, ns, name, version)
        print(
            "sync to k8s",
            "with src location: ",
            src,
            "for ns: ",
            ns,
            "for server: ",
            baseUrl,
        )
        reps = http_json_post(
            baseUrl,
            8888,
            "/openapi/v1/update_model",
            upload_data_to_platform_json_builder(
                name, src, ns, version, hdfs_du("hdfs://dplhcluster" + src, HK_CONF)
            ),
            True,
        )
        if not reps["errno"] == "1000000":
            print("fail to sync data to k8s platform")
            return False
        return True

    return inner


def main():

    """
    1. check if is in hdfs
    2. if not exist upload local_src to hdfs
    3. sync to localhdfs
    4. sync to k8s platform
    """

    parser = argparse.ArgumentParser(
        description="Upload model to ceto platform \n",
        epilog="""
    Example Usage:

    Publish model from local to hk and sg cetos:

    update_resource_k8s.py -n=bayes_all --ns=rtp_model-test ../bayes_all

    Publish model from hk hdfs cluster with xdl preprocessor to hk and sg cetos:

    update_resource_k8s.py -p=XDL --ns=likee_imo-ws-offline --name=name -s=hk hdfs://bigo-rt/user/rec_imo_rank/indigo_ws/xdl_output_model/ws_multi_v1_new_nl/2020082814

    Publish model from local with xdl preprocessor to hk and sg cetos:

    update_resource_k8s.py -p=XDL --ns=likee_imo-ws-offline --name=name ./2020082814
    """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("path", type=str, help="local or remote model folder path")

    parser.add_argument(
        "-s",
        "--source",
        choices=["hk", "sg", "local"],
        type=str,
        default="local",
        help="where is model, it can be located at local or hk/sg hdfs",
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

    parser.add_argument(
        "--ns",
        "--namespace",
        required=True,
        help="cetos namespace, such likee_recall, rtp_model",
    )

    parser.add_argument("-n", "--name", required=True, help="model name")
    parser.add_argument(
        "-v",
        "--version",
        type=int,
        default=int(time.time()),
        help="model version(default is current timestamp)",
    )

    parser.add_argument(
        "-p",
        "--preprocessor",
        choices=["XDL", "NONE"],
        help="use preprocessor to process the data before uploading(default is NONE)",
        default="NONE",
    )

    parser.add_argument(
        "-l",
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (defult is WARNING)",
        default=logging.WARNING,
    )

    args = parser.parse_args()

    logging.basicConfig(level=args.log)

    # prepare source
    split_path = args.path.split("/")
    location = os.getcwd() + "/" + args.name + split_path[-1]
    if args.source == "hk":
        hdfs_get(args.path, location, HK_CONF)
        args.path = location
    elif args.source == "sg":
        hdfs_get(args.path, location, SG_CONF)
        args.path = location

    if args.preprocessor == "XDL":
        try:
            assert 0 == subprocess.call(
                ("bash", sys.path[0] + "/emb-index.sh", sys.path[0], args.path)
            )
            if upload_and_sync(
                args.ns, args.path, args.name, args.version, args.destination
            ):
                assert 0 == subprocess.call(("rm", "-rf", args.path))
        except AssertionError:
            print("=== fail ===")
            return False
        return True
    else:
        logger.info(args)
        return upload_and_sync(
            args.ns, args.path, args.name, args.version, args.destination
        )


if __name__ == "__main__":
    if not main():
        sys.exit(1)
