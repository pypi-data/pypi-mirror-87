"""
在同一个进程中同时 import feature_processor 和 import google.protobuf.pyext._message ，会有莫名其妙的错误。
所以将 feature process 放到单独的进程中来进行
"""
import os
import sys
import base64
import zlib
import logging
import struct
from optparse import OptionParser
from ctypes import cdll


def parse_featurelog_line(line):
    try:
        compressed_bytes = base64.b64decode(line)
    except Exception as e:
        logging.error("Failed to decode base64 featurelog, exception: %d", e)
        return None

    origin_bytes = zlib.decompress(compressed_bytes)

    return origin_bytes


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--fg_dir", dest="fg_dir", type=str)
    parser.add_option(
        "--origin_samples_path", dest="origin_samples_path", type=str
    )
    parser.add_option(
        "--processed_samples_path", dest="processed_samples_path", type=str
    )
    (options, args) = parser.parse_args()

    # import fg so
    sys.path.insert(0, options.fg_dir)
    cdll.LoadLibrary(os.path.join(options.fg_dir, "libfg_operators.so"))
    import fglib_py3 as fglib_py

    processor = fglib_py.PyFeatureGenerator()
    # Create, succeed if return not 0
    fg_client = processor.Create()
    if fg_client == 0:
        raise RuntimeError("processor Create failed")

    ret = processor.InitOnce(
        fg_client,
        os.path.join(options.fg_dir, "fg.yaml"),
        "./demo.log",
        0,
        "",
        False,
    )
    if ret != 0:
        raise RuntimeError("processor InitOnce failed")

    with open(options.processed_samples_path, "wb") as processed_fp:
        with open(options.origin_samples_path, "r") as origin_fp:
            for line in origin_fp.readlines():
                origin_bytes = parse_featurelog_line(line)
                if not origin_bytes:
                    continue

                processed_ret = processor.ProcessFeatureLog(
                    fg_client, origin_bytes, False, False,
                )
                # 新数据流的格式...
                processed_fp.write(
                    struct.pack("<Q", len(processed_ret))
                )  # length = len(processed_ret)
                processed_fp.write(bytes(4))  # crc32(length)
                processed_fp.write(processed_ret)
                processed_fp.write(bytes(4))  # crc32(processed_ret)

    ret = processor.Release(fg_client)
    if ret != 0:
        raise RuntimeError("processor Release failed")
