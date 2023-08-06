#!/bin/bash

online_meta_url="http://164.90.76.180:6210/CycloneMetaService/GetModelDeployInfo"
test_meta_url="http://103.43.87.118:6210/CycloneMetaService/GetModelDeployInfo"

function check_input_path()
{
    hadoop fs -test -e "${1}"
    if [ $? -ne 0 ]
    then
      echo "Error: input path doesn't exists, ${1}"
      exit 1
    fi

    size=$(hadoop fs -du -s ${1} | awk '{print $1}')
    echo ${size}
    if [ ${size} -lt 0 ]
    then
      echo "Error: input path size is ${size}, too small"
      exit 1
    fi
}

function check_model()
{
    cyclone_model_name="${1}"
    cyclone_model_version="${2}"
    url=""
    is_test=$(echo $3 | grep 'test')
    if [ -z "$is_test" ]; then
        url=$online_meta_url
    else
        url=$test_meta_url
    fi
    echo "model name: ${cyclone_model_name}, version: ${cyclone_model_version}, url: ${url}"
    rest_retry_times=720 #最长配送1h，如果还没完成则退出报警
    while [ $rest_retry_times -gt 0 ]
    do
        result=`curl $url -d '{"model_name":"'${cyclone_model_name}'","model_version":"'${cyclone_model_version}'"}'`
        check_result=$(echo $result | grep '"status":"OK"')
        if [ -z "$check_result" ]; then
            echo "Round-robin querying cyclone ..."
            sleep 10s
        else
            echo "get model success from cyclone, name: ${cyclone_model_name}, version: ${cyclone_model_version}"
            return 0
        fi
        let "rest_retry_times--"
    done

    if [ $rest_retry_times -eq 0 ]; then
        echo "get model failed from cyclone, name: ${cyclone_model_name}, version: ${cyclone_model_version}"
        return 1
    fi
}

CWD=$(dirname "$0")
ts_dir=$(cd $CWD;pwd)
if [[ ! $tools_dir ]] || [[ -z $tools_dir ]]; then
        export tools_dir=$ts_dir
fi


while [ $# -gt 0 ]; do
  case "$1" in
    --input_path=*)
      input_path="${1#*=}"
      ;;
    --data_name=*)
      data_name="${1#*=}"
      ;;
    --is_base64=*)
      is_base64="${1#*=}"
      ;;
    --kv_delimiter=*)
      kv_delimiter="${1#*=}"
      ;;
    --dup_cnt=*)
      dup_cnt="${1#*=}"
      ;;
    --creator=*)
      creator="${1#*=}"
      ;;
    --namespace=*)
      namespace="${1#*=}"
      ;;
    --is_test=*)
      is_test="${1#*=}"
      ;;
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.*\n"
      printf "***************************\n"
      exit 1
  esac
  shift
done

if [ -z $input_path ] || [ -z $data_name ] || [ -z $creator ] || [ -z $namespace ]
then
    echo "Must have 4 args: input_path, data_name, namespace and creator"
    exit 1
fi

if [ -z $is_base64 ]
then
is_base64=false
fi

if [ -z $kv_delimiter ]
then
kv_delimiter=space
fi

if [ -z is_test ]
then
is_test=no
fi


current=$(date "+%Y-%m-%d %H:%M:%S")
timeStamp=$(date -d "$current" +%s)
echo $timeStamp

check_input_path ${input_path}

python3 $ts_dir/cannon/cannon_publisher.py --build_type=common_kv --input_path=$input_path --data_name=$data_name \
                                          --class_name=CardinalCmphDictModel --other_args="${is_base64},${kv_delimiter}" --is_test=$is_test \
                                          --version=$timeStamp --creator=$creator --dup_cnt=$dup_cnt --namespace=$namespace
if [ $? -ne 0 ];then echo "Error : cannon publish $cannon_model_name $timeStamp failed!";exit 1;fi
check_model $data_name $timeStamp $is_test
if [ $? -ne 0 ];then echo "Error : check cyclone load status $cannon_model_name $timeStamp failed!";exit 1;fi

