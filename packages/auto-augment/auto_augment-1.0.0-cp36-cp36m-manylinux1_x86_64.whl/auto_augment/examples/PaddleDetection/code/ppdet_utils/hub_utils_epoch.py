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

import yaml
import re
import os
import copy
from paddle import fluid
import time
import numpy as np
import tempfile
import shutil
import inspect
import importlib
from collections import OrderedDict
from ppdet.core.workspace import merge_config, global_config, AttrDict, make_partial
from ppdet.core.config.schema import extract_schema
from ppdet.data.reader import Reader, _has_empty, _segm
from ppdet.core.config.schema import SchemaDict, SchemaValue, SharedConfig
import logging
logger = logging.getLogger(__name__)

def eval_run(exe, compile_program, reader, loader, keys, values, cls):
    """
    Run evaluation program, return program outputs.
    """
    iter_id = 0
    results = []
    if len(cls) != 0:
        values = []
        for i in range(len(cls)):
            _, accum_map = cls[i].get_map_var()
            cls[i].reset(exe)
            values.append(accum_map)

    images_num = 0
    start_time = time.time()
    has_bbox = 'bbox' in keys

    for it, data in enumerate(loader()):
        outs = exe.run(compile_program,
                       feed=data,
                       fetch_list=values,
                       return_numpy=False)

        res = {
            k: (np.array(v), v.recursive_sequence_lengths())
            for k, v in zip(keys, outs)
        }
        results.append(res)
        if iter_id % 100 == 0:
            logger.info('Test iter {}'.format(iter_id))
        iter_id += 1
        images_num += len(res['bbox'][1][0]) if has_bbox else 1

    end_time = time.time()
    fps = images_num / (end_time - start_time)
    if has_bbox:
        logger.info('Total number of images: {}, inference time: {} fps.'.
                    format(images_num, fps))
    else:
        logger.info('Total iteration: {}, inference time: {} batch/s.'.format(
            images_num, fps))

    return results

def create_reader(cfg, global_cfg=None, devices_num=1):
    """
    Return iterable data reader.

    Args:
        max_iter (int): number of iterations.
    """
    if not isinstance(cfg, dict):
        raise TypeError("The config should be a dict when creating reader.")

    # synchornize use_fine_grained_loss/num_classes from global_cfg to reader
    # cfg
    if global_cfg:
        cfg['use_fine_grained_loss'] = getattr(global_cfg,
                                               'use_fine_grained_loss', False)
        cfg['num_classes'] = getattr(global_cfg, 'num_classes', 80)
    cfg['devices_num'] = devices_num
    reader = Reader(**cfg)()

    def _reader():
        while True:
            n = 0
            for _batch in reader:
                if len(_batch) > 0:
                    yield _batch
                    n += 1
                # if max_iter > 0 and n == max_iter:
                #     return
            reader.reset()
            # 迭代器无数据的情况下不能return, 要重启
            # 因paddle detection reader已重构，不再深究其bug, 后续直接升级reader
            # 目前保障功能完好
            if n != 0:
                # 每个epoch返回
                return
            # if max_iter <= 0:
            #     return

    return _reader, reader


class DetReaderStatus(object):
    """
    update detection reader status
    """

    def __init__(self, reader):
        """

        Args:
            reader:
        """

        self.reader = reader

        self.auto_aug_transform = None
        for i, sample_transform in enumerate(reader._source._sample_transforms.transforms):
            if sample_transform.__class__.__name__ == "CustomAutoAugTransform":
                self.auto_aug_transform = sample_transform
                break

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