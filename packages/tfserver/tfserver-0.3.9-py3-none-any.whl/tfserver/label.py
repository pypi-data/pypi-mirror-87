import numpy as np
import copy
import pickle

class Labels:
    def __init__ (self, labels = []):
        self.labels = labels

    def __getattr__ (self, item):
        if isinstance(item, str) and item[:2] == item[-2:] == '__':
            # skip non-existing dunder method lookups
            raise AttributeError(item)
        return getattr (self.labels, item)

    def __len__ (self):
        return len (self.labels)

    def __getitem__(self, sliced):
        return self.labels [sliced]

    def __repr__ (self):
        return repr (self.labels)

    def add (self, label):
        self.labels.append (label)

    def encode (self, *args):
        assert len (args) == len (self.labels)
        y = []
        for idx, label in enumerate (self.labels):
            val = args [idx]
            if isinstance (val, dict):
                y = label.setval (val, prefix = y)
            elif isinstance (val, (list, tuple)):
                y = label.ones (val, prefix = y)
            else:
                y = label.onehot (val, prefix = y)
        return y


class Label:
    def __init__ (self, items = None, name = "label"):
        self._origin = items or set ()
        self.name= name
        self._indexes = {}
        self._origin and self.systemize ()

    def systemize (self):
        if isinstance (self._origin, set):
            self._origin = sorted (list (self._origin))

        if isinstance (self._origin, (list, tuple)):
            self._set = self._origin [:]
        else:
            assert isinstance (self._origin, dict)
            try:
                assert len (self._origin) > 1
                items_ = sorted (self._origin.items (), key = lambda x: x [1])
                pos = [v for k, v in items_]
                self._set = [k for k, v in items_]
                assert len (items_) == len (set (pos))
                assert pos [0] == 0
                assert pos [-1] == len (pos) - 1
            except (TypeError, AssertionError): # val is None
                self._set = sorted (self._origin.keys ())

        for idx, item in enumerate (self._set):
            self._indexes [item] = idx
        self._items = dict ([(v, k) for k, v in self._indexes.items ()])

    def __repr__ (self):
        return "<Label ({}): {}>".format (self.name, "[" + ", ".join ([str (each) for each in self._set]) + "]")

    def __len__ (self):
        return len (self._set)

    def __getitem__ (self, index):
        return self.class_name (index)

    def info (self, class_name):
        return self._origin [class_name]

    def put (self, class_name):
        self._origin.add (class_name)
        self.systemize ()

    def index (self, class_name):
        return self._indexes [class_name]

    def class_name (self, index):
        return self._items [index]
    item = class_name

    def class_names (self):
        return self._set
    items = class_names

    @property
    def classes (self):
        return self.class_names ()

    # encoding utils --------------------------------------------
    def top_k (self, arr, k = 1):
        items = []
        for idx in np.argsort (arr)[::-1][:k]:
            items.append (self._items [idx])
        return items

    def setval (self, items, type = np.float, prefix = None):
        arr = np.zeros (len (self._set)).astype (type)
        if not isinstance (items, (dict, list, tuple)):
            items = [items]
        if isinstance (items, dict):
            items = list (items.items ())

        for item, value in items:
            tid = self._indexes.get (item, -1)
            if tid == -1:
                raise KeyError ("{} Not Found".format (item))
            arr [self._indexes [item]] = value

        if prefix is not None:
            return np.concatenate ([prefix, arr])
        else:
            return arr

    def onehot (self, class_name, type = np.float, prefix = None):
        return self.setval ({class_name: 1.0}, type, prefix)
    one = onehot #lower version compatible

    def ones (self, class_names, type = np.float, prefix = None):
        return self.setval (dict ([(class_name, 1.0) for class_name in class_names]), type, prefix)

    def onehots (self, class_names, type = np.float, prefix = None):
        return np.array ([self.onehot (class_name, type, prefix) for class_name in class_names])


def onehots (labels, vals):
    if not isinstance (labels, list):
        labels = [labels]
    if not isinstance (vals, list):
        vals = [vals]
    y = []
    for idx, label in enumerate (labels):
        y = label.onehot (vals [idx], prefix = y)
    return y


if __name__ == "__main__":
    v1 = Label (["a", "b", "c", "d", "e"])
    v2 = Label (["a", "b", "c", "d", "e"])
    v3 = Label (["a", "b", "c", "d", "e"])
    f = Labels ([v1, v2, v3])
    print (f.encode ("c", {"a": 0.5}, ['d', 'e']))




