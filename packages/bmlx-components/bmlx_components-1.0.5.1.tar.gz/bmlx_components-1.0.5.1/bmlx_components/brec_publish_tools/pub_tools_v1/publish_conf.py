import sys
import requests
import json
import threading
import time
import random
import argparse
import http.client, yaml

HOST = 'config-sys.internal.bigo.sg'
PORT = 80
TOKEN = '1555301612345'
API = '/a/config/batchCUAndPublish'

def get_version(guardian_addr, data_name):
    payload = {'name': data_name, 'min_version': '-1', 'phase': 'intermediate'}
    i = 0
    ver = 0
    while i < 61:
        i = i + 1
        now_time = int(time.time())
        r = requests.get(guardian_addr, params=payload)
        print("try " + str(i) + " times")
        print(r.text)
        res_json = r.json()
        if len(res_json['data']) != 1:
            print ("result data not equal 1")
            time.sleep(60)
            continue
        data = res_json['data'][0]
        ver = data['version']
        if now_time - ver > 2000:
            print("version is too old, " + str(ver))
            time.sleep(60)
            continue
        else:
            break
    if i > 60:
        return None
    return str(ver)

def change_conf(host, api):
    #print(host)
    #print(api)
    port = 8100
    headers = {
        'Content-type': 'text/plain'
    }
    conn = http.client.HTTPConnection(host, port, 8)
    conn.request('POST', api, '', headers)
    resp = conn.getresponse()
    conn.close()
    if not resp or resp.status != 200:
        print ("Error resp : " + resp.read())


parser = argparse.ArgumentParser()
parser.add_argument("--data_name", type = str, help = "data name")
parser.add_argument("--version", type = str, help = "data version")
parser.add_argument("--send_conf", type = str, help = "whether send conf to config center")
parser.add_argument("--test", type = str, help = "whether is test env")
args = parser.parse_args()

try:
    data_name = args.data_name
    send_conf = args.send_conf
    test = args.test
    if not data_name:
        print ("No data_name")
        sys.exit(1)

    guardian_addr = "http://43.224.67.124:8787/api/v1/datas/"
    build_host = "43.224.67.124"
    if args.test and "test" in args.test:
        guardian_addr = "http://164.90.76.189:8787/api/v1/datas/"
        build_host = "139.5.110.39"

    version = None

    if args.version:
        version = args.version
    else:
        version = get_version(guardian_addr, data_name)

    if not version:
        print('version is null')
        sys.exit(1)

    #change data status in cannon
    api = "/change_data/?name=" + data_name + "&version=" + version + "&phase=final&send_conf=" + send_conf
    change_conf(build_host,api)
    print("change data " + data_name + ", version " + version + " success")

except Exception as e:
    print(e)
