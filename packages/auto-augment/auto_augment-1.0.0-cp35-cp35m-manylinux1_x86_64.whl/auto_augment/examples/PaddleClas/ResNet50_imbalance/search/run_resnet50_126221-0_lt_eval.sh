#!/usr/bin/env bash

export PYTHONPATH=$PWD:$PYTHONPATH
export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/baidu/aicc/auto-augment
export PYTHONPATH=${PYTHONPATH}:/home/lvhaijun/video_recognition/utils_project/experiment_project/baidu/aicc/auto-augment/auto_augment/third_party/PaddleClas

# first stage
#model_save_dir_first_stage="./output/ResNet50_126221-0_LT_lt_f1score/first_stage"
model_save_dir_first_stage="./output/ResNet50_126221-0_LT_lt_f1score_val_imal/first_stage"

load_yaml=examples/PaddleClas/ResNet50_imbalance/search/ResNet50_126221-0_LT_lt_first_stage.yaml

#load_yaml=./tools/configs/ResNet50_126221-0_LT_lt_balance_sampe.yaml

mkdir -p ${model_save_dir_first_stage}
#python -m paddle.distributed.launch \
#    --selected_gpus="4,5,6,7" \
#    tools/train.py \
#        -c ${load_yaml} \
#        --override model_save_dir=${model_save_dir_first_stage} 2>&1 | tee -a ${model_save_dir_first_stage}/log.txt


python -m paddle.distributed.launch \
    --selected_gpus="3" \
    examples/PaddleClas/code/eval.py \
        -c ${load_yaml} \
        --override  pretrained_model=/home/lvhaijun/video_recognition/utils_project/experiment_project/baidu/aicc/auto-augment/auto_augment/work_dirs/cls_bal_pbt_classifer/test_aug_126221_resnet50_v3_firt_stage/checkpoint
##


# second_stage
#model_save_dir="./output/ResNet50_126221-0_LT_lt_f1score/second_stage"
#model_save_dir="./output/ResNet50_126221-0_LT_lt_f1score_val_imal/second_stage_test_1gpu"
#mkdir -p ${model_save_dir}
#python -m paddle.distributed.launch \
#    --selected_gpus="4" \
#    tools/train.py \
#        -c ./tools/configs/ResNet50_126221-0_LT_lt_second_stage.yaml \
#        --override model_save_dir=${model_save_dir} \
#        --override pretrained_model=${model_save_dir_first_stage}/ResNet50/best_f1_score_model/ppcls 2>&1 | tee -a ${model_save_dir}/log.txt

##
#python -m paddle.distributed.launch \
#    --selected_gpus="3" \
#    tools/eval.py \
#        -c ./tools/configs/ResNet50_126221-0_LT_lt_second_stage.yaml \
#        --override  pretrained_model=${model_save_dir}/ResNet50/best_f1_score_model/ppcls 2>&1 | tee -a ${model_save_dir}/test_bal_log.txt
