#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : mp3
# @Time         : 2020/9/1 10:42 上午
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
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse, StreamingResponse
from starlette.status import *

ROUTE = "/mongo"
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)


@app.get("/mp3/{file}")
def read_root(file):
    path = f"/Users/yuanjie/Desktop/{file}"

    # file_like = open(path, mode="rb")
    # return StreamingResponse(file_like, media_type="video/mp4")

    return FileResponse(path, media_type="video/mp4")


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(
        app=f"{main_file}:app", host='0.0.0.0',
        port=8000, workers=1,
        reload=True,
        debug=True
    )
