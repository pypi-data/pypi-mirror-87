import tensorflow as tf
if tf.__version__ [0] == '2':
    tf.compat.v1.disable_v2_behavior ()
from . import normalizer
from .label import Label
import os
import pickle
import shutil
from rs4 import pathtool, attrdict
import requests

def check_or_create (sess, graph):
    if sess is None:
        sess = tf.compat.v1.Session ()
    if graph is None:
        graph = sess.graph
    return sess, graph

def check_or_get (sess, graph):
    if sess is None:
        from tensorflow.compat.v1.keras.backend import get_session
        sess = get_session ()
    return check_or_create (sess, graph)

def add_classes_info (output_list, output_dict, labels = []):
    from tensorflow.python.ops import lookup_ops
    from tensorflow.python.framework import dtypes

    if not labels:
        return output_dict

    if isinstance (labels, Label):
        labels = [labels]

    if len (output_list) != len (labels):
        return output_dict # maybe concatenated output, skip

    for idx, lab in enumerate (labels):
        y = output_list [idx]
        name = y.name.split (":") [0].split ("/") [0]
        prefix = len (output_list) == 1 and '' or '{}_'.format (name)
        class_names = [str (cn) for cn in lab.class_names ()]
        output_dict ['{}scores'.format (prefix)], indices = tf.nn.top_k (y, min (len (class_names), 16))
        table = lookup_ops.index_to_string_table_from_tensor (
            vocabulary_list = tf.constant (class_names),
            default_value = "UNK",
            name = None
        )
        output_dict ['{}classes'.format (prefix)] = table.lookup (tf.cast(indices, dtype=dtypes.int64))
    return output_dict

def get_latest_version (path):
    versions = [ int (v) for v in os.listdir (path) if v.isdigit () ]
    if not versions:
        raise ValueError ('cannot find any model')
    return sorted (versions) [-1]

def get_next_version (path):
    try:
        return get_latest_version (path) + 1
    except ValueError:
        return 1

def convert_labels (asset_dir, labels):
    new_labels = [(label._origin, label.name) for label in labels]
    os.rename (os.path.join (asset_dir, 'labels'), os.path.join (asset_dir, 'labels.old2'))
    with open (os.path.join (asset_dir, "labels"), "wb") as f:
        pickle.dump (new_labels, f)

def load_labels (asset_dir):
    labels_path = os.path.join (asset_dir, "labels")
    if not os.path.isfile (labels_path):
        return
    with open (labels_path, "rb") as f:
        labels = pickle.load (f)
        if str (labels [0].__class__).find ('dnn.label') != -1:
            convert_labels (asset_dir, labels)
            return load_labels (asset_dir)
    return [Label (*label) for label in labels]

def save (model_dir, inputs, outputs = None, signature_name = 'predict', sess = None, graph = None, labels = [], assets_dir = None, verbose = True):
    def make_tensor_spec (tensors):
        return { tensor.name.split (":")[0].split ('/')[0]: tensor for tensor in tensors }

    if not isinstance (inputs, dict): # keras model
        model = inputs
        inputs = make_tensor_spec (model.inputs)
        outputs = make_tensor_spec (model.outputs)
        output_list = model.outputs
    else:
        output_list = list (outputs.values ())
    assert outputs, "output tensor required"

    sess, graph = check_or_get (sess, graph)
    with graph.as_default ():
        if assets_dir and not labels:
            labels = load_labels (assets_dir)

        if labels:
            outputs = add_classes_info (output_list, outputs, labels)

        inputs = dict ([(k, tf.compat.v1.saved_model.build_tensor_info (v)) for k, v in inputs.items ()])
        outputs = dict ([(k, tf.compat.v1.saved_model.build_tensor_info (v)) for k,v in outputs.items ()])
        prediction_signature = (
            tf.compat.v1.saved_model.signature_def_utils.build_signature_def (
                inputs = inputs,
                outputs = outputs,
                method_name = tf.saved_model.PREDICT_METHOD_NAME
            )
        )
        if not tf.compat.v1.saved_model.signature_def_utils.is_valid_signature (prediction_signature):
            raise ValueError("Error: prediction signature not valid!")

        signature_def_map = {
              tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY: prediction_signature,
              signature_name: prediction_signature,
        }
        builder = tf.compat.v1.saved_model.builder.SavedModelBuilder(model_dir)
        builder.add_meta_graph_and_variables (
            sess,
            [tf.saved_model.SERVING],
            signature_def_map = signature_def_map,
            main_op = tf.compat.v1.tables_initializer(),
            strip_default_attrs=True
        )
        builder.save ()

    pathtool.mkdir (os.path.join (model_dir, 'assets'))
    if assets_dir:
        verbose and print ("* Collecting assets")
        for asset in os.listdir (assets_dir):
            src = os.path.join (assets_dir, asset)
            if not os.path.isfile (src):
                continue
            verbose and print ('  - {} is copied'.format (asset))
            shutil.copyfile (src, os.path.join (model_dir, 'assets', asset))

    if verbose:
        print ("* Saved model")
        print ("  - Inputs")
        for k, v in inputs.items (): print ("    . {}: {}".format (k, v.name))
        print ("  - Outputs")
        for k, v in outputs.items (): print ("    . {}: {}".format (k, v.name))

    return inputs, outputs
convert = save


def deploy (model_dir, url, **data):
    with pathtool.flashfile ('model.zip') as zfile:
        pathtool.zipdir ('model.zip', model_dir)
        pathtool.uploadzip (url, 'model.zip', **data)
    resp = requests.get ('/'.join (url.split ("/")[:-2]))
    return resp.json ()


def load (model_dir, sess = None, graph = None):
    sess, graph = check_or_create (sess, graph)

    with graph.as_default ():
        meta = tf.compat.v1.saved_model.loader.load (
            sess,
            [tf.saved_model.SERVING],
            model_dir
        )

    input_map = {}
    outputs = {}
    activation = {}

    for signature_def_name, signature_def in meta.signature_def.items ():
        input_map [signature_def_name] = {}
        outputs [signature_def_name] = []
        activation [signature_def_name] = []

        for k, v in signature_def.inputs.items ():
            input_map [signature_def_name][k] = (v.name, sess.graph.get_tensor_by_name (v.name), v.dtype, [dim.size for dim in v.tensor_shape.dim])
        for k, v in signature_def.outputs.items ():
            outputs[signature_def_name].append ((k, v.name, sess.graph.get_tensor_by_name (v.name), v.dtype, [dim.size for dim in v.tensor_shape.dim]))
            activation [signature_def_name].append (v.name)

    return Interpreter (model_dir, meta, input_map, outputs, activation, sess, graph)

def load_latest (path):
    return load (os.path.join (path, str (get_latest_version (path))))

class Interpreter:
    def __init__ (self, model_dir, meta, input_map, outputs, activation, sess, graph):
        self.model_dir = model_dir
        self.meta = meta
        self.input_map = input_map
        self.outputs = outputs
        self.activation = activation
        self.sess = sess
        self.graph = graph
        self.asset_dir = os.path.join (self.model_dir, 'assets')
        if not os.path.exists (self.asset_dir):
            self.asset_dir = self.model_dir
        self.labels = load_labels (self.asset_dir)
        self.normalizer = normalizer.Normalizer.load (self.asset_dir)

    def normalize (self, x):
        if not self.normalizer:
            return x
        return self.normalizer.transform (x)

    def _run_output (self, feed_dict, signature_def_name = tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY):
        with self.graph.as_default (): # IMP: for thread-safe
            return self.sess.run (self.activation [signature_def_name], feed_dict = feed_dict)

    # publics ---------------------------------------------
    def tensor_names (self, filter = None):
        with self.graph.as_default ():
            current_graph = tf.compat.v1.get_default_graph()
            graph_def = current_graph.as_graph_def()
            for n in graph_def.node:
                if filter and n.name.find (filter) == -1:
                    continue
                print (n.name)

    def get_tensor_by_name (self, name):
        if len (name.split (":")) == 1:
            name = name + ":0"
        with self.graph.as_default ():
            current_graph = tf.compat.v1.get_default_graph ()
            return current_graph.get_tensor_by_name (name)

    def run (self, ops, feed_dict):
        if isinstance (ops, dict):
            # old version compat
            return self._run_output (ops, feed_dict)

        if not ops:
            return self.tensor_names ()
        ops_ = []
        for op in ops:
            if isinstance (op, str):
                ops_.append (self.get_tensor_by_name (op))
            else:
                ops_.append (op)

        feed_dict_ = {}
        for k, v in feed_dict.items ():
            if isinstance (k, str):
                feed_dict_ [self.get_tensor_by_name (k)] = v
            else:
                feed_dict_ [k] = v

        with self.graph.as_default (): # IMP: for thread-safe
            return self.sess.run (ops_, feed_dict = feed_dict_)

    def predict (self, inputs, signature_name = tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY, normalize = True):
        if not isinstance (inputs, dict):
            input_name = list (self.input_map [signature_name].keys ()) [0]
            inputs = {input_name: inputs}

        feed_dict = {}
        for k, v in inputs.items ():
            tensor_name, tensor, dtype, shape = self.input_map [signature_name][k]
            if normalize:
                v = self.normalize (v)
            feed_dict [tensor] = v
        results = self._run_output (feed_dict, signature_name)
        return attrdict.AttrDict (
            { output [0]: results [i] for i, output in enumerate (self.outputs [signature_name]) }
        )

    def ftest (self, inputs, signature_name = tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY):
        # IMP: no normalization
        return self.predict (inputs, signature_name , False)

