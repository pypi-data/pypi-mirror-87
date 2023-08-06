#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : simbert
# @Time         : 2020-04-09 14:08
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import numpy as np
from collections import Counter
from bert4keras.backend import keras, K
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding, AutoRegressiveDecoder
from bert4keras.snippets import uniout
from keras.layers import *


def normalize(x):
    return x / np.linalg.norm(x, 2, axis=len(x.shape) > 1, keepdims=True)


# bert配置
config_path = './chinese_simbert_L-12_H-768_A-12/bert_config.json'
checkpoint_path = './chinese_simbert_L-12_H-768_A-12/bert_model.ckpt'
dict_path = './chinese_simbert_L-12_H-768_A-12/vocab.txt'

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)

# 建立加载模型
bert = build_transformer_model(
    config_path,
    checkpoint_path,
    with_pool='linear',
    application='unilm',
    return_keras_model=True  # True: bert.predict([np.array([token_ids]), np.array([segment_ids])])
)

bert_ = build_transformer_model(
    config_path,
    checkpoint_path,
    with_pool='linear',
    application='unilm',
    return_keras_model=False  # True: bert.predict([np.array([token_ids]), np.array([segment_ids])])
)

encoder = keras.models.Model(bert_.model.inputs, bert_.model.outputs[0])


# seq2seq = keras.models.Model(bert.model.inputs, bert.model.outputs[1])

def sentence_encode(texts: list, batch_size=64):
    X, S = [], []
    for t in texts:
        x, s = tokenizer.encode(t)
        X.append(x)
        S.append(s)
    X = sequence_padding(X)
    S = sequence_padding(S)

    vec = encoder.predict([X, S], batch_size)
    return normalize(vec).tolist()
