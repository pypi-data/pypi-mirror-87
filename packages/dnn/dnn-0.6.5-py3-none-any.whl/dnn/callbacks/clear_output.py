from tensorflow.keras.callbacks import Callback
import os

class ClearOutput (Callback):
    def on_epoch_end (self, epoch, logs={}):
        if os.getenv ("JPY_PARENT_PID"):
            from IPython.display import clear_output
            clear_output (wait = True)
