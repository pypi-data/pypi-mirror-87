#!/usr/bin/env bash
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/rudder_online/baidu/dragonboat/
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/PaddleClas
export PYTHONPATH=${PYTHONPATH}:../
export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleDetection

#export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleClas
echo ${PYTHONPATH}

config="examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x/train/faster_rcnn_r50_vd_fpn_3x_coco.yml"

model_save_dir="work_dirs/pbt_detector/test_autoaug_detector_coco_faster_rcnn_r50_vd_fpn_3x/train/"

weights=${model_save_dir}/
export CUDA_VISIBLE_DEVICES=0,1

#weights_name="30000 60000 90000 120000 150000 180000 210000 240000"
weights_name="240000"
for weight_name in ${weights_name}
do
    python examples/PaddleDetection/code/eval.py \
    -c ${config} \
    -o weights=${model_save_dir}/faster_rcnn_r50_vd_fpn_3x_coco/${weight_name} #2>&1 | tee -a ${model_save_dir}/eval.txt
done
