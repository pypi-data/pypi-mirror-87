#!/usr/bin/env bash
export PYTHONPATH=${PYTHONPATH}:../
echo ${PYTHONPATH}

export FLAGS_fast_eager_deletion_mode=1
export FLAGS_eager_delete_tensor_gb=0.0

config="examples/PaddleClas/ResNet50/search/pba_classifier_ResNet50_imagnet.yaml"
workspace="./work_dirs/pbt_classifer/test_aug_imagenet_resnet50"
# workspace工作空间需要初始化
rm -rf ${workspace}
mkdir -p ${workspace}
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python test/autoaug_search.py \
    --config=${config} \
    --workspace=${workspace} 2>&1 | tee -a ${workspace}/log.txt
