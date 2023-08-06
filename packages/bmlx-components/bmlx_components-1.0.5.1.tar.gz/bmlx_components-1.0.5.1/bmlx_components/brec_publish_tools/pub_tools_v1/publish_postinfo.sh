#!/bin/bash

CWD=$(dirname "$0")
ts_dir=$(cd $CWD;pwd)
if [[ ! $tools_dir ]] || [[ -z $tools_dir ]]; then
        export tools_dir=$ts_dir
fi

cannon_model_name=$1
cannon_input_path=$2
cannon_collection=$3
cannon_namespace=$4
creator=$5
data_phase=$6
publish_conf=$7
is_test=$(echo "$8" | grep "test")
addr="http://43.224.67.125:8100/deliver_data"
if [[ "${is_test}" != "" ]]; then
  addr="http://139.5.110.39:8100/deliver_data"
fi

python $ts_dir/cannon/cannon_publisher_v1.py --build_type=delivery --input_path=$cannon_input_path --data_name=$cannon_model_name \
                                           --collection=$cannon_collection --other_args=$publish_conf --srv_addr=$addr --namespace=$cannon_namespace \
                                           --is_test=$is_test  --creator=$creator --phase=$data_phase
if [ $? -ne 0 ];then echo "Error : publish $cannon_model_name failed!";exit 1;fi

echo "publish postinfo success"
