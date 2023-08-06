from tensorflow.keras.callbacks import Callback
import matplotlib.pyplot as plt
import os

class PlotProgress (Callback):
    def __init__(self, entity = 'loss'):
        self.entity = entity
        self.jpy = os.getenv ("JPY_PARENT_PID")

    def on_train_begin (self, logs={}):
        if not self.jpy:
            return
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        self.fig = plt.figure ()
        self.logs = []

    def on_epoch_end (self, epoch, logs={}):
        if not self.jpy:
            return
        self.logs.append (logs)
        self.x.append (self.i)
        self.losses.append (logs.get('{}'.format (self.entity)))
        self.val_losses.append (logs.get('val_{}'.format (self.entity)))
        self.i += 1

        plt.plot (self.x, self.losses, label="{}".format (self.entity))
        plt.plot (self.x, self.val_losses, label="val_{}".format (self.entity))
        plt.legend ()
        plt.show ()