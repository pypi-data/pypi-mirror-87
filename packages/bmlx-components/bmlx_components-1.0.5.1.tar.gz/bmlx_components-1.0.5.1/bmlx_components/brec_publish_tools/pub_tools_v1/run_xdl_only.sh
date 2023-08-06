#!/bin/bash
##发布xdl模型到cyclone

online_meta_url="http://164.90.76.180:6210/CycloneMetaService/GetModelDeployInfo"
test_meta_url="http://103.43.87.118:6210/CycloneMetaService/GetModelDeployInfo"

function check_model()
{
    cyclone_model_name="${2}_${3}"
    url=""
    is_test=$(echo $5 | grep 'test')
    if [ -z "$is_test" ]; then
        url=$online_meta_url
    else
        url=$test_meta_url
    fi
    rest_retry_times=360 #最长配送1h，如果还没完成则退出报警
    while [ $rest_retry_times -gt 0 ]
    do
        result=`curl $url -d '{"model_name":"'${cyclone_model_name}'","model_version":"'$4'"}'`
        echo $result
        check_result=$(echo $result | grep '"status":"OK"')
        if [ -z "$check_result" ]; then
            sleep 10s
        else
            echo "get model success from cyclone, name: ${cyclone_model_name}, version: $4"
            return 0
        fi
        let "rest_retry_times--"
    done

    if [ $rest_retry_times -eq 0 ]; then
        echo "get model failed from cyclone, name: ${cyclone_model_name}, version: $4"
        return 1
    fi
}

function publish_embedding_model()
{
    #begin build data with cannon
    cannon_build_type="embed"
    cannon_input_path=$1
    cannon_model_name=$2
    cannon_model_class="EmbeddingModel2"
    cannon_model_dim=$5
    cannon_args="$4,$5,$3"
    cannon_version=$3
    is_test=$7
    echo $cannon_input_path
    echo $cannon_args
    echo $cannon_version
    if [[ ! $tools_dir ]] || [[ -z $tools_dir ]]; then
            export tools_dir=$6
    fi
    python $6/cannon/cannon_publisher.py \
            $cannon_build_type $cannon_input_path $cannon_model_name $cannon_model_class $cannon_args $is_test
    if [ $? -ne 0 ];then echo "Error: python $6/cannon/cannon_publisher.py $cannon_build_type $cannon_input_path $cannon_model_name $cannon_model_class $cannon_args $is_test failed! exit...";exit 1;fi

    check_model $cannon_input_path $cannon_model_name $cannon_model_dim $cannon_version $is_test
    if [ $? -ne 0 ];then echo "Error : check_model $cannon_input_path $cannon_model_name $cannon_model_dim $cannon_version $is_test failed!";exit 1;fi
}


#get tools dir position
CWD=$(dirname "$0")
ts_dir=$(cd $CWD;pwd)
echo "tools_dir is : $ts_dir"
convert_pub_hdfs=$1
model_name=$2
emb_collection=$3  #CYCLONE_COLLECTION
is_test=$4

#get current timestamp
build_latency=300
current=`date "+%Y-%m-%d %H:%M:%S"`  
timeStamp=`date -d "$current" +%s`   

version=`expr $timeStamp + $build_latency`

for dim in `hadoop fs -ls ${convert_pub_hdfs}/emb_bin | awk '{if(NF==8)print $NF}' | awk -F '/' '{print $NF}'`;do
    input_path_embed="${convert_pub_hdfs}/emb_bin/${dim}"
    publish_embedding_model $input_path_embed $model_name $version $emb_collection $dim $ts_dir $is_test
    wait
done

