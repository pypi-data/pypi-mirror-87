import numpy as np
import pickle
import os

def _get_scaling_range (normrange):
    if isinstance (normrange, (list, tuple)):
        scale_min, scale_max = normrange
    else:
        scale_min, scale_max = -1, 1
    return scale_min, scale_max

def standardize (x, mean, std):
    return (x - mean) / std

def scaling (x, min_, gap, normrange):
    scale_min, scale_max = _get_scaling_range (normrange)
    return np.clip (scale_min + (scale_max - scale_min) * ((x - min_) / gap), scale_min, scale_max)

def normalize (x, *args):
    pca = None
    if isinstance (x, list):
        x = np.array (x)
    if len (args) == 8:
        # old version
        mean, std, min_, gap, pca_k, pca, _normalize, _standardize = args
    else:
        mean, std, min_, gap, pca_k, eigen_vecs, pca_mean, _normalize, _standardize = args

    if _standardize: # 0 mean, 1 var
        x = standardize (x, mean, std)
    if _normalize: # -1 to 1
        x = scaling (x, min_, gap, normalize)

    if pca_k: # PCA
        orig_shape = x.shape
        if len (orig_shape) == 3:
            x = x.reshape ([orig_shape [0]  * orig_shape [1], orig_shape [2]])
        if pca:
            # for old version
            x = pca.transform (x)
        else:
            x = np.dot (x - pca_mean, eigen_vecs)
        if len (orig_shape) == 3:
            x = x.reshape ([orig_shape [0], orig_shape [1], pca_k])

    return x


class Normalizer:
    version = 'v2'
    def __init__ (self, normrange = None, standardize = False, axis = 0):
        self.normrange = normrange
        self.standardize = standardize
        self.axis = axis
        self.mean, self.std = None, None
        self.min_, self.gap = None, None

    def fitted (self):
        return self.mean is not None

    def transform_or_fit (self, x):
        if not self.fitted ():
            return self.fit_transform (x)
        else:
            return self.transform (x)

    def fit_transform (self, x):
        self.fit (x)
        return self.transform (x)

    def transform (self, x):
        if self.standardize:
            x = standardize (x, self.mean, self.std)
        if self.normrange:
            x = scaling (x, self.min_, self.gap, self.normrange)
        return x

    def fit (self, x):
        self.mean = np.mean (x, self.axis, keepdims = True)
        self.std = np.std (x, self.axis, keepdims = True) + 1e-8
        if self.standardize:
            x = standardize (x, self.mean, self.std)
        self.min_ = np.min (x, self.axis, keepdims = True)
        self.gap = (np.max (x, self.axis, keepdims = True) - self. min_) + 1e-8

    def save (self, path):
        args = (
            self.version,
            self.normrange,
            self.standardize,
            self.axis,
            self.mean, self.std,
            self.min_, self.gap
        )
        with open (os.path.join (path, 'normfactors'), 'wb') as f:
            f.write (pickle.dumps (args))

    @classmethod
    def load (cls, path):
        path = os.path.join (path, 'normfactors')
        if not os.path.isfile (path):
            return
        with open (path, 'rb') as f:
            args = pickle.loads (f.read ())

        if args [0] == 'v2':
            version, normrange, standardize, axis, mean, std, min_, gap = args
        else:
            axis = 0
            version = 'v1'
            if len (args) == 8:
                # old version
                mean, std, min_, gap, _, _, normrange, standardize = args
            else:
                mean, std, min_, gap, _, _, _, normrange, standardize = args

        n = Normalizer (normrange, standardize, axis)
        n.version = version
        n.mean = mean
        n.std = std
        n.min_ = min_
        n.gap = gap
        return n
