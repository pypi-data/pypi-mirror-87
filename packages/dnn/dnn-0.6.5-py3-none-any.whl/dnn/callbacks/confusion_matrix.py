from tensorflow.keras.callbacks import Callback
import numpy as np
from rs4.termcolor import tc, stty_size
from . import base
import os
from sklearn.metrics import f1_score, confusion_matrix

def plot (cm, target_names, title='Confusion matrix', cmap = None, normalize = False, metrics = None):
    import matplotlib.pyplot as plt
    import itertools

    wi = max (len (target_names), 5)
    he = wi - 2
    figsize = (wi, he)

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=figsize)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    xlabel = 'Predicted label'
    if metrics:
        xlabel = xlabel + '\n' + (", ".join (['{}={:.4}'.format (k, v) for k, v in metrics.items ()]))
    plt.xlabel(xlabel)
    plt.show()


def plot_with_logits (y_true, y_pred, target_names):
    metrics = dict (
        acc = f1_score (y_true, y_pred, average = 'micro'),
        f1 = f1_score (y_true, y_pred, average = 'weighted')
    )
    cm = confusion_matrix (y_true, y_pred)
    plot (cm, target_names, metrics = metrics)


class ConfusionMatrixCallback (base.Display, base.ValiadtionSet, Callback):
    def __init__(self, labels, validation_data, display_list = None):
        Callback.__init__(self)
        base.ValiadtionSet.__init__ (self, validation_data)
        if not isinstance (labels, (list, tuple)):
            labels = [labels]
        self.labels = labels
        self.display_list = display_list
        self.buffer = []
        self.jpy = os.getenv ("JPY_PARENT_PID")

    def _confusion_matrix (self, label_index = 0, indent = 4, show_label = True):
        cur_label = self.labels [label_index]
        if isinstance (self.ys, tuple):
            ys = self.ys [label_index]
            logits = self.logits [label_index]
        else:
            ys = self.ys
            logits = self.logits

        y_true, y_pred = np.argmax (ys, 1), np.argmax (logits, 1)
        mat_ = confusion_matrix (y_true, y_pred)
        metrics = dict (
            acc = f1_score (y_true, y_pred, average = 'micro'),
            f1 = f1_score (y_true, y_pred, average = 'weighted')
        )

        # if self.jpy:
        #     plot (mat_, cur_label.class_names (), cur_label.name, metrics = metrics)
        #     return

        # text plotting
        mat = str (mat_) [1:-1]
        try:
            self.buffer.append ("\nconfusion matrix{}\n".format (tc.info (cur_label.name and (" of " + cur_label.name) or "")))
        except IndexError:
            return

        labels = []
        if show_label:
            first_row_length = len (mat.split ("\n", 1) [0]) - 2
            label_width = (first_row_length - 1) // mat_.shape [-1]
            labels = [str (each) [:label_width].rjust (label_width) for each in cur_label.class_names ()]
            self.buffer.append (tc.fail ((" " * (indent + label_width + 1)) + " ".join (labels)))

        lines = []
        for idx, line in enumerate (mat.split ("\n")):
            if idx > 0:
                line = line [1:]
            line = line [1:-1]
            if labels:
                line = tc.info (labels [idx]) + " " + line
            if indent:
                line = (" " * indent) + line
            self.buffer.append (line)
        self.buffer.append ((" " * indent) + 'metrics: ' + (", ".join (['{}={:.4}'.format (k, v) for k, v in metrics.items ()])))

    def on_epoch_begin(self, epoch, logs):
        self.buffer = []

    def on_epoch_end(self, epoch, logs):
        self.make_predictions ()
        for label_index, label in enumerate (self.labels):
            if self.display_list and label.name not in self.display_list:
                continue
            self._confusion_matrix (label_index)
        print ('\n' + '\n'.join (self.buffer))
        self.draw_line ()

    def get_info (self):
        return self.buffer
