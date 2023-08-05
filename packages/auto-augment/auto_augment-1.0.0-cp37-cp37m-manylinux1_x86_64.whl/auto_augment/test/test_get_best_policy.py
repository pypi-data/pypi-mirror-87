# -*- coding: utf-8 -*-
#*******************************************************************************
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
#*******************************************************************************
"""

Authors: lvhaijun01@baidu.com
Date:     2020-04-04 23:42
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
sys.path.append("/home/lvhaijun/video_recognition/rudder_online/baidu/dragonboat/")

from auto_augment.autoaug.utils.data_aug_utils import get_best_policy, calculate_show_scheduler, trace_trial_sched, trial_result
from auto_augment.autoaug.transform.ops.utils import parse_log
import logging
import json
import argparse
from auto_augment.autoaug.utils import log
from auto_augment.autoaug.utils.data_aug_utils import get_best_policy, trace_trial_sched, trial_result, pba_convert_user_policy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    """

    Returns:

    """

    parser = argparse.ArgumentParser(
        "data augmentation job")
    parser.add_argument(
        "--work_home",
        help="data_augmentation_type",
        default="data_augment_classifer_search.PbtAutoAugmentClassiferSearch")

    parser.add_argument(
        "--reward_attr",
        help="reward_attr",
        default="val_acc")

    parser.add_argument(
        "--task_type",
        help="task_type",
        default="classifier")

    parser.add_argument(
        "--schedule_epoch",
        help="schedule_epoch",
        default=360,
        type=int)

    args = parser.parse_args()
    args = vars(args)
    return args


def main():
    conf = parse_args()
    work_home = conf["work_home"]
    #best_trail_res_txt = get_best_policy(work_home, cls_prefix="TrainableDetector", reward_attr="val_map")

    # trace every trail sched route
    trace_trial_sched(work_home, cls_prefix="TrainableAutoAug", reward_attr=conf["reward_attr"],
                       schedule_epoch=conf["schedule_epoch"])
    best_res_txt, best_trial_num = get_best_policy(work_home, cls_prefix="TrainableAutoAug", reward_attr=conf["reward_attr"])
    best_policy = pba_convert_user_policy(
        best_trial_num,
        best_res_txt, conf["schedule_epoch"], conf["task_type"], "PBA")
    result = trial_result(best_policy)
    result.dump_best_policy(
        path=work_home)



if __name__ == "__main__":
    main()
