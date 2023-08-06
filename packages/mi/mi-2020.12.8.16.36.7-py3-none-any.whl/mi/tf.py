
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Java.
# @File         : gen_pb_model.py
# @Time         : 2020-03-13 18:03
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : IntelliJ IDEA
# @Description  :


# from wandb import magic
import numpy as np
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from tensorflow.keras import optimizers
import tensorflow
import tensorflow as tf
from tensorflow import keras

print(tf.__version__)
# import tensorflow.keras.backend as K

from sklearn.datasets import make_classification

X, y = make_classification(100000, 16)

input_shape = X.shape[1:]
model_input = Input(input_shape)
x = Dense(128)(model_input)
x = Dense(64)(x)
model_out = Dense(1, activation='sigmoid')(x)

model = Model(inputs=model_input, outputs=model_out)
model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['acc', tf.keras.metrics.AUC()])

model.fit(X, y, batch_size=128, epochs=1)
model.save('keras.h5')
# saved_model_cli show --dir tfmodel --all

model.save('tfmodel', save_format="tf")
# tf.saved_model.save(model, "./pb")

if __name__ == '__main__':
    import os

    os.system("saved_model_cli show --dir tfmodel --all")
