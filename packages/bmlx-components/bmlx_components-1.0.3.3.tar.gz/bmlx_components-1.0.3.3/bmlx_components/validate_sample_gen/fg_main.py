"""
在同一个进程中同时 import feature_processor 和 import google.protobuf.pyext._message ，会有莫名其妙的错误。
所以将 feature process 放到单独的进程中来进行
"""
import os
import sys
import base64
import zlib
import logging
from optparse import OptionParser


def parse_featurelog_line(line):
    if line.startswith("22222"):
        return None
    parts = line.strip(" \r\n").split("\t")
    try:
        compressed_bytes = base64.b64decode(parts[-1])
    except Exception as e:
        logging.error("Failed to decode base64 featurelog, exception: %d", e)
        return None
    if parts[4].endswith("#1"):
        origin_bytes = zlib.decompress(compressed_bytes)
    else:
        origin_bytes = compressed_bytes
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

    sys.path.insert(0, options.fg_dir)
    import feature_processor

    processor = feature_processor.FeatureProcessorExt()
    if processor.init(
        [("bmlx-feature-processor", os.path.join(options.fg_dir, "fg.yaml"), 2)]
    ):
        raise RuntimeError("Failed to init feature processor")

    with open(options.processed_samples_path, "wb") as processed_fp:
        with open(options.origin_samples_path, "r") as origin_fp:
            for line in origin_fp.readlines():
                origin_bytes = parse_featurelog_line(line)
                if not origin_bytes:
                    continue

                processed_ret = processor.process_for_xdl(
                    feature_stream=origin_bytes,
                    json_format=False,
                    base64_encoded=False,
                )
                processed_fp.write(processed_ret)
