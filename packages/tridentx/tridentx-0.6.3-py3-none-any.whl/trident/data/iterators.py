from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy
import hashlib
import inspect
import itertools
import builtins
import os
import pickle
import random
import string
import sys
import threading
import time
from enum import Enum, unique
from typing import List, TypeVar, Iterable, Tuple, Union, Dict
import numpy as np
from skimage import color

from trident.data.bbox_common import xywh2xyxy, xyxy2xywh
from trident.data.image_common import gray_scale, image2array, mask2array, image_backend_adaption, reverse_image_backend_adaption, \
    unnormalize, array2image,  GetImageMode
from trident.data.label_common import label_backend_adaptive
from trident.data.mask_common import mask_backend_adaptive, color2label
from trident.data.text_common import text_backend_adaption,reverse_text_backend_adaption
from trident.data.samplers import *
from trident.backend.common import *
from trident.backend.tensorspec import *

from trident.data.dataset import *
try:
    import Queue
except ImportError:
    import queue as Queue

if get_backend() == 'pytorch':
    from trident.backend.pytorch_backend import to_numpy, to_tensor
    import torch
elif get_backend() == 'tensorflow':
    from trident.backend.tensorflow_backend import to_numpy, to_tensor
class IteratorV2(object):
    def __init__(self, data:(Dataset,Dict[str,Dataset])=None, label:(Dataset,Dict[str,Dataset])=None, mask:(Dataset,Dict[str,Dataset])=None, unpair:(Dataset,Dict[str,Dataset])=None,is_shuffle=True, sample_filter=None, minibatch_size=8):
        self.is_pair_process = False
        self.signature = None
        self._data = data
        self._label =OrderedDict()
        self._unpair = unpair
        self._mask=mask
        self.is_shuffle=is_shuffle
        self.workers = 2
        self.itr = 0

        if isinstance(self._label, (MaskDataset, ImageDataset, BboxDataset, ZipDataset)) and isinstance(self._data, ImageDataset) and len(self._label) == len(self._data):
            self._label.is_pair_process = self._data.is_pair_process = self.is_pair_process = True
        elif isinstance(self._label, TextSequenceDataset) and isinstance(self._data, TextSequenceDataset) and len(self._label) == len(self._data):
            self._label.is_pair_process = self._data.is_pair_process = self.is_pair_process = True
        elif isinstance(self._label, dict):
            for i,(k,v) in enumerate(self.label):
                labeldata=v
                if labeldata.symbol is None:
                    labeldata.symbol=k
                if isinstance(labeldata, (MaskDataset, ImageDataset, BboxDataset, ZipDataset)) and isinstance(self._data, ImageDataset) and len(labeldata) == len(
                        self._data):
                    labeldata.is_pair_process = self._data.is_pair_process = self.is_pair_process = True
                elif isinstance(labeldata, TextSequenceDataset) and isinstance(self._data, TextSequenceDataset) and len(labeldata) == len(self._data):
                    labeldata.is_pair_process = self._data.is_pair_process = self.is_pair_process = True
        #
        # elif inspect.isgenerator(label)  and isinstance(self._data, TextSequenceDataset) and len(self._label) == len(self._data):
        #     self._label.is_pair_process = self._data.is_pair_process = self.is_pair_process = True
        # else:
        #     self._label.is_pair_process = self._data.is_pair_process = self.is_pair_process = False


        self._minibatch_size = minibatch_size
        self.paired_transform_funcs = []
        self.batch_sampler = BatchSampler(self, self._minibatch_size, is_shuffle=True, drop_last=False)
        self._sample_iter = iter(self.batch_sampler)
        self.buffer_size = 10
        self.out_queue = Queue.Queue(maxsize=self.buffer_size)
        self.sample_filter = None
        if inspect.isfunction(sample_filter) or callable(sample_filter) :
            self.sample_filter = sample_filter
            self.batch_sampler.sample_filter = self.sample_filter

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        if self._label is not None and isinstance(self._label, (MaskDataset, BboxDataset, ImageDataset)) and isinstance(self._data, ImageDataset) and len(self._label) == len(
                self._data):
            self._label.is_pair_process = self._data.is_pair_process = self.is_pair_process = True
        else:
            self._label.is_pair_process = self._data.is_pair_process = self.is_pair_process = False

        self.batch_sampler = BatchSampler(self, self._minibatch_size, is_shuffle=True, drop_last=False)
        self.batch_sampler.sample_filter = self.sample_filter
        self._sample_iter = iter(self.batch_sampler)


    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        if isinstance(self._label, (MaskDataset, ImageDataset, BboxDataset)) and isinstance(self._data, ImageDataset) and len(
                self._label) == len(self._data):
            self._label.is_pair_process = self._data.is_pair_process = self.is_pair_process = True
        else:
            self._label.is_pair_process = self._data.is_pair_process = self.is_pair_process = False
        self.batch_sampler.sample_filter = self.sample_filter
        self._sample_iter = iter(self.batch_sampler)

    @property
    def unpair(self):
        return self._unpair

    @unpair.setter
    def unpair(self, value):
        self._unpair = value
        self.batch_sampler.sample_filter = self.sample_filter
        self._sample_iter = iter(self.batch_sampler)

    @property
    def palette(self):
        if isinstance(self._label, MaskDataset) and self._label.expect_data_type in [ExpectDataType.label_mask, ExpectDataType.color_mask]:
            return self._label.palette
        else:
            return None

    @property
    def minibatch_size(self):
        return self._minibatch_size

    @minibatch_size.setter
    def minibatch_size(self, value):
        self._minibatch_size = value
        self.batch_sampler = BatchSampler(self, self._minibatch_size, is_shuffle=True, drop_last=False)
        self.batch_sampler.sample_filter = self.sample_filter
        self._sample_iter = iter(self.batch_sampler)

    def update_signature(self, arg_names):
        iterdata = self.next()
        if self.signature is None or not isinstance(self.signature, Signature):
            self.signature = Signature()
            self.signature.name = 'data_provider'
        if isinstance(arg_names, (list, tuple)) and len(iterdata) == len(arg_names):
            for i in range(len(arg_names)):
                arg = arg_names[i]
                data = iterdata[i]
                self.signature.outputs[arg] = (-1,) + data.shape[1:] if data.ndim > 1 else (-1)

        elif not isinstance(arg_names, (list, tuple)):
            raise ValueError('arg_names should be list or tuple')
        elif len(self.signature.key_list) != len(arg_names):
            raise ValueError('data feed and arg_names should be the same length')
        else:
            self.signature = None
            iterdata = self.next()

    def paired_transform(self, img_data, paired_img):

        if isinstance(img_data, list) and all(isinstance(elem, np.ndarray) for elem in img_data):
            img_data = np.asarray(img_data)
        if isinstance(img_data, str) and os.path.isfile(img_data) and os.path.exists(img_data):
            img_data = image2array(img_data)

        if len(self.paired_transform_funcs) == 0:
            return img_data, paired_img
        if isinstance(img_data, np.ndarray):
            # if img_data.ndim>=2:
            for fc in self.paired_transform_funcs:
                try:
                    img_data, paired_img = fc(img_data, paired_img)
                except:
                    PrintException()

            return img_data, paired_img
        else:
            return img_data, paired_img

    def __getitem__(self, index: int):
        # start = time.time()

        try:
            bbox = None
            mask = None
            data = self.data.__getitem__(index % len(self.data)) if self.data is not None and len(self.data) > 0 else None

            label1 = self.label[index % len(self.label)]
            label = self.label.__getitem__(index % len(self.label)) if self.label is not None and len(self.label) > 0 else None
            # stop = time.time()
            # print('get label:{0}'.format(stop - start))
            # start = stop
            if isinstance(self.label, (BboxDataset, LandmarkDataset)):
                data, label = self.paired_transform(data, label)
                if hasattr(self.data, 'image_transform'):
                    data = self.data.image_transform(data)
                if hasattr(self.label, 'bbox_transform'):
                    new_label = self.label.bbox_transform(label)
                    if isinstance(new_label, tuple):
                        bbox, label = new_label
                    else:
                        bbox = new_label
                        label=None
                else:
                    bbox = label
                    label = None
            elif isinstance(self.label, MaskDataset):
                data, label = self.paired_transform(data, label)
                if hasattr(self.data, 'image_transform'):
                    data = self.data.image_transform(data)
                if hasattr(self.label, 'mask_transform'):
                    new_label = self.label.mask_transform(label)
                    if isinstance(new_label, tuple):
                        mask, label = new_label
                    else:
                        mask = new_label
                else:
                    mask = label.copy()
                label = None
            elif isinstance(self.label, ImageDataset):
                data, label = self.paired_transform(data, label)
                # stop = time.time()
                # print('paired_transform:{0}'.format(stop - start))
                # start = stop
                if hasattr(self.data, 'image_transform'):
                    data = self.data.image_transform(data)  # stop = time.time()  # print('data image_transform:{0}'.format(stop - start))  #
                    # start = stop
                if hasattr(self.label, 'image_transform'):
                    label = self.label.image_transform(label)  # stop = time.time()  # print('label image_transform:{0}'.format(stop - start))  #
                    # start = stop
            else:
                if hasattr(self.label, 'label_transform'):
                    label = self.label.label_transform(label)

            if hasattr(self.label, 'label_transform') and not isinstance(self.label, (BboxDataset, MaskDataset)):
                label = self.label.label_transform(label)

            unpair = self.unpair.__getitem__(index % len(self.unpair)) if len(self.unpair) > 0 else None

            return_data = []
            if self.signature is None or len(self.signature) == 0:
                self.signature = Signature()
                self.signature.name = 'data_provider'
                if data is not None:
                    self.signature.outputs['data' if self.data.symbol is None or len(self.data.symbol) == 0 else self.data.symbol] = (-1,) + data.shape
                if bbox is not None:
                    self.signature.outputs['bbox' if self.label.symbol is None or len(self.label.symbol) == 0 else self.label.symbol] = (-1,) + bbox.shape
                if mask is not None:
                    self.signature.outputs['mask' if self.label.symbol is None or len(self.label.symbol) == 0 else self.label.symbol] = (-1,) + mask.shape
                if label is not None:
                    self.signature.outputs['label' if self.label.symbol is None or len(self.label.symbol) == 0 or self.label.symbol in self.signature else self.label.symbol] = (
                                                                                                                                                                                -1,) + label.shape if isinstance(
                        label, np.ndarray) else (-1,)
                if unpair is not None:
                    self.signature.outputs['unpair' if self.unpair.symbol is None or len(self.unpair.symbol) == 0 else self.unpair.symbol] = (
                                                                                                                                             -1,) + unpair.shape  # stop =
                    # time.time()  #
                    # print('signature:{0}'.format(stop - start))  # start = stop

            if data is not None:
                return_data.append(data)
            if bbox is not None:
                return_data.append(bbox)
            if mask is not None:
                return_data.append(mask)
            if label is not None:
                return_data.append(label)
            if unpair is not None:
                return_data.append(unpair)
            # stop = time.time()
            # print('prepare tuple:{0}'.format(stop - start))
            # start = stop
            return tuple(return_data)
        except:
            PrintException()

    def _next_index(self):
        return next(self._sample_iter)

    def __iter__(self):
        return self._sample_iter

    # return a batch , do minimal fetch before return
    def next(self):
        if self.out_queue.qsize() == 0:
            in_data = self._sample_iter.__next__()
            self.out_queue.put(in_data, False)

        out_data = self.out_queue.get(False)

        if self.out_queue.qsize() <= self.buffer_size // 2:
            for i in range(2):
                in_data = self._sample_iter.__next__()
                self.out_queue.put(in_data, False)

        return out_data

    # yield a batch , and trigger following fetch after yield
    def __next__(self):
        if self.out_queue.qsize() == 0:
            in_data = self._sample_iter.__next__()
            self.out_queue.put(in_data, False)

        out_data = self.out_queue.get(False)

        yield out_data
        if self.out_queue.qsize() <= self.buffer_size // 2:
            for i in range(self.buffer_size - self.out_queue.qsize()):
                in_data = self._sample_iter.__next__()
                self.out_queue.put(in_data, False)

    def __len__(self):
        return max([len(self.data) if self.data is not None else 0, len(self.unpair) if self.unpair is not None else 0])
