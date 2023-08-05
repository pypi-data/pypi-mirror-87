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

from ppdet.data.transform.operators import BaseOperator, ImageError
from ppdet.data.transform.operators import register_op


import numpy as np
from PIL import Image
import copy
import traceback

import logging
logger = logging.getLogger(__name__)
#
@register_op
class CustomAutoAugTransform(BaseOperator):
    """
    CustomAutoAugTransform
    """
    def __init__(self, policy=None, stage="search", train_epochs=None):
        """ Transform the image data to numpy format.

        Args:
            to_rgb (bool): whether to convert BGR to RGB
            with_mixup (bool): whether or not to mixup image and gt_bbbox/gt_score
        """
        # from auto_augment.autoaug.transform.ops.utils import get_policy_schedule_from_file
        # from auto_augment.autoaug.transform.autoaug_transform import DetectorAutoAugTransform
        #
        # assert mode in ["train", "search"]
        #
        # logger.info("CustomAutoAugTransform init")
        # super(CustomAutoAugTransform, self).__init__()
        #
        # if mode == "train":
        #     transform_conf = get_policy_schedule_from_file(
        #         data_aug_file, train_epochs)
        # elif mode == "search":
        #     transform_conf = conf
        #
        # if transform_conf["autoaug_mode"] in ["PBA", "pba"]:
        #     self.auto_aug_transform = DetectorAutoAugTransform(
        #         transform_conf)
        # elif transform_conf["autoaug_mode"] == "aa":
        #     from rudder.rudder_data_augmentation.transform.data_augment_detector_transform \
        #         import SingleAutoAugmentDetectorTransform
        #     self.auto_aug_transform = SingleAutoAugmentDetectorTransform(
        #         transform_conf)
        super(CustomAutoAugTransform, self).__init__()
        from auto_augment.autoaug.transform.autoaug_transform import AutoAugTransform
        assert stage in ["train", "search"]
        self.policy = policy
        self.stage = stage
        self.train_epochs = train_epochs
        if policy is not None:
            self.auto_aug_transform = AutoAugTransform.create(policy, stage=stage, train_epochs=train_epochs)

    def reset_param(self, policy, stage, train_epochs=None):
        """
        用于搜索流程中的重新reset
        Args:
            policy:
            stage:

        Returns:

        """
        from auto_augment.autoaug.transform.autoaug_transform import AutoAugTransform
        assert policy is not None
        self.policy = policy
        self.stage = stage
        if train_epochs is not None:
            self.train_epochs = train_epochs
        self.auto_aug_transform = AutoAugTransform.create(policy, stage=stage, train_epochs=self.train_epochs)

    def get_param(self):
        param = dict(
            policy=self.policy,
            stage=self.stage,
            train_epochs=self.train_epochs
        )
        return param

    def get_non_empty_box_indices(self, boxes):
        """Get indices for non-empty boxes."""
        # Selects indices if box height or width is 0.
        height = boxes[:, 3] - boxes[:, 1]
        width = boxes[:, 2] - boxes[:, 0]

        indices = np.where(np.logical_and(np.greater(height, 0),
                                          np.greater(width, 0)))
        return indices[0]


    def set_epoch(self, indx):
        """

        Args:
            indx:

        Returns:

        """
        self.cur_epoch = indx
        ret = self.auto_aug_transform.set_epoch(self.cur_epoch)
        logger.info("CustomAutoAugTransform cur_epoch:{}".format(indx))
        return ret


    def reset_policy(self, new_hparams):
        """

        Args:
            new_hparams:

        Returns:

        """
        self.auto_aug_transform.reset_policy(new_hparams)


    def __call__(self, sample, context=None):
        """

        Args:
            sample:  "gt_bbox": [xmin, ymin, xmax, ymax]
            context:

        Returns:

        """
        boxes = sample['gt_bbox']
        img = sample['image']
        labels = sample['gt_class']
        gt_score = None
        if 'gt_score' in sample:
            gt_score = sample['gt_score']
        if not isinstance(img, np.ndarray):
            raise TypeError("{}: image is not a numpy array.".format(self))
        if len(img.shape) != 3:
            raise ImageError("{}: image is not 3-dimensional.".format(self))

        img_height, img_width = (img.shape[0], img.shape[1])
        #print("img_height:{}, img_width:{}".format(img_height, img_width))
        boxes = boxes.astype(np.float32)

        # todo box 顺序不一致
        boxes[:, 0] = boxes[:, 0] / img_width
        boxes[:, 2] = boxes[:, 2] / img_width
        boxes[:, 1] = boxes[:, 1] / img_height
        boxes[:, 3] = boxes[:, 3] / img_height
        #print("boxes[:,:] after normalize:{}".format(boxes[:,:]))

        boxes_index = boxes[:, :] > 1
        if boxes_index.any():
            assert 0, "img_height:{}, img_width:{}, box has some cordinate normalize failed: {}".format(
                img_height, img_width, boxes)

        # change box from [xmin, ymin, xmax, ymax] to (min_y, min_x, max_y,
        # max_x), compatible with tensorflow augment
        boxes = boxes[:, [1, 0, 3, 2]]

        boxes_num_before_aug = boxes.shape[0]

        img, boxes = self.auto_aug_transform.apply(img, boxes)

        if boxes.shape[0] != boxes_num_before_aug:
            assert 0, "boxes shape does not fit, origin num:{}, now num:{}".format(
                boxes_num_before_aug, boxes.shape[0])

        # change box back from (min_y, min_x, max_y, max_x) to [xmin, ymin,
        # xmax, ymax]
        boxes = boxes[:, [1, 0, 3, 2]]

        # denormalize box
        boxes[:, 0] = boxes[:, 0] * img_width
        boxes[:, 2] = boxes[:, 2] * img_width
        boxes[:, 1] = boxes[:, 1] * img_height
        boxes[:, 3] = boxes[:, 3] * img_height

        # filter valid box and label
        indices = self.get_non_empty_box_indices(boxes)
        boxes = boxes[indices]
        labels = labels[indices]
        if 'gt_score' in sample:
            gt_score = gt_score[indices]
            sample['gt_score'] = gt_score

        if isinstance(img, Image.Image):
            img = np.asarray(img)

        sample['image'] = img
        sample['gt_bbox'] = boxes
        sample['gt_class'] = labels
        return sample
