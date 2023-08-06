import numpy as np
from rs4 import pathtool, attrdict
from hashlib import md5
import os
import math
import rs4
import random
import pickle
from .label import Label
from .normalizer import Normalizer
import tensorflow as tf
from sklearn.utils import class_weight


class Datasets:
    def __init__ (self, steps, trainset, validset, testset = None, labels = None, normalizer = None, meta = None, save_testset = True):
        self.steps = steps
        self.trainset = trainset
        self.validset = validset
        self.testset = testset
        if testset is None:
            self.testset = validset
        self.save_testset = save_testset
        self.labels = labels
        self.normalizer = normalizer
        self.meta = attrdict.AttrDict (meta or {})
        self.raw_testset = [None, None]

    def get_class_weight (self, aslist = False):
        ys_ = []
        for xs, ys in self.testset.as_numpy_iterator ():
            ys_.extend (ys)
        ys = np.argmax (ys_, 1)
        weights = class_weight.compute_class_weight ('balanced', classes = np.unique (ys), y = ys)
        if aslist:
            return weights.tolist ()
        return { idx: weight for idx, weight in enumerate (weights) }

    def shapes (self):
        if 'shapes' in self.meta:
            return self.meta ["shapes"]
        xs, ys = next (self.testset.as_numpy_iterator ())
        self.meta ["shapes"] = xs.shape [1:], ys.shape [1:]
        return self.meta ["shapes"]

    def _to_numpy (self, data):
        if isinstance (data, tuple):
            return tuple ([ np.array (each) for each in data ])
        else:
            return np.array (data)

    def _collect (self, data, index):
        if isinstance (data, tuple):
            if self.raw_testset [index] is None:
                self.raw_testset [index] = tuple ([[] for i in range (len (data))])
            for idx, v in enumerate (data):
                self.raw_testset [index][idx].extend (v)
        else:
            if self.raw_testset [index] is None:
                self.raw_testset [index] = []
            self.raw_testset [index].extend (data)

    def collect_testset (self):
        if self.raw_testset [0] is not None:
            return self.raw_testset
        for xs, ys in self.testset.as_numpy_iterator ():
            self._collect (xs, 0)
            self._collect (ys, 1)
        self.raw_testset = (self._to_numpy (self.raw_testset [0]), self._to_numpy (self.raw_testset [1]))
        return self.raw_testset

    def testset_as_numpy (self):
        if self.raw_testset [0] is None:
            self.collect_testset ()
        return self.raw_testset

    def save (self, assets_dir, save_testset = True): # typically checkpoint/assets
        pathtool.mkdir (assets_dir)
        if self.labels:
            obj = [ (lb._origin, lb.name) for lb in self.labels ]
            with open (os.path.join (assets_dir, 'labels'), 'wb') as f:
                f.write (pickle.dumps (obj))
        self.normalizer and self.normalizer.save (assets_dir)
        if self.save_testset and save_testset:
            with open (os.path.join (assets_dir, 'testset'), 'wb') as f:
                f.write (pickle.dumps (self.collect_testset ()))
        if self.meta:
            with open (os.path.join (assets_dir, 'meta'), 'wb') as f:
                f.write (pickle.dumps (self.meta))

    @classmethod
    def load (cls, assets_dir):
        lables, testset, raw_testset, meta = None, None, None, None
        if os.path.isfile (os.path.join (assets_dir, 'labels')):
            with open (os.path.join (assets_dir, 'labels'), 'rb') as f:
                labels = [Label (classes, name) for classes, name in pickle.loads (f.read ())]

        if os.path.isfile (os.path.join (assets_dir, 'meta')):
            with open (os.path.join (assets_dir, 'meta'), 'rb') as f:
                meta = pickle.loads (f.read ())

        if os.path.isfile (os.path.join (assets_dir, 'testset')):
            with open (os.path.join (assets_dir, 'testset'), 'rb') as f:
                testset = pickle.loads (f.read ())
                print (testset)
                raw_testset = testset
                testset = tf.data.Dataset.from_tensor_slices (testset).batch (64)

        dss = Datasets (0, None, None, testset, labels, Normalizer.load (assets_dir), meta)
        dss.raw_testset = raw_testset
        return dss

def load (assets_dir):
    return Datasets.load (assets_dir)
