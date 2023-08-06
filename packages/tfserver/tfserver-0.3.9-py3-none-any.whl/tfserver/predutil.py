import numpy as np
import math
from sklearn.utils.extmath import softmax as softmax_
import hyperopt
import os
from rs4 import annotations
from . import cli
from . import loaders

def softmax (x):
    x = np.array (x)
    if len (x.shape) == 2:
        return softmax_ (x).tolist ()
    return softmax_ ([x])[0].tolist ()

def sigmoid (x):
    return [1 / (1 + np.exp(-e)) for e in x]

def confusion_matrix (labels, predictions, num_labels):
  rows = []
  for i in range (num_labels):
    row = np.bincount (predictions[labels == i], minlength=num_labels)
    rows.append (row)
  return np.vstack (rows)

def render_trial (space, trial, stringfy = False):
    if trial.get ("misc"):
        trial = dict ([(k, v [0]) for k, v in trial ["misc"]["vals"].items ()])
    params = hyperopt.space_eval(space, trial)
    if stringfy:
        return ", ".join (["{}: {}".format (k, v) for k, v in params.items ()])
    return params

def get_latest_model (path):
    if not os.path.isdir (path) or not os.listdir (path):
        return
    version = max ([int (ver) for ver in os.listdir (path) if ver.isdigit () and os.path.isdir (os.path.join (path, ver))])
    return os.path.join (path, str (version))

def confidence_interval (level, error, n):
    c = {90: 1.64, 95: 1.96, 98: 2.33, 99: 2.58}[level]
    return c * math.sqrt((error * (1 - error)) / n)


# deprecated model loaders ------------------------------------------------
class CheckPoint (loaders.CheckPoint):
    @annotations.deprecated ('use tfserver.loaders.CheckPoint.predict')
    def predict (self, xs):
        return self.net.run (self.net.logit, x = self.net.normalize (xs)) [0]


class SavedModel (loaders.SavedModel):
    @annotations.deprecated ('use tfserver.loaders.SavedModel.predict')
    def predict (self, x, **kargs):
        y = self.stub.run (x, **kargs)[0]
        return y.astype (np.float64)


class TFLite (loaders.TFLite):
    @annotations.deprecated ('use tfserver.loaders.TFLite.predict')
    def predict (self, x, **kargs):
        ys = []
        for x_ in x:
            ys.append (self.stub.run (x_, **kargs)[0].astype (np.float64))
        return np.array (ys)


class TFServer (loaders.TFServer):
    @annotations.deprecated ('use tfserver.loaders.TFServer.predict')
    def predict (self, x, **kargs):
        resp = self.stub.predict (self.alias, 'predict', x = x, **kargs)
        return resp.y

