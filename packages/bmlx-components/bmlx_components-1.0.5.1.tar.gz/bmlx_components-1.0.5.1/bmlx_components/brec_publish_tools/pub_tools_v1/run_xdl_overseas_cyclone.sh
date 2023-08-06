#!/bin/bash
##发布xdl模型到欧洲cyclone


while [ $# -gt 0 ]; do
  case "$1" in
    --convert_pub_hdfs=*)
      convert_pub_hdfs="${1#*=}"
      ;;
    --model_name=*)
      model_name="${1#*=}"
      ;;
    --overseas=*)
      overseas="${1#*=}"
      ;;
    --graph_collection=*)
      graph_collection="${1#*=}"
      ;;
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.*\n"
      printf "***************************\n"
      exit 1
  esac
  shift
done

dims=""
for dim in `hadoop fs -ls ${convert_pub_hdfs}/emb_bin | awk '{if(NF==8)print $NF}' | awk -F '/' '{print $NF}'`;do
    if [ ! -n "$(echo $dim| sed -n "/^[0-9]\+$/p")" ];then
        continue
    fi
    dims="${dims},${dim}"
done

dims=${dims#*,}
if [ -z $dims ]
then
    echo "no dims"
    exit 1
fi

if [ -z $overseas]
then
    echo "no overseas"
    exit 1
fi

#/bin/bash
cur_ts=$(date +%s)
rand=$((${cur_ts}%4))
arr_ip=("43.224.67.120" "43.224,67.124" "43.224.67.125" "103.211.228.11")
remote_ip=${arr_ip[$rand]}
echo "model_name: ${model_name} , overseas: ${overseas} , graph_collection: ${graph_collection} , dims: ${dims} , convert_pub_hdfs: ${convert_pub_hdfs}"
echo "remote service ip: ${remote_ip}"

curl -X POST  "http://${remote_ip}:8100/delivery_overseas?data_name=${model_name}&overseas=${overseas}&dims=${dims}&graph_collection=${graph_collection}" -s >"curl_eu_${cur_ts}" &
sleep 5
grep "success" "curl_eu_${cur_ts}" >/dev/null
if [ $? -ne 0 ];then 
    echo "Error: run_xdl_eu_cyclone.sh failed, "
    echo "curl res: $(cat "curl_eu_${cur_ts}")"
    exit 1
fi

