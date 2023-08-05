#!/usr/bin/env bash
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/rudder_online/baidu/dragonboat/
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/PaddleClas
export PYTHONPATH=${PYTHONPATH}:../
export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleDetection

#export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleClas
echo ${PYTHONPATH}

config="examples/PaddleDetection/faster_rcnn_r50_fpn_2x/train/faster_rcnn_r50_fpn_2x_76557.yml"

model_save_dir="work_dirs/pbt_detector/test_autoaug_76557/train"

export CUDA_VISIBLE_DEVICES=4,5,6,7
#python examples/PaddleDetection/code/train.py \
python examples/PaddleDetection/code/train_not_iterable_epoch.py \
-c ${config} \
--eval \
-o save_dir=${model_save_dir} #2>&1 | tee -a ${model_save_dir}/log