import requests
import json
import logging

TOKEN = "access_token=eyJJbmZvIjoiZXlKVmMyVnlJam9pY205aWIzUXhJaXdpUlhod2FYSmhkR2x2YmtSaGRHVWlPams1T1RZMk1qazRNamw5IiwiSG1hYyI6Ik54ajBUcEhubGo1OFIxWkxWNFRaOVh1cUJyaHRDTVd1STlRWkpoWUd3bjg9In0="
HK_CETO_UPDATE_MODEL_URL = (
    "http://ceto.recsys.bigo.inner:8888/openapi/v1/update_model"
)
SG_CETO_UPDATE_MODEL_URL = (
    "http://sg.ceto.recsys.bigo.inner:8888/openapi/v1/update_model"
)


def publish_model_to_ceto(name, namespace, version, path, is_hk=False):
    headers = {"Content-type": "application/json", "Cookie": TOKEN}
    payload = {
        "name": name,
        "path": path,
        "ns": namespace,
        "version": version,
        "type": "model",
        "size": 11010,
    }
    resp = requests.post(
        HK_CETO_UPDATE_MODEL_URL if is_hk else SG_CETO_UPDATE_MODEL_URL,
        headers=headers,
        data=json.dumps(payload),
    )
    logging.info(
        "post meta to k8s, request header: %s, request payload: %s, resp: %s",
        headers,
        payload,
        resp.text,
    )
    if resp.status_code != requests.codes.ok:
        raise RuntimeError("Failed to post meta to k8s")
    resp_dict = json.loads(resp.content)
    if resp_dict["errno"] != "1000000":
        logging.error(
            "Failed to sync data to k8s platform, errno: %s", resp_dict["errno"]
        )
        return False
    return True
