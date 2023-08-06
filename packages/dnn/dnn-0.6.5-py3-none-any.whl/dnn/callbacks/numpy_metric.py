from tensorflow.keras.callbacks import Callback
from rs4.termcolor import tc, stty_size
from tensorflow.python.keras import backend as K
from . import base
import numpy as np
from sklearn.metrics import f1_score


# numpy metrics ---------------------------------
def F1 (mode = 'weighted'):
    def f1_weighted (y_true, y_pred, logs = None, name = None):
        logs = logs or {}
        labels = np.argmax (y_true, axis = 1)
        logs ['val{}_f1'.format (name and ('_' + name) or '')] = f1_score (labels, np.argmax (y_pred, axis = 1), average = mode)
        return '' # return displayable message
    return f1_weighted


class NumpyMetricCallback (base.ValiadtionSet, Callback):
    def __init__(self, func, validation_data):
        Callback.__init__(self)
        base.ValiadtionSet.__init__ (self, validation_data)
        self.func = F1 ('weighted') if func == 'f1' else func
        self.info = None

    def get_info (self):
        return self.info

    def on_epoch_end (self, epoch, logs):
        logs = logs or {}
        self.make_predictions ()
        if isinstance (self.ys, tuple):
            self.info = []
            for idx in range (len (self.ys)):
                name = self.model.outputs [idx].name.split ("/")[0]
                self.info.append (self.func (self.ys [idx], self.logits [idx], logs, name))
            self.info = '\n'.join (self.info)
        else:
            self.info = self.func (self.ys, self.logits, logs)

