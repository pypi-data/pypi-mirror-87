import optparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from functools import partial

import airflow
from airflow import DAG
from airflow.utils.dates import days_ago

from hooks.callback_util import task_status_notify_by_wechat
from operators.hdfs_docker_operator import HDFSDockerOperator

default_args = {
    "owner": "xiongchenyu",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["xiongchenyu@bigo.sg"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=60),
    "queue": "bigdata"
    #   'on_success_callback': partial(task_status_notify_by_wechat, 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=79ccc046-dace-4962-a6e8-faf434965588'),
    #   'on_failure_callback': partial(task_status_notify_by_wechat, 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=79ccc046-dace-4962-a6e8-faf434965588', ['18010159753'])
}

dag = DAG(
    dag_id="xdl_build_and_upload_airflow_trigger_controller",
    default_args=default_args,
    start_date=days_ago(2),
    schedule_interval=timedelta(minutes=1),
    max_active_runs=1,
    catchup=False,
)

task1 = HDFSDockerOperator(
    task_id="xdl_build_and_upload_airflow_trigger_controller",
    hdfs_conn_id="bigdata_hdfs",
    api_version="1.25",
    image="harbor.bigo.sg/bigdata/likee_recall_hot:latest",
    docker_conn_id="bigo_docker_hub",
    volumes=[
        "/recommend/platform:/workspace/platform",
        "/recommend/xdl_build_and_upload_airflow:/xdl",
    ],
    command="cd /workspace/platform/xdl_to_platform && python xdl_to_platform_multi.py",
    network_mode="host",
    exec_user="hdfs",
    auto_remove=True,
    force_pull=True,
    dag=dag,
)
