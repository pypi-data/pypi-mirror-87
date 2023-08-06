#!/bin/bash
HDFS_ROOT="hdfs://bigocluster/user/hadoop/dispatching/models"

function check_input_path() {
	hadoop fs -test -e "${1}"
	if [ $? -ne 0 ]; then
		echo "Error: input path doesn't exists, ${1}"
		exit 1
	fi

	size=$(hadoop fs -du -s ${1} | awk '{print $1}')
	echo ${size}
	if [ ${size} -eq 0 ]; then
		echo "Error: input path size is ${size}, invalid"
		exit 1
	fi
}

function upload_hdfs() {
	echo "model name: ${1}  hdfs dir: ${2}  version: ${3}"
	hadoop fs -test -e "${2}"
	if [ $? -ne 0 ]; then
		hadoop fs -mkdir -p ${2} &&
			hadoop fs -chmod -R 777 ${2}
	fi
	hadoop fs -put $1 "${2}/$3" &&
		hadoop fs -chmod -R 777 ${2}
	if [ $? -ne 0 ]; then
		echo "upload to hdfs failed"
		exit 1
	fi
}

CWD=$(dirname "$0")
ts_dir=$(
	cd $CWD
	pwd
)
if [[ ! $tools_dir ]] || [[ -z $tools_dir ]]; then
	export tools_dir=$ts_dir
fi

while [ $# -gt 0 ]; do
	case "$1" in
	--input_path=*)
		input_path="${1#*=}"
		;;
	--build_type=*)
		build_type="${1#*=}"
		;;
	--data_name=*)
		data_name="${1#*=}"
		;;
	--collection=*)
		collection="${1#*=}"
		;;
	--send_conf=*)
		send_conf="${1#*=}"
		;;
	--version=*)
		version="${1#*=}"
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
	--phase=*)
		phase="${1#*=}"
		;;
	--local_src=*)
		local_src="${1#*=}"
		;;
	--source=*)
		source="${1#*=}"
		;;
	--dest=*)
		dest="${@#*=}"
		;;
	esac
	shift
done

if [ -z "$build_type" ]; then
	build_type=deliver
fi

if [ -z "$input_path" ] && [ -z "$local_src" ]; then
	echo "input_path and local_src must have one"
fi

if [ ! -z "$input_path" ] && [ ! -z "$local_src" ]; then
	echo "input_path and local_src could only have one"
fi

if [ ! -z "${input_path}" ]; then
	check_input_path ${input_path}
fi

if [ -z "$collection" ]; then
	echo "collection is null"
	exit 1
fi

if [ -z "$version" ]; then
	current=$(date "+%Y-%m-%d %H:%M:%S")
	version=$(date -d "$current" +%s)
fi

hdfs_move="true"
if [ ! -z "$local_src" ]; then
	out_path="${HDFS_ROOT}/${collection}/${data_name}/${version}/${version}"
	input_dir="${HDFS_ROOT}/${collection}/${data_name}/${version}"
	hdfs_move="false"
	upload_hdfs $local_src $input_dir $version
	check_input_path ${out_path}
fi

if [ ! -z "${send_conf}" ]; then
	other_args="send_conf=${send_conf};hdfs_move=${hdfs_move}"
else
	other_args="send_conf=false;hdfs_move=${hdfs_move}"
fi

if [ -z $data_name ] || [ -z $creator ] || [ -z $namespace ]; then
	echo "Must have 3 args: data_name, namespace and creator"
	exit 1
fi

python $ts_dir/cannon/cannon_publisher.py --build_type=$build_type \
	--input_path="${input_path}" \
	--output_path="${out_path}" \
	--data_name="$data_name" \
	--collection="$collection" \
	--version="$version" \
	--phase="$phase" \
	--other_args="$other_args" \
	--overseas="$overseas" \
	--creator="$creator" \
	--namespace="$namespace" \
	--destination $dest \
	--source=$source
if [ $? -ne 0 ]; then
	echo "publish failed, data_type:${build_type}, data_name:${data_name}, collection:${collection}, version:${version}"
	exit 1
fi
