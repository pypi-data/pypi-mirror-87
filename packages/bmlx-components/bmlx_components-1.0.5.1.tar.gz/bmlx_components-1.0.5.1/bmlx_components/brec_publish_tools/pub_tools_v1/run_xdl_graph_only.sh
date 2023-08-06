#!/bin/bash
##发布xdl模型到cyclone

online_meta_url="http://164.90.76.180:6210/CycloneMetaService/GetModelDeployInfo"
test_meta_url="http://103.43.87.118:6210/CycloneMetaService/GetModelDeployInfo"

function check_model()
{
    cyclone_model_name="${1}_${2}"
    url=""
    is_test=$(echo $4 | grep 'test')
    if [ -z "$is_test" ]; then
        url=$online_meta_url
    else
        url=$test_meta_url
    fi
    echo "model name: ${cyclone_model_name}, version: ${cyclone_model_version}, url: ${url}"
    rest_retry_times=360 #最长配送1h，如果还没完成则退出报警
    while [ $rest_retry_times -gt 0 ]
    do
        result=`curl $url -d '{"model_name":"'${cyclone_model_name}'","model_version":"'$3'"}'`
        check_result=$(echo $result | grep '"status":"OK"')
        if [ -z "$check_result" ]; then
            echo "Round-robin querying cyclone ..."
            sleep 10s
        else
            echo "get model success from cyclone, name: ${cyclone_model_name}, version: $3"
            return 0
        fi
        let "rest_retry_times--"
    done

    if [ $rest_retry_times -eq 0 ]; then
        echo "get model failed from cyclone, name: ${cyclone_model_name}, version: $3"
        return 1
    fi
}

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
      echo "Error: input path size is ${size}, too small"
      exit 1
    fi
}

function publish_embedding_model()
{
    #begin build data with cannon
    check_input_path ${1}
    cannon_build_type="embed"
    cannon_input_path=$1
    cannon_model_name=$2
    cannon_model_class="EmbeddingModel2"
    cannon_model_dim=$5
    cannon_args="$4,$5,$3"
    cannon_version=$3
    cannon_dup_cnt=$7
    data_creator=$8
    cannon_namespace=$9
    is_test=${10}
    if [[ ! $tools_dir ]] || [[ -z $tools_dir ]]; then
            export tools_dir=$6
    fi
    python $6/cannon/cannon_publisher.py \
            --build_type=$cannon_build_type --input_path=$cannon_input_path --data_name=$cannon_model_name --class_name=$cannon_model_class \
            --other_args=$cannon_args --creator=$data_creator --dup_cnt=$cannon_dup_cnt --is_test=$is_test --namespace=$cannon_namespace
    if [ $? -ne 0 ];then echo "Error: python $6/cannon/cannon_publisher.py $cannon_build_type $cannon_input_path $cannon_model_name $cannon_model_class $cannon_args $data_creator $cannon_dup_cnt $is_test faied! exit...";exit 1;fi

    check_model $cannon_model_name $cannon_model_dim $cannon_version $is_test
    if [ $? -ne 0 ];then echo "Error : check_model $cannon_model_name $cannon_model_dim $cannon_version $is_test failed!";exit 1;fi
}

function publish_graph()
{
    python $5/update_resource_v3.py --collection=$4 --name=$2 --processor=DELIVER-V1 \
                                 --version=$3 --hdfs_src=$1
    if [ $? -ne 0 ];then echo "Error: python $5/update_resource_v3.py --collection=$4 --name=$2 --processor=DELIVER-V1 \
                                 --version=$3 --hdfs_src=$1 faied! exit...";exit 1;fi
}

#get tools dir position
CWD=$(dirname "$0")
ts_dir=$(cd $CWD;pwd)
echo ${ts_dir}
while [ $# -gt 0 ]; do
  case "$1" in
    --convert_pub_hdfs=*)
      convert_pub_hdfs="${1#*=}"
      ;;
    --model_name=*)
      model_name="${1#*=}"
      ;;
    --emb_collection=*)
      emb_collection="${1#*=}"
      ;;
    --graph_collection=*)
      graph_collection="${1#*=}"
      ;;
    --dup_cnt=*)
      dup_cnt="${1#*=}"
      ;;
    --namespace=*)
      namespace="${1#*=}"
      ;;
    --creator=*)
      creator="${1#*=}"
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


#get current timestamp
build_latency=300
current=`date "+%Y-%m-%d %H:%M:%S"`  
timeStamp=`date -d "$current" +%s`   

version=`expr $timeStamp + $build_latency`
if [ -z "$convert_pub_hdfs" ] || [ -z "$model_name" ] || [ -z "$creator" ] || [ -z "$namespace" ]
then
    echo "Must have 4 args: convert_pub_hdfs, model_name, creator and namespace"
    exit 1
fi

if [ -z $dup_cnt ]
then
    dup_cnt=6
fi
if [ -z $emb_colleciton ]
then
    emb_collection=CYCLONE_COLLECTION
fi

if [ -z $is_test ]
then
    is_test=no
fi


version=1589856039
input_path_embed="${convert_pub_hdfs}/emb_bin/64"
dim=64
publish_embedding_model $input_path_embed $model_name $version $emb_collection $dim $ts_dir $dup_cnt $creator $namespace $is_test
#for dim in `hadoop fs -ls ${convert_pub_hdfs}/emb_bin | awk '{if(NF==8)print $NF}' | awk -F '/' '{print $NF}'`;do
#    input_path_embed="${convert_pub_hdfs}/emb_bin/${dim}"
#    publish_embedding_model $input_path_embed $model_name $version $emb_collection $dim $ts_dir $dup_cnt $creator $namespace $is_test
#    if [ $# -ne 0 ]; then
#        echo "publish embedding failed"
#        exit 1
#    fi
#done
#input_path_graph="${convert_pub_hdfs}/online_model"
#echo "publish_graph $input_path_graph $model_name $version $graph_collection $ts_dir"
#graph_retry_times=5 #最长配送1h，如果还没完成则退出报警
#while [ $graph_retry_times -gt 0 ]
#do
#    publish_graph $input_path_graph $model_name $version $graph_collection $ts_dir
#    if [ $? -eq 0 ];then 
#      echo "publish ad graph success";exit 0
#    else
#      sleep 5
#      let "graph_retry_times--"
#    fi
#done
#
#if [ $graph_retry_times -eq 0 ]; then
#    echo "publish ad graph failed"
#    exit 1
#fi
###bash -x run_xdl.sh "hdfs://bigo-rt/user/alg_rank/xdlModelData/xdl_new_din_russia_v2_online_k8s/20200224/10/output" xdl_new_din_russia_v2_online_k8s "CYCLONE_COLLECTION" "JUNK_COLLECTION"
