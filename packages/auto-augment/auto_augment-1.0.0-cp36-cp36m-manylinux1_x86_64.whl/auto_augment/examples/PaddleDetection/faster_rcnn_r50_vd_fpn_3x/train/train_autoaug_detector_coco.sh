#!/usr/bin/env bash
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/rudder_online/baidu/dragonboat/
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/PaddleClas
export PYTHONPATH=${PYTHONPATH}:../
export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleDetection

#export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleClas
echo ${PYTHONPATH}

config="examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x/train/faster_rcnn_r50_vd_fpn_3x_coco.yml"

model_save_dir="work_dirs/pbt_detector/test_autoaug_detector_coco_faster_rcnn_r50_vd_fpn_3x_v4/train"
#
#mkdir -p ${model_save_dir}
#export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
#python examples/PaddleDetection/code/train.py \
#-c ${config} \
#--eval \
#-o save_dir=${model_save_dir} 2>&1 | tee -a ${model_save_dir}/log

resume_checkpoint="${model_save_dir}/faster_rcnn_r50_vd_fpn_3x_coco/240000"
mkdir -p ${model_save_dir}
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
python examples/PaddleDetection/code/train.py \
-c ${config} \
--eval \
--resume_checkpoint ${resume_checkpoint} \
-o save_dir=${model_save_dir} 2>&1 | tee -a ${model_save_dir}/log