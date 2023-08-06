#!/bin/bash

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
    if [ ${size} -eq 0 ]
    then
      echo "Error: input path size is ${size}, invalid"
      exit 1
    fi
}

cur_dir=`pwd`
app_dir=${cur_dir%alg_recall*}
ts_dir=$app_dir"alg_recall/pub_tools"
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
    --delimiter=*)
      delimiter="${1#*=}"
      ;;
    --dup_cnt=*)
      dup_cnt="${1#*=}"
      ;;
    --creator=*)
      creator="${1#*=}"
      ;;
    --overseas=*)
      overseas="${1#*=}"
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

check_input_path ${input_path}

python $ts_dir/cannon/cannon_publisher.py --build_type=relationship \
                                          --input_path=$input_path \
                                          --data_name=$data_name \
                                          --class_name=RelationShipModel \
                                          --other_args="CYCLONE_COLLECTION,true,${delimiter}" \
                                          --is_test=$is_test \
                                          --creator=$creator \
                                          --dup_cnt=$dup_cnt \
                                          --overseas=$overseas \
                                          --namespace=$namespace
