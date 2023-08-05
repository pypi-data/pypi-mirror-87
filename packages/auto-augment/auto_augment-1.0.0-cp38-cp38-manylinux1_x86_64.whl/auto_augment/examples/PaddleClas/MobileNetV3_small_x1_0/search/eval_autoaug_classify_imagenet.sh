#!/usr/bin/env bash
export PYTHONPATH=${PYTHONPATH}:../
export PYTHONPATH=${PYTHONPATH}:./third_party/PaddleClas
echo ${PYTHONPATH}


export FLAGS_fast_eager_deletion_mode=1
export FLAGS_eager_delete_tensor_gb=0.0

config="examples/PaddleClas/MobileNetV3_small_x1_0/search/MobileNetV3_small_x1_0.yaml"
python -m paddle.distributed.launch \
    --selected_gpus="5,6" \
    examples/PaddleClas/code/eval.py \
        -c ${config} \
        --override pretrained_model=pretrain/MobileNetV3_small_x1_0_pretrained

