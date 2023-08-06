#!/bin/bash
function publish_postinfo() {
    task='{"namespace" : "like_recall","params" : {"data_name":"'${1}'","input_path":"'${2}'","args":"'${3}'"}}'
    echo "task : ${task}"
    curl -H "Content-Type:application/json" -X POST -d "${task}" 'http://43.224.67.124:8100/deliver_big_data'
    if [ $? -ne 0 ]; then
        echo "publish data failed"
        exit 1
    fi
}

if [ $1 == "local" ] && [ ! -d $2 ]; then
  echo "${2} is not a directory"
  exit 1
fi

hdfs_tmp_dir="hdfs://bigocluster/recommend/cannon_delivery_data"
hdfs_save_path=""
if [ $1 == "local" ]; then
  base_name=$(basename $2)
  hdfs_save_path="${hdfs_tmp_dir}/${base_name}"
  hadoop fs -test -e "${hdfs_save_path}"
  if [ $? -eq 0 ] ;then
    echo "${hdfs_save_path} exists, cann't publish"
    exit 1
  fi
  if [ $1 == "local" ]; then
    hadoop fs -put $2 ${hdfs_tmp_dir}
  fi
else
  hdfs_save_path=$2
fi

hadoop fs -test -e "${hdfs_save_path}"
if [ ! $? -eq 0 ] ;then
  echo "${hdfs_save_path} doesn't exists"
  exit 1
fi

hadoop fs -chmod 777 "${hdfs_save_path}"
if [ ! $? -eq 0 ] ;then
  echo "${hdfs_save_path} chmod failed"
  exit 1
fi

file_count=$(hadoop fs -ls ${hdfs_save_path} | wc -l)
if [ ${file_count} -le 2 ]; then
  echo "junk file" > .junk_file
  hadoop fs -put .junk_file ${hdfs_save_path}
  rm .junk_file
fi

publish_postinfo $3 ${hdfs_save_path} $4
