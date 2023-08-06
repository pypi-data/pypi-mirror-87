__version__ = "0.3.9"

import tensorflow as tf
import os
import numpy as np
import time
import pickle
from tensorflow.python.framework import tensor_util
from tensorflow.core.framework import tensor_pb2
import sys
from .label import Label
import threading
from rs4 import pathtool
import shutil

glock = threading.RLock ()
MODEL_BASE_DIR = None

def preference (path = None):
    import skitai
    pref =  skitai.preference (path = path)
    pref.config.tf_models = {}
    return pref

def get_latest_version (model_root):
    vs = [ int (v) for v in os.listdir (model_root) if v.isdigit () ]
    if not vs:
        return None
    return sorted (vs) [-1]

class Session:
    def __init__ (self, model_dir, tfconfig = None):
        from . import saved_model

        self.model_dir = model_dir
        try:
            self.version = int (os.path.basename (model_dir))
        except:
            self.version = 0
        self.model_root = os.path.dirname (model_dir)
        self.tfconfig = tfconfig
        self.graph = tf.Graph ()
        self.tfsess = tf.compat.v1.Session (config = tfconfig, graph = self.graph)
        self.interp = saved_model.load (model_dir, self.tfsess)
        self.labels = self.interp.labels

    def remove_all_resources (self):
        shutil.rmtree (self.model_root)

    def remove_version (self, version):
        deletable = os.path.join (self.model_root, str (version))
        if not os.path.isdir (deletable):
            return
        shutil.rmtree (deletable)

    def add_version (self, version, asset_zfile):
        target = os.path.join (self.model_root, str (version))
        pathtool.unzipdir (asset_zfile, target)

    def get_version (self):
        return self.version

    def run (self, feed_dict, signature_def_name = tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY):
        return self.interp._run_output (feed_dict, signature_def_name)

    def close (self):
        self.tfsess.close ()

    def get_latest_version (self):
        return get_latest_version (self.model_root)


tfsess = {}
def load_model (alias, model_dir, tfconfig = None):
    global tfsess
    if isinstance (tfconfig, float):
        tfconfig = tf.compat.v1.ConfigProto(
            gpu_options = tf.compat.v1.GPUOptions (per_process_gpu_memory_fraction = tfconfig),
            log_device_placement = False
        )
    sess = Session (model_dir, tfconfig)
    with glock:
        tfsess [alias] = sess

added_models = {}
def load_models ():
    global added_models
    loaded = []
    for alias, (model_dir, tfconfig) in added_models.items ():
        load_model (alias, model_dir, tfconfig)
        loaded.append ((alias, model_dir))
    return loaded

def add_model (alias, model_dir, gpu_usage):
    global added_models
    with glock:
        added_models [alias] = (model_dir, gpu_usage)

def add_models_from_directory (base, gpu_usage = 0.1):
    global MODEL_BASE_DIR

    MODEL_BASE_DIR = base
    for alias in os.listdir (base):
        if alias.startswith ('#'):
            continue
        model_root = os.path.join (base, alias)
        version = str (get_latest_version (model_root))
        if version is None:
            continue
        add_model (alias, os.path.join(model_root, str (version)), gpu_usage)

def close (alias = None):
    global tfsess
    if alias:
        with glock:
            if alias not in tfsess:
                return
            tfsess [alias].close ()
            del tfsess [alias]
            return

    with glock:
        for sess in tfsess.values ():
            sess.close ()
        tfsess = {}

# public methods --------------------------
def predict (alias, signature_name = 'predict', **inputs):
    global tfsess

    interp = tfsess [alias].interp
    numpy_inputs = {}
    for k, v in inputs.items ():
        if isinstance(v, tensor_pb2.TensorProto):
            v = tensor_util.MakeNdarray (v)
        elif type (v) is not np.ndarray:
            v = np.array (v)
        numpy_inputs [k] = v
    return interp.predict (numpy_inputs, signature_name)

run = predict

def get_labels (alias):
    with glock:
        return tfsess [alias].labels

def get_model (alias):
    global tfsess
    with glock:
        return tfsess.get (alias)

def models ():
    global tfsess
    with glock:
        return list (tfsess.keys ())

def delete_model (alias):
    model = get_model (alias)
    close (alias)
    model.remove_all_resources ()

def refresh_model (alias):
    model = get_model (alias)
    close (alias)
    version = model.get_latest_version ()
    if not version:
        return
    load_model (alias, os.path.join (model.model_root, str (version)), model.tfconfig)

def get_model_base_directory ():
    global MODEL_BASE_DIR

    if MODEL_BASE_DIR:
        return MODEL_BASE_DIR

    dirs = {}
    for model_name in models ():
        m = get_model (model_name)
        root = os.path.dirname (m.model_root)
        try: dirs [root] += 1
        except KeyError: dirs [root] = 1
    MODEL_BASE_DIR = sorted (dirs.items (), key = lambda x: x [1]) [-1][0]
    return MODEL_BASE_DIR

def delete_model_versions (alias, versions):
    if isinstance (versions, int):
        versions = [versions]
    versions = sorted (map (int, versions))
    model = get_model (alias)
    for version in versions:
        model.remove_version (version)
        if model.version == version:
            refresh_model (alias)

def add_model_version (alias, version, asset_zfile, refresh = True, overwrite = False):
    model = get_model (alias)
    if model:
        model_dir = os.path.join (model.model_root, str (version))
        if not overwrite:
            assert not os.path.exists (model_dir)
        model.add_version (version, asset_zfile)
        refresh and refresh_model (alias)
        return

    root_dir = get_model_base_directory ()
    model_dir = os.path.join (root_dir, alias, str (version))
    pathtool.unzipdir (asset_zfile, model_dir)
    refresh and load_model (alias, model_dir, 0.1)
