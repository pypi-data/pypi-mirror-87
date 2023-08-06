#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : nlp_app
# @Time         : 2020/6/8 11:27 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import os
from collections import OrderedDict

import numpy as np

import jieba.analyse  as ja
from gensim.models.fasttext import load_facebook_model

_norm = lambda x, ord=1: x / np.linalg.norm(x, ord, axis=len(x.shape) > 1, keepdims=True)

import time
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

ROUTE = "/nlp"
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)

cmd = f"wget http://cdn.cnbj1.fds.api.mi-img.com/browser-algo-nanjing/data/wv/skipgram.title -O skipgram.title"
os.popen(cmd).read()

wv = load_facebook_model("./skipgram.title").wv


def topk_words_vec(q):
    vec = np.zeros(200)
    ws = ja.tfidf(q, topK=8)

    if ws:
        for w in ws:
            vec += wv[w] / len(ws)
        vec = _norm(vec)
    return " ".join(map(str, vec.tolist()))


@app.post("/nlp/wv/fasttext")
async def report(kwargs: dict):
    dic = OrderedDict()

    id2sent = kwargs['id2word']

    data = {i: topk_words_vec(sent) for i, sent in id2sent.items()}
    dic['data'] = data

    return dic


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, debug=True)
