# -*- coding: utf-8 -*-
# *******************************************************************************
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
# *******************************************************************************
"""

Authors: lvhaijun01@baidu.com
Date:     2019-10-01 16:44
"""

# import yaml
# import re
# import os
# import copy
# from paddle import fluid
# import time
# import numpy as np
# import tempfile
# import shutil
# import inspect
# import importlib
# from collections import OrderedDict
# from ppdet.core.workspace import merge_config, global_config, AttrDict, make_partial
# from ppdet.core.config.schema import extract_schema
from ppdet.data.reader import Reader, _has_empty, _segm
from ppdet.core.config.schema import SchemaDict, SchemaValue, SharedConfig
import math
import logging
logger = logging.getLogger(__name__)


def create_reader(cfg, max_iter=0, global_cfg=None, devices_num=1):
    """
    Return iterable data reader.

    Args:
        max_iter (int): number of iterations.
    """
    if not isinstance(cfg, dict):
        raise TypeError("The config should be a dict when creating reader.")

    # synchornize use_fine_grained_loss/num_classes from global_cfg to reader cfg
    if global_cfg:
        cfg['use_fine_grained_loss'] = getattr(global_cfg,
                                               'use_fine_grained_loss', False)
        cfg['num_classes'] = getattr(global_cfg, 'num_classes', 80)
    cfg['devices_num'] = devices_num
    reader = Reader(**cfg)()

    def _reader():
        n = 0
        while True:
            for _batch in reader:
                if len(_batch) > 0:
                    yield _batch
                    n += 1
                if max_iter > 0 and n == max_iter:
                    return
            reader.reset()
            if max_iter <= 0:
                return

    return _reader, reader



class DetReaderStatus(object):
    """
    update detection reader status
    """

    def __init__(self, reader, cfg, devices_num):
        """

        Args:
            reader:
        """

        self.reader = reader
        image_nums = len(reader._source._roidbs)
        train_epoch_steps = int(image_nums / cfg.TrainReader["batch_size"] / devices_num)
        # 数量不足以训练一个step的情况下，强制训练一个step
        if train_epoch_steps == 0:
            train_epoch_steps = 1
        epoch_nums = math.ceil(cfg.max_iters // train_epoch_steps)
        self.train_epoch_steps = train_epoch_steps

        self.auto_aug_transform = None
        for i, sample_transform in enumerate(reader._source._sample_transforms.transforms):
            if sample_transform.__class__.__name__ == "CustomAutoAugTransform":
                param = sample_transform.get_param()
                sample_transform.reset_param(
                    policy=param["policy"], stage=param["stage"], train_epochs=epoch_nums)
                self.auto_aug_transform = sample_transform
                break

        logger.info(
            "max_iters:{} convert to {} epochs,  each epoch contain {} steps".format(
                cfg.max_iters, epoch_nums, train_epoch_steps))

    def on_epoch_begin(self, epoch, logs=None):
        """on_epoch_begin"""
        if self.auto_aug_transform is not None:
            ret = self.auto_aug_transform.set_epoch(epoch)
            # ret=1: 使用基于epoch级的数据增强策略
            # ret=0: 不使用基于epohc级的数据增强策略
            if ret:
                logger.info(
                    "reader status set epoch:{}, using auto aug transform:{}".format(
                        epoch, self.auto_aug_transform.policy[epoch]))
            else:
                pass

    def on_batch_begin(self, batch, logs=None):
        if batch % self.train_epoch_steps == 0:
            epoch = batch // self.train_epoch_steps
            if self.auto_aug_transform is not None:
                ret = self.auto_aug_transform.set_epoch(epoch)
                # ret=1: 使用基于epoch级的数据增强策略
                # ret=0: 不使用基于epohc级的数据增强策略
                if ret:
                    logger.info(
                        "reader status set epoch:{}, using auto aug transform:{}".format(
                            epoch, self.auto_aug_transform.policy[epoch]))
                else:
                    pass

