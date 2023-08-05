#copyright (c) 2020 PaddlePaddle Authors. All Rights Reserve.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import os
import signal
import paddle
from . import operators as custom_operators
from ppcls.data import imaug
from ppcls.data.imaug import transform
from ppcls.data.reader import SampleNumException, check_params, get_file_list, shuffle_lines, ModeException

from ppcls.utils import logger

trainers_num = int(os.environ.get('PADDLE_TRAINERS_NUM', 1))
trainer_id = int(os.environ.get("PADDLE_TRAINER_ID", 0))

def partial_reader(params, full_lines, transform_ops, part_id=0, part_num=1):
    """
    create a reader with partial data

    Args:
        params(dict):
        full_lines: label list
        part_id(int): part index of the current partial data
        part_num(int): part num of the dataset
    """
    assert part_id < part_num, ("part_num: {} should be larger " \
            "than part_id: {}".format(part_num, part_id))

    full_lines = full_lines[part_id::part_num]

    batch_size = int(params['batch_size']) // trainers_num
    if params['mode'] == "train"  and len(full_lines) < batch_size:
        raise SampleNumException('', len(full_lines), batch_size)

    delimiter = params.get("delimiter", " ")

    def reader():
        #print("full_lines first 5 line:{}".format(full_lines[:5]))
        for line in full_lines:
            img_path, label = line.split(delimiter)
            img_path = os.path.join(params['data_dir'], img_path)
            with open(img_path, 'rb') as f:
                img = f.read()
            yield (transform(img, transform_ops), int(label))

    return reader


def mp_reader(params, transform_ops):
    """
    multiprocess reader

    Args:
        params(dict):
    """
    check_params(params)

    full_lines = get_file_list(params)
    if params["mode"] == "train":
        full_lines = shuffle_lines(full_lines, seed=None)

    part_num = 1 if 'num_workers' not in params else params['num_workers']

    readers = []
    for part_id in range(part_num):
        reader = partial_reader(params, full_lines, transform_ops, part_id, part_num)
        readers.append(reader)

    return paddle.reader.multiprocess_reader(readers, use_pipe=False)


def term_mp(sig_num, frame):
    """ kill all child processes
    """
    pid = os.getpid()
    pgid = os.getpgid(os.getpid())
    logger.info("main proc {} exit, kill process group "
                "{}".format(pid, pgid))
    os.killpg(pgid, signal.SIGKILL)

def create_operators(params):
    """
    create operators based on the config

    Args:
        params(list): a dict list, used to create some operators
    """
    assert isinstance(params, list), ('operator config should be a list')
    ops = []
    for operator in params:
        assert isinstance(operator,
                          dict) and len(operator) == 1, "yaml format error"
        op_name = list(operator)[0]
        param = {} if operator[op_name] is None else operator[op_name]
        if hasattr(imaug, op_name):
            op = getattr(imaug, op_name)(**param)
        else:
            op = getattr(custom_operators, op_name)(**param)
        ops.append(op)
    return ops


class Reader:
    """
    Create a reader for trainning/validate/test

    Args:
        config(dict): arguments
        mode(str): train or val or test
        seed(int): random seed used to generate same sequence in each trainer

    Returns:
        the specific reader
    """

    def __init__(self, config, mode='train', seed=None):
        try:
            self.params = config[mode.upper()]
        except KeyError:
            raise ModeException(mode=mode)

        use_mix = config.get('use_mix')
        self.params['mode'] = mode
        if seed is not None:
            self.params['shuffle_seed'] = seed
        self.batch_ops = []
        if use_mix and mode == "train":
            self.batch_ops = create_operators(self.params['mix'])
        self.transform_ops = create_operators(self.params['transforms'])
        self.auto_aug_transform = None
        for op in self.transform_ops:
            if op.__class__.__name__ == "CustomAutoAugTransform":
                self.auto_aug_transform = op

    def set_epoch(self, epoch):
        self.epoch = epoch
        if self.auto_aug_transform:
            self.auto_aug_transform.set_epoch(epoch)

    def reset_policy(self, new_hparams):
        """

        Args:
            new_hparams:

        Returns:

        """
        if self.auto_aug_transform:
            self.auto_aug_transform.reset_policy(new_hparams)

    def __call__(self):
        batch_size = int(self.params['batch_size']) // trainers_num
        def wrapper():
            reader = mp_reader(self.params, self.transform_ops)
            batch = []
            for idx, sample in enumerate(reader()):
                img, label = sample
                batch.append((img, label))
                if (idx + 1) % batch_size == 0:
                    batch = transform(batch, self.batch_ops)
                    yield batch
                    batch = []

        return wrapper


signal.signal(signal.SIGINT, term_mp)
signal.signal(signal.SIGTERM, term_mp)
