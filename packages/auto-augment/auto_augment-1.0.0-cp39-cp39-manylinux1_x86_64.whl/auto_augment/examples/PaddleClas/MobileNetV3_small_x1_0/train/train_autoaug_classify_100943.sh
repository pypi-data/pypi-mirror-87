#!/usr/bin/env bash
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/rudder_online/baidu/dragonboat/
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/PaddleClas
export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/baidu/aicc/auto-augment
export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/baidu/aicc/auto-augment/auto_augment/third_party/PaddleClas

#export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleClas
echo ${PYTHONPATH}

config="examples/PaddleClas/MobileNetV3_small_x1_0/train/MobileNetV3_small_x1_0_38833.yaml"

model_save_dir="work_dirs/pbt_classifer/test_autoaug/train"
#woorker_log="--log_dir $model_save_dir"
mkdir -p ${model_save_dir}
python -m paddle.distributed.launch \
    --selected_gpus="0" \
    ${woorker_log} \
    examples/PaddleClas/code/train.py \
        -c ${config} \
        --override model_save_dir=${model_save_dir} 2>&1 | tee -a ${model_save_dir}/log.txt