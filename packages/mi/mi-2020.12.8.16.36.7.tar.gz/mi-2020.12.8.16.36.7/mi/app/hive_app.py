#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : EmailApp
# @Time         : 2020-03-06 09:41
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

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

ROUTE = ""
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)


@app.get("/demo}")
async def report():
    pass

@app.post("/report/{job_type}")
async def report(request: Request, kwargs: dict, job_type):
    """https://www.jianshu.com/p/5b922809f5ef
    一般对于Request Body不会通过get提交，对于get提交的参数一般称为是查询参数。
    所以，如果是通过POTS,PUT等方式提交的参数信息，我们一般是放到Request Body来提交到我们的后端。
    """
    # post: kwargs: dict
    # print(dict(request))
    # print(request.path_params) # {'job_type': 'hive'}
    dic = dict(request.query_params)
    dic['date'] = datetime.now().__str__()
    dic['post_data'] = kwargs
    dic['form_data'] = dict(await request.form())

    print(dic)
    if job_type == 'hive':
        return "post succeed"

    elif job_type == 'spark':
        pass


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, debug=True)
