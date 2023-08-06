# loop check location

# list out files
# read files
# xdl_to_platform
# delete files
# write xxxx_complete y/n

# exit when xxx empty

import os, sys, subprocess, optparse, time

sys.path.append(os.path.join(sys.path[0], os.pardir))
from update_resource_k8s import *
from multiprocessing import Process

HADOOP_BIN = "/usr/bin/hadoop"
directory = "/xdl/"
postfix = ".complete"


def process(filename, path, HDFS_PREFIX):
    status = "y"
    try:
        file = open(path, "r")
        line = file.readline()
        s = line.split(":", 1)
        ns = s[0]
        hdfs_src = s[1].rstrip()

        split_path = hdfs_src.split("/")

        location = sys.path[0] + "/" + filename + split_path[-1]
        hdfs_get(hdfs_src, location, HK_CONF)
        try:
            assert 0 == subprocess.call(
                ("bash", sys.path[0] + "/emb-index.sh", sys.path[0], location)
            )
            if upload_and_sync(ns, location, filename, int(time.time()), "hk"):
                assert 0 == subprocess.call(("rm", "-rf", location))
        except AssertionError:
            print("=== fail ===")
            return False
        status_file = directory + filename + postfix
        f = open(status_file, "w+")
        f.write(status)
        f.close()

        os.remove(directory + filename)
        assert 0 == subprocess.call((HADOOP_BIN, "fs", "-rm", HDFS_PREFIX + filename))
        assert 0 == subprocess.call(
            (HADOOP_BIN, "fs", "-put", status_file, HDFS_PREFIX)
        )
    except:
        status = "n"
        status_file = directory + filename + postfix
        f = open(status_file, "w+")
        f.write(status)
        f.close()
        os.remove(directory + filename)
        assert 0 == subprocess.call((HADOOP_BIN, "fs", "-rm", HDFS_PREFIX + filename))
        assert 0 == subprocess.call(
            (HADOOP_BIN, "fs", "-put", status_file, HDFS_PREFIX)
        )


def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    # Put some work in the queue

    parser = optparse.OptionParser()
    parser.add_option("--folder", dest="folder", default="xdl_build_and_upload_airflow")

    options, args = parser.parse_args()
    HDFS_PREFIX = "hdfs://bigocluster/recommend/" + options.folder + "/"
    pl = []
    for filename in os.listdir(directory):
        if not filename.endswith(".complete"):
            path = os.path.join(directory, filename)
            p = Process(
                target=process,
                args=(filename, path, HDFS_PREFIX),
            )
            pl.append(p)
    list([x.start() for x in pl])
    list([x.join() for x in pl])
    print("finish")
    return True


if __name__ == "__main__":
    if not main():
        sys.exit(1)
