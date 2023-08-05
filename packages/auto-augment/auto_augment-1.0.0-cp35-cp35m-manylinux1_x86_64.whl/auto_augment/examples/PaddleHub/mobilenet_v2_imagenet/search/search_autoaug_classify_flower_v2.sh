#!/usr/bin/env bash
export PYTHONPATH=${PYTHONPATH}:../
echo ${PYTHONPATH}
export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/PaddleHub
export FLAGS_fast_eager_deletion_mode=1
export FLAGS_eager_delete_tensor_gb=0.0

config="examples/PaddleHub/mobilenet_v2_imagenet/search/pba_classifier_mobilenetv2_flower_small.yaml"
workspace="./work_dirs/pbt_paddlehub_classifer/test_aug_flower_mobilenetv2_v2"
# workspace工作空间需要初始化
rm -rf ${workspace}
mkdir -p ${workspace}
CUDA_VISIBLE_DEVICES=0,1 python test/paddlehub_autoaug_search.py \
    --config=${config} \
    --workspace=${workspace} #2>&1 | tee -a ${workspace}/log.txt
