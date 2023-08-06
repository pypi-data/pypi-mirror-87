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

CWD=$(dirname "$0")
ts_dir=$(cd $CWD;pwd)
if [[ ! $tools_dir ]] || [[ -z $tools_dir ]]; then
        export tools_dir=$ts_dir
fi

while [ $# -gt 0 ]; do
  case "$1" in
    --input_parent=*)
      input_parent="${1#*=}"
      ;;
    --country=*)
      country="${1#*=}"
      ;;
    --data_name=*)
      data_name="${1#*=}"
      ;;
    --model_class=*)
      model_class="${1#*=}"
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
    --overseas=*)
      overseas="${1#*=}"
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

input_path=$input_parent/$country
echo "input path : ${input_path}"
other_args="CYCLONE_COLLECTION,${country},gap_days,false,false"


if [ -z $input_path ] || [ -z $data_name ] || [ -z $creator ] || [ -z $namespace ]
then
    echo "Must have 4 args: input_path, data_name, namespace and creator"
    exit 1
fi

check_input_path ${input_path}

python $ts_dir/cannon/cannon_publisher.py --build_type="cf" \
                                          --input_path="${input_path}" \
                                          --data_name="$data_name" \
                                          --class_name="$model_class" \
                                          --other_args="$other_args" \
                                          --overseas="$overseas" \
                                          --dup_cnt="$dup_cnt" \
                                          --creator="$creator" \
                                          --namespace="$namespace" \
                                          --is_test="$is_test"
