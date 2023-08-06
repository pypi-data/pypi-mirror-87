__version__ = "0.6.5"

from .layers import layers
import glob, os, shutil

def clear_session ():
    import tensorflow as tf
    tf.keras.backend.clear_session ()

def setup_gpus (memory_limit = 'growth', gpu_devices = []):
    # memory_limit unit is MB
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        if gpu_devices:
            visibles = [gpus [i] for i in gpu_devices]
        else:
            visibles = gpus
        for gpu in visibles:
            if memory_limit == 'growth':
                tf.config.experimental.set_memory_growth (gpu, True)
            else:
                tf.config.set_logical_device_configuration (gpu, [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=memory_limit)])
        tf.config.set_visible_devices(visibles, 'GPU')

def processing (train_func, *args):
    from multiprocessing import Pool
    with Pool(1) as p:
        return p.apply (train_func, args)
subprocess = processing

def get_last_checkpoint (train_dir):
    cks = glob.glob (os.path.join (train_dir, 'checkpoint', '*.ckpt.index'))
    if not cks:
        raise IOError ('no checkpoint found')
    best = sorted (cks) [-1]
    return best [:-6]

def reset_dir (train_dir):
    os.path.isdir (train_dir) and shutil.rmtree (train_dir)

def get_assets_dir (train_dir):
    return os.path.join (train_dir, 'assets')

def inspect_train_dir (train_dir, restore = True):
    if not restore:
        reset_dir (train_dir)

    try:
        last = get_last_checkpoint (train_dir)
    except IOError:
        return 0, None
    return int (os.path.basename (last).split ('.')[0]), get_last_checkpoint (train_dir)

