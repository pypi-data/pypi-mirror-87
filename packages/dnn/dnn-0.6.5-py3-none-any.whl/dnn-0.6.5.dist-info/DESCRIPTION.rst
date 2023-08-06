
History
============

- 0.6 (2020.6.29)

  - add dnn.setup_gpus (memory_limit = 'growth', gpu_devices = [])
  - add dnn.layers for proxying tf.keras.layers
  - add dnn.callbacks for tf.keras
  - minor fixes for tfserver_
  - update for tensorflow 2.x

- 0.4 (2020.6.24)

  - integrate tfserver into dnn.tfserver
  - data processing utils were moved to rs4.mldp

- 0.3:

  - remove trainale ()
  - add set_learning_rate ()
  - add argument to set_train_dir () for saving chcekpoit
  - make compatible with tf 1.12.0

- 0.2

  - add tensorflow lite conversion and interpreting

- 0.1: project initialized


.. _rs4: https://pypi.org/project/rs4/
.. _tfserver: https://pypi.org/project/tfserver/


