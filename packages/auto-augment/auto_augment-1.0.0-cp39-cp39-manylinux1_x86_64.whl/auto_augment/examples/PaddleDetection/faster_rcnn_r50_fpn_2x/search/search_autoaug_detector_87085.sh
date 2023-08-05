#!/usr/bin/env bash
export PYTHONPATH=${PYTHONPATH}:../
echo ${PYTHONPATH}

export FLAGS_eager_delete_tensor_gb=0.0

workspace="work_dirs/pbt_detector/test_autoaug_87085"
rm -rf ${workspace}
mkdir -p ${workspace}
config="examples/PaddleDetection/faster_rcnn_r50_fpn_2x/search/pba_detector_faster_rcnn_r50_fpn_2x_87085_coco.yaml"


CUDA_VISIBLE_DEVICES=3,4,5 python test/autoaug_search.py \
    --config=${config} --workspace=${workspace} #2>&1 | tee -a ${workspace}/log.txt


