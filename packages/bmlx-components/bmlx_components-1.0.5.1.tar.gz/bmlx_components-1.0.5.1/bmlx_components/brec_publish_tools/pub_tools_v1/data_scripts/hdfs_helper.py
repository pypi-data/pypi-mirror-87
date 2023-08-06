#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import logging

HADOOP_BIN = "/usr/bin/hadoop"

FOLDER_PREFIX = "/data/models"

XDL_FOLDER_PREFIX = "/user/hadoop/dispatching/models"

HDFS_PREFIX = "hdfs://bigocluster" + FOLDER_PREFIX

HDFS_PREFIX_DP = "hdfs://dplhcluster" + FOLDER_PREFIX

HDFS_PREFIX_JJA = "hdfs://jjalhcluster" + FOLDER_PREFIX

HDFS_PREFIX_QW = "hdfs://qwlhcluster" + FOLDER_PREFIX

fpath = os.path.dirname(os.path.abspath(__file__))

HK_CONF = fpath + "/hk_hdfs_conf"
SG_CONF = fpath + "/sg_hdfs_conf"

FAILED_TO_LIST_DIRECTORY_MSG = "No such file or directory"

logger = logging.getLogger("hdfs helper")


class HdfsException(Exception):
    pass


def asyncUploadHdfs(src, local_src):
    base = os.path.dirname(src)

    def inner(prefix, conf):
        assert 0 == subprocess.call(
            (
                HADOOP_BIN,
                "--config",
                conf,
                "fs",
                "-mkdir",
                "-p",
                prefix + base,
            )
        )
        assert 0 == subprocess.call(
            (
                HADOOP_BIN,
                "--config",
                conf,
                "fs",
                "-chmod",
                "777",
                prefix + base,
            )
        )
        return subprocess.Popen(
            (
                HADOOP_BIN,
                "--config",
                conf,
                "fs",
                "-put",
                local_src,
                prefix + src,
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    return inner


def hdfs_upload(local_src, src, dest):
    print("upload:", local_src, "->", src)
    uploader = asyncUploadHdfs(src, local_src)
    uploaders = []
    try:
        if "hk" in dest:
            dp = uploader(HDFS_PREFIX_DP, HK_CONF)
            uploaders.append(dp)
            jja = uploader(HDFS_PREFIX_JJA, HK_CONF)
            uploaders.append(jja)
            qw = uploader(HDFS_PREFIX_QW, HK_CONF)
            uploaders.append(qw)
        if "sg" in dest:
            sg = uploader(HDFS_PREFIX, SG_CONF)
            uploaders.append(sg)
        returnCodeList = map(lambda x: x.wait(), uploaders)
        return not any(returnCodeList)
    except AssertionError:
        print("=== fail ===")
        return False


def hdfs_ls(dirname, conf):
    """Returns list of HDFS directory entries."""
    print("Listing HDFS directory " + dirname)
    proc = subprocess.Popen(
        ["hdfs", "--config", conf, "dfs", "-ls", dirname],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (out, err) = proc.communicate()
    if out:
        print("stdout:\n", out)
    if proc.returncode != 0:
        errmsg = (
            'Failed to list HDFS directory "'
            + dirname
            + '", return code '
            + str(proc.returncode)
        )
        logger.error(errmsg)
        logger.error(err)
        if not FAILED_TO_LIST_DIRECTORY_MSG in str(err):
            raise HdfsException(errmsg)
        return []
    elif err:
        print("stderr:\n", err)
    return out.splitlines()


def hdfs_get(hdfs_src, target_location, conf):
    print("download from :", hdfs_src, "to", target_location)
    try:
        assert 0 == subprocess.call(("rm", "-rf", target_location))
        assert 0 == subprocess.call(
            (HADOOP_BIN, "--config", conf, "fs", "-get", hdfs_src, target_location)
        )
    except AssertionError:
        print("=== fail ===")
        return False
    return True


def hdfs_du(dirname, conf):
    proc = subprocess.Popen(
        ["hadoop", "--config", conf, "fs", "-du", "-s", dirname],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (out, err) = proc.communicate()
    if out:
        print("stdout:\n", out)
    if proc.returncode != 0:
        errmsg = (
            'Failed to du HDFS directory "'
            + dirname
            + '", return code '
            + str(proc.returncode)
        )
        logger.error(errmsg)
        logger.error(err)
        return 10010
    return int(out.decode("utf-8").split(" ")[0])


def hdfs_distcp(src, dest):
    print("distcp from :", src, "to", dest)
    try:
        assert 0 == subprocess.call(
            (HADOOP_BIN, "--config", SG_CONF, "distcp", "-p=rbcaxt", src, dest)
        )
    except AssertionError:
        print("=== distcp fail ===")
        return False
    return True


# if __name__ == "__main__":
#     print(hdfs_du("hdfs://jjalhcluster/data/", HK_CONF))
