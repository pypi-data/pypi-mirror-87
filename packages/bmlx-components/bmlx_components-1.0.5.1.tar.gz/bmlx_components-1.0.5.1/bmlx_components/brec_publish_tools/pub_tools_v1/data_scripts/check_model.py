#!/usr/bin/env python3

import http.client
import json
import argparse
from datetime import datetime

TOKEN = "access_token=eyJJbmZvIjoiZXlKVmMyVnlJam9pY205aWIzUXhJaXdpUlhod2FYSmhkR2x2YmtSaGRHVWlPams1T1RZMk1qazRNamw5IiwiSG1hYyI6Ik54ajBUcEhubGo1OFIxWkxWNFRaOVh1cUJyaHRDTVd1STlRWkpoWUd3bjg9In0="

parser = argparse.ArgumentParser()
parser.add_argument("--product", dest="product", default="likee")
parser.add_argument("--app", dest="app", default="recall")
parser.add_argument(
    "-d",
    "--destination",
    choices=["hk", "sg"],
    type=str,
    default="hk",
    help="destination data center",
)

options = parser.parse_args()
try:
    conn = http.client.HTTPConnection("ceto.recsys.bigo.inner", 8888)
    if options.destination == "sg":
        conn = http.client.HTTPConnection("sg.ceto.recsys.bigo.inner", 8888)
    headers = {"Content-type": "application/json", "Cookie": TOKEN}
    conn.request(
        "GET",
        "/api/v1/"
        + options.product
        + "/"
        + options.app
        + "/datas?ns="
        + options.product
        + "_"
        + options.app
        + "&page_num=0&page_size=1000&data_type=model",
        "",
        headers,
    )
    resp = conn.getresponse()
    data = json.loads(resp.read())
    for model in [
        (
            x["name"],
            x["revisions"][0]["version"],
            datetime.fromtimestamp(float(x["revisions"][0]["version"])).strftime(
                "%m/%d/%Y, %H:%M:%S"
            ),
        )
        for x in data["data"]["list"]
    ]:
        print(model)
    conn.close()
except BaseException as e:
    print("fail to access service: ", e)
