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
import pandas as pd
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile, Body
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *
import numpy as np


ROUTE = ""
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)
d = {}

@app.get("/get")
def xxxx(request: Request):
    print(request.query_params.get('a', 'xxxxxxx'))
    return {"Hello": d}

@app.post("/post")
def xxxx(request: Request, kwargs: dict):
    print(request.query_params)
    print(kwargs)
    return {"Hello": "World"}

@app.get("/gett")
def read_root():
    return {'a': np.array([1, 2, 3]).tolist()}


@app.get("/report")
def read_root():
    # return HTMLResponse(content=open("/Users/yuanjie/Desktop/notebook/your_report.html").read())
    return PlainTextResponse(content=open("/Users/yuanjie/Desktop/notebook/your_report.html").read())


@app.get("/reports")
def read_root():
    print(1)
    return FileResponse(path="/Users/yuanjie/Desktop/notebook/your_report.html", filename='downloadName')


@app.get("/view/{file}")
def read_root(file):
    return FileResponse(path=f"/Users/yuanjie/Desktop/notebook/{file}")


from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

# HTMLResponse(content="htmlString")
# HTMLResponse(content=open("/Users/yuanjie/Desktop/notebook/your_report.html").read())
# FileResponse(path="/Users/yuanjie/Desktop/notebook/your_report.html", filename=None) # 等价于上方
# FileResponse(path="./file.txt", filename='downloadName')
# https://fastapi.tiangolo.com/tutorial/background-tasks/

if __name__ == '__main__':

    d['a']=111111111
    import os
    import socket

    me = socket.gethostname() == 'yuanjie-Mac.local'

    uvicorn = "uvicorn" if me else "/opt/soft/python3/bin/uvicorn"

    main_file = __file__.split('/')[-1].split('.')[0]

    # --reload测试环境
    os.system(f"uvicorn {main_file}:app --reload --host 0.0.0.0 --port 9000")
