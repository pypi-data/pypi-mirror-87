import numpy as np
import math
from sklearn.utils.extmath import softmax as softmax_
import hyperopt
import os
from rs4.webkit import siesta
from . import cli

class CheckPoint:
    def __init__ (self, net):
        self.net = net

    def ftest (self, xs, ys, **kargs):
        return self.net.ftest (self.net.normalize (xs), ys, **kargs)

    def predict (self, xs):
        return self.net.run (self.net.logit, x = self.net.normalize (xs)) [0]


class SavedModel:
    def __init__ (self, model_root, debug = False):
        from .predutil import get_latest_model

        self.model_root = model_root
        self.debug = debug
        self.model_path = get_latest_model (self.model_root)
        self.stub = self.create_stub (self.model_path)
        self.version = os.path.basename (self.model_path)

    def create_stub (self, model_path):
        from . import saved_model
        return saved_model.load (model_path)

    def predict (self, **kargs):
        return self.stub.run (**kargs)


class TFLite (SavedModel):
    def __init__ (self, model_root, model_file = "model.tflite", debug = False):
        self.model_file = model_file
        SavedModel.__init__ (self, model_root, debug)

    def create_stub (self, model_path):
        from . import tflite

        return tflite.load (
            os.path.join (model_path, self.model_file),
            (128, 128)
        )

    def predict (self, **kargs):
        ys = []
        for x_ in x:
            ys.append (self.stub.run (**kargs)[0].astype (np.float64))
        return np.array (ys)


class TFServer:
    def __init__ (self, endpoint, alias, debug = False):
        self.endpoint = endpoint
        self.alias = alias
        self.debug = debug

        self.stub = cli.Server (endpoint)
        api = siesta.API (endpoint)
        resp = api.models (self.alias).version.get ()
        self.version = resp.data.version

    def predict (self, **kargs):
        return self.stub.predict (self.alias, 'predict', **kargs)
