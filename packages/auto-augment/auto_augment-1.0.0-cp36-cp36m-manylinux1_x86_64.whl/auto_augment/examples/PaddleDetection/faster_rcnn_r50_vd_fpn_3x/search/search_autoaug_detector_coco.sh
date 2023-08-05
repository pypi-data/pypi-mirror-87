#!/usr/bin/env bash
export PYTHONPATH=${PYTHONPATH}:../
echo ${PYTHONPATH}

export FLAGS_eager_delete_tensor_gb=0.0


config="examples/PaddleDetection/faster_rcnn_r50_vd_fpn_3x/search/pba_detector_faster_rcnn_r50_vd_fpn_3x_coco.yaml"
workspace="work_dirs/pbt_detector/test_autoaug_detector_coco_faster_rcnn_r50_vd_fpn_3x_v4"
rm -rf ${workspace}
mkdir -p ${workspace}
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python test/autoaug_search.py \
    --config=${config} --workspace=${workspace} 2>&1 | tee -a ${workspace}/log.txt
