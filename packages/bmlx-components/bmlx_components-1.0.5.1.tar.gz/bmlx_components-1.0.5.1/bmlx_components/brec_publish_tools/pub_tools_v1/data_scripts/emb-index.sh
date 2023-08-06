#!/bin/bash

if [[ $# != 2 ]]; then
    echo "no basic args"
    exit 1
fi

PLUGINS_ROOT="$1"
TASK_DIR="$2"

TOOLS="${PLUGINS_ROOT}/tools"

PACK_PATH="${TASK_DIR}/${VERSION}"

EMB_RAW_DIR="${TASK_DIR}/emb_bin"
EMB_TMP_DIR="${TASK_DIR}/emb-kv"

find "${EMB_RAW_DIR}" -type f -size 0c | xargs -n 1 rm -f


# dim level raw_dir
function partition_and_build() {
    mkdir "${EMB_TMP_DIR}" && \
    echo "partition.exe --dim=${1} --level=${2} ..." && \
    sudo chmod 777 ${TOOLS}/partition.exe && \
    ${TOOLS}/partition.exe "--dim=${1}" "--level=${2}" \
        "--input=${3}" "--output_dir=${EMB_TMP_DIR}" && \
    echo "build.exe ..."  && \
    sudo chmod 777 ${TOOLS}/build.exe && \
    ${TOOLS}/build.exe "--dim=${1}" "--level=${2}" \
        "--thread_level=4" "--input_dir=${EMB_TMP_DIR}" "--output=${PACK_PATH}/dim-${dim}.emb" && \
    rm -rf "${EMB_TMP_DIR}"
}

for dim in `ls ${EMB_RAW_DIR}`; do
    EMB_RAW_SUB_DIR="${EMB_RAW_DIR}/${dim}"
    if [[ `ls "${EMB_RAW_SUB_DIR}"` == "" ]]; then
        echo "skip ${EMB_RAW_SUB_DIR} ..."
        continue
    fi
    echo "build ${EMB_RAW_SUB_DIR} ..."

    EMB_BYTES=`du -sb "${EMB_RAW_SUB_DIR}" | awk '{print $1}'`
    PARTITION_LEVEL=`echo "l(${EMB_BYTES}/671088640)/l(2)" | bc -l`
    PARTITION_LEVEL="${PARTITION_LEVEL%.*}"
    echo ${PARTITION_LEVEL} 
    if [[ ${PARTITION_LEVEL} == "-" ]]; then
        PARTITION_LEVEL=0
    elif [[ ${PARTITION_LEVEL} -ge 7 ]]; then
        PARTITION_LEVEL=7
    elif [[ ${PARTITION_LEVEL} -le 0 ]]; then
        PARTITION_LEVEL=0
    fi
    echo ${PARTITION_LEVEL} 

    if ! partition_and_build ${dim} ${PARTITION_LEVEL} ${EMB_RAW_SUB_DIR}; then
        echo "fail to build ${EMB_RAW_SUB_DIR}"
        exit 1
    fi
done
    mv ${PACK_PATH}/online_model/* ${PACK_PATH}
    rm -rf ${PACK_PATH}/online_model
    rm  ${PACK_PATH}/_SUCCESS.train
    rm -rf "${EMB_RAW_DIR}"
