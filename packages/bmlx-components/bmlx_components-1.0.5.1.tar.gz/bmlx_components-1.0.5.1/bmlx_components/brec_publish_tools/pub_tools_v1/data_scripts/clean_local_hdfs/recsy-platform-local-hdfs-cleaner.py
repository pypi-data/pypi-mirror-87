from datetime import datetime, timedelta

import airflow
from airflow import DAG
from operators.hdfs_docker_operator import HDFSDockerOperator

from functools import partial
from hooks.callback_util import task_status_notify_by_wechat

default_args = {
    "owner": "xiongchenyu",
    "depends_on_past": False,
    "start_date": "2020-09-08 11:43:00+08:00",
    "email": ["xiongchenyu@bigo.sg"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=60),
    "queue": "default_spark"
    #   'on_success_callback': partial(task_status_notify_by_wechat, 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=79ccc046-dace-4962-a6e8-faf434965588'),
    #   'on_failure_callback': partial(task_status_notify_by_wechat, 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=79ccc046-dace-4962-a6e8-faf434965588', ['18010159753'])
}

dag = DAG(
    "recsy-platform-local-hdfs-cleaner",
    default_args=default_args,
    description="recsy-platform-local-hdfs-cleaner",
    schedule_interval=timedelta(hours=1),
    max_active_runs=1,
    catchup=False,
)

task1 = HDFSDockerOperator(
    task_id="recsy-platform-local-hdfs-cleaner",
    hdfs_conn_id="bigdata_hdfs",
    api_version="1.25",
    image="harbor.bigo.sg/bigdata/likee_recall_hot:latest",
    docker_conn_id="bigo_docker_hub",
    volumes=["/recommend/platform/clean_local_hdfs:/workspace/clean_local_hdfs"],
    command="cd /workspace/clean_local_hdfs && python3 clean_local_hdfs.py",
    network_mode="host",
    exec_user="hdfs",
    auto_remove=True,
    force_pull=True,
    dag=dag,
)
