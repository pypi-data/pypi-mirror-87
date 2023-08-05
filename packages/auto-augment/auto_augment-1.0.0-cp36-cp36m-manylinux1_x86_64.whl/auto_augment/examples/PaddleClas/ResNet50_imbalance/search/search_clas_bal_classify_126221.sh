#!/usr/bin/env bash
export PYTHONPATH=${PYTHONPATH}:../
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/PaddleClas
echo ${PYTHONPATH}


export FLAGS_fast_eager_deletion_mode=1
export FLAGS_eager_delete_tensor_gb=0.0

#config="examples/PaddleClas/ResNet50_imbalance/search/pba_classifier_ResNet50_1141.yaml"
config="examples/PaddleClas/ResNet50_imbalance/search/pba_classifier_ResNet50_126221.yaml"
#config="examples/PaddleClas/ResNet50_imbalance/search/ResNet50_1141-0_LT_lt_test.yaml"
workspace="./work_dirs/cls_bal_pbt_classifer/test_aug_126221_resnet50_v3_firt_stage"
# workspace工作空间需要初始化
#
rm -rf ${workspace}
mkdir -p ${workspace}
CUDA_VISIBLE_DEVICES=3,4,5,6 python test/autoaug_search.py \
    --config=${config} \
    --workspace=${workspace} #2>&1 | tee -a ${workspace}/log.txt
