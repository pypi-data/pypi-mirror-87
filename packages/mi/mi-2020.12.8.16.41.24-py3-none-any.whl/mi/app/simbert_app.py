#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : simbert
# @Time         : 2020-04-08 20:22
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import re
import time
from collections import OrderedDict
from datetime import datetime
import pandas as pd
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *
from traceback import format_exc  # https://www.cnblogs.com/klchang/p/4635040.html

ROUTE = "/bert"
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)

#################################################################################
import numpy as np
import keras
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding
from loguru import logger


# import os
# os.environ['TF_KERAS'] = '1'
# cli
import argparse

parser = argparse.ArgumentParser(description='BERT APP')
parser.add_argument('-d', '--bertDir', type=str, help='bert dir')
args = parser.parse_args()
BERT_DIR = args.bertDir
if BERT_DIR:
    logger.info(f"BERT_DIR: {BERT_DIR}")

config_path = f'{BERT_DIR}/bert_config.json'
checkpoint_path = f'{BERT_DIR}/bert_model.ckpt'
dict_path = f'{BERT_DIR}/vocab.txt'

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)

# 建立加载模型
bert = build_transformer_model(
    config_path,
    checkpoint_path,
    with_pool='linear',
    application='unilm',
    return_keras_model=False  # True: bert.predict([np.array([token_ids]), np.array([segment_ids])])
)

encoder = keras.models.Model(bert.model.inputs, bert.model.outputs[0])


# seq2seq = keras.models.Model(bert.model.inputs, bert.model.outputs[1])

def normalize(x):
    return x / np.linalg.norm(x, 2, axis=len(x.shape) > 1, keepdims=True)


def sentence_encode(texts: list, batch_size=128):
    X, S = [], []
    for t in texts:
        x, s = tokenizer.encode(t)
        X.append(x)
        S.append(s)
    X = sequence_padding(X)
    S = sequence_padding(S)

    vec = encoder.predict([X, S], batch_size)
    return normalize(vec).tolist()


@app.get("/bert/simbert")
def simbert(request: Request):
    dic = OrderedDict()
    date = datetime.now()
    dic['date'] = date.__str__()[:10]
    dic['datetime'] = date.__str__()
    dic['timestamp'] = date.timestamp()

    texts = request.query_params.get("texts", [])
    if texts:
        dic['vectors'] = sentence_encode(texts)
    else:
        dic['vectors'] = [[]]

    return dic


@app.post("/bert/simbert")
def simbert(kwargs: dict):
    dic = OrderedDict()
    date = datetime.now()
    dic['date'] = date.__str__()[:10]
    dic['datetime'] = date.__str__()
    dic['timestamp'] = date.timestamp()

    texts = kwargs.get("texts", [])
    if texts:
        dic['vectors'] = sentence_encode(texts)
    else:
        dic['vectors'] = [[]]

    return dic


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, debug=True)
