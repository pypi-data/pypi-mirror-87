#!/usr/bin/env bash
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/rudder_online/baidu/dragonboat/
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/PaddleClas
export PYTHONPATH=${PYTHONPATH}:../
#export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleClas
echo ${PYTHONPATH}

export FLAGS_fast_eager_deletion_mode=1
export FLAGS_eager_delete_tensor_gb=0.0

workspace=work_dirs/pbt_classifer/test_autoaug_pba_simplespace
rm -rf ${workspace}
mkdir -p ${workspace}

#config="examples/PaddleClas/MobileNetV3_small_x1_0/search/pba_classifier_MobileNetV3_small_x1_0_38833.yaml"
config="examples/PaddleClas/MobileNetV3_small_x1_0/search/pba_classifier_MobileNetV3_small_x1_0_38833_simplespace.yaml"
 CUDA_VISIBLE_DEVICES=3,4 python test/autoaug_search.py \
    --config=${config} --workspace=${workspace} #2>&1 | tee -a  ${workspace}/log.txt
