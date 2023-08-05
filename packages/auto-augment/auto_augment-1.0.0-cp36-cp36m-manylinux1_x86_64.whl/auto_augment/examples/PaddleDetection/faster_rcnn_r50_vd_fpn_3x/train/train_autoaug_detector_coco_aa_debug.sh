#!/usr/bin/env bash
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/rudder_online/baidu/dragonboat/
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/PaddleClas
export PYTHONPATH=${PYTHONPATH}:../
export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleDetection

#export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleClas
echo ${PYTHONPATH}

config="examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x/train/faster_rcnn_r50_vd_fpn_aa_3x.yml"

model_save_dir="work_dirs/pbt_detector/faster_rcnn_r50_vd_fpn_aa_3x/train_not_use_cudnn"

#resume_checkpoint="work_dirs/pbt_detector/faster_rcnn_r50_vd_fpn_aa_3x/train/faster_rcnn_r50_vd_fpn_aa_3x/240000"
mkdir -p ${model_save_dir}
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
#python examples/PaddleDetection/code/train_not_iterable_epoch.py \

export GLOG_v=10
export FLAGS_fast_eager_deletion_mode=0
export FLAGS_eager_delete_tensor_gb=-1.0
export FLAGS_fraction_of_gpu_memory_to_use=0.98
python examples/PaddleDetection/code/train_hang.py \
-c ${config} \
--eval \
-o save_dir=${model_save_dir} #2>&1 | tee -a /ssd2/lvhaijun/autoaug_debug_log.txt

#resume_checkpoint="work_dirs/pbt_detector/faster_rcnn_r50_vd_fpn_aa_3x/train/faster_rcnn_r50_vd_fpn_aa_3x/240000"
#mkdir -p ${model_save_dir}
#export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
#python examples/PaddleDetection/code/train.py \
#-c ${config} \
#--eval \
#--resume_checkpoint ${resume_checkpoint} \
#-o save_dir=${model_save_dir} 2>&1 | tee -a ${model_save_dir}/log