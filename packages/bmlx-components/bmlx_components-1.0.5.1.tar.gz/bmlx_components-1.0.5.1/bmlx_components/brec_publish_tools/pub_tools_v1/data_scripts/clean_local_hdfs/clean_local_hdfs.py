#! /usr/bin/python3
#
#
import re
import subprocess
import sys
import argparse

MAX_VERSION = 5

HADOOP_BIN = "/usr/bin/hadoop"

FOLDER_PREFIX = "/data/models"

HDFS_PREFIX_JJA = "hdfs://jjalhcluster" + FOLDER_PREFIX

HDFS_PREFIX_DP = "hdfs://dplhcluster" + FOLDER_PREFIX

HDFS_PREFIX_QW = "hdfs://qwlhcluster" + FOLDER_PREFIX

FAILED_TO_LIST_DIRECTORY_MSG = "No such file or directory"


class HdfsException(Exception):
    pass


def hdfs_delete(hdfs_base_src, conf, target):
    print(("async delete folder: ", HDFS_PREFIX_JJA + hdfs_base_src))
    try:
        if target == "hk":
            dp = subprocess.Popen(
                (HADOOP_BIN, "fs", "-rmr", HDFS_PREFIX_DP + hdfs_base_src),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            jja = subprocess.Popen(
                (HADOOP_BIN, "fs", "-rmr", HDFS_PREFIX_JJA + hdfs_base_src),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            qw = subprocess.Popen(
                (HADOOP_BIN, "fs", "-rmr", HDFS_PREFIX_QW + hdfs_base_src),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            dp.wait(),
            jja.wait()
            qw.wait()
    except AssertionError:
        print("=== fail ===")
        return False
    return True


def clean_hdfs_models_version(model_path):
    folders = hdfs_ls(HDFS_PREFIX_JJA + model_path)
    versions = list([int(re.findall(r"\d+", x.split("/")[-1])[0]) for x in folders])
    print(versions)
    if len(versions) > MAX_VERSION:
        versions.sort()
        old_versions = versions[:-(MAX_VERSION)]
        for old_version in old_versions:
            to_be_removed = model_path + "/" + str(old_version)
            print(("start to delete folder :", to_be_removed))
            hdfs_delete(to_be_removed)


"""
1. list out ns in /data/models foler
2. traverse all model in every ns
3. traverse all version in model
4. keep latest 5 version
5. remove others
6. finish
"""


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-t", "--target", default="hk")
    args = arg_parser.parse_args()
    for ns_path in hdfs_ls(HDFS_PREFIX_JJA):
        ns = ns_path.split("/")[-1]
        ns_hdfs_path = HDFS_PREFIX_JJA + "/" + ns
        for model_path in hdfs_ls(ns_hdfs_path):
            model = model_path.split("/")[-1]
            model_hdfs_base_path = "/" + ns + "/" + model
            clean_hdfs_models_version(model_hdfs_base_path)

    print("finished clean up, see you next time")
    return True


if __name__ == "__main__":
    if not main():
        sys.exit(1)
