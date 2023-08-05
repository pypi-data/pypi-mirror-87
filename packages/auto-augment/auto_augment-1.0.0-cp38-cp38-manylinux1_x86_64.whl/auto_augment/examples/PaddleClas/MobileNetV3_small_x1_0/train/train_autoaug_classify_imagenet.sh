#!/usr/bin/env bash
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/rudder_online/baidu/dragonboat/
#export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/PaddleClas
export PYTHONPATH=${PYTHONPATH}:../
export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleClas

#export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleClas
echo ${PYTHONPATH}

#config="examples/PaddleClas/MobileNetV3_small_x1_0/train/MobileNetV3_small_x1_0_imagenet.yml"
#config="examples/PaddleClas/MobileNetV3_small_x1_0/train/MobileNetV3_small_x1_0_imagenet_fastaa.yml"
config="examples/PaddleClas/MobileNetV3_small_x1_0/train/MobileNetV3_small_x1_0_reduce_imagenet_fastaa.yml"
#config="examples/PaddleClas/MobileNetV3_small_x1_0/train/MobileNetV3_small_x1_0_reduce_imagenet.yml"

#model_save_dir="work_dirs/pbt_classifer/test_aug_imagenet/train_cls240_num100_paddlecv_v2"
#model_save_dir="work_dirs/pbt_classifer/test_aug_imagenet_refine_cls240/train_cls240_num100_paddleclas"
#model_save_dir="work_dirs/pbt_classifer/test_aug_imagenet_refine_cls240_v3/train"
#model_save_dir="work_dirs/pbt_classifer/test_aug_imagenet_fastaa/reduce_train"
#model_save_dir="work_dirs/pbt_classifer/100_0_mobilenetv3_samll_x1_0_reduce_imagenet_cls240_num100/reduce_train_baseline"
model_save_dir="./work_dirs/pbt_classifer/test_aug_imagenet_fastaa_v2/reduce_train"
#woorker_log="--log_dir $model_save_dir"
mkdir -p ${model_save_dir}
python -m paddle.distributed.launch \
    --selected_gpus="1,2,3,4,5,6" \
    ${woorker_log} \
    examples/PaddleClas/code/train.py \
        -c ${config} \
        --override model_save_dir=${model_save_dir} 2>&1 | tee -a ${model_save_dir}/log.txt