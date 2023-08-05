"""
# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

class CustomAutoAugTransform(object):
    """
    CustomAutoAugTransform
    """

    def __init__(self, policy, stage="search", train_epochs=None):
        """

        Args:
            stage:
            conf: search conf
            data_aug_file: train aug file
            train_epochs:
        """
        from auto_augment.autoaug.transform.autoaug_transform import AutoAugTransform
        assert stage in ["train", "search"]
        self.auto_aug_transform = AutoAugTransform.create(policy, stage=stage, train_epochs=train_epochs)

    def set_epoch(self, indx):
        """

        Args:
            indx:

        Returns:

        """
        self.cur_epoch = indx
        self.auto_aug_transform.set_epoch(self.cur_epoch)



    def reset_policy(self, new_hparams):
        """

        Args:
            new_hparams:

        Returns:

        """
        self.auto_aug_transform.reset_policy(new_hparams)


    def __call__(self, img):
        """

        Args:
            sample:  "gt_bbox": [xmin, ymin, xmax, ymax]
            context:

        Returns:
        """
        img = self.auto_aug_transform.apply(img)
        return img


