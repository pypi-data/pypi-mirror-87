#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : nni_app
# @Time         : 2020/9/3 1:24 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import os
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

# experiment

ROUTE = "/nni"
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)


@app.get("/nni/download")
def hdfs():
    cmd = f"""
    /usr/bin/kinit -k -t /h_browser.keytab h_browser@XIAOMI.HADOOP
    rm -rf ~/nni/experiments/*
    /infra-client/bin/hdfs --cluster zjyprc-hadoop dfs -get /user/h_data_platform/platform/browser/logs/data/nni/* ~/nni/experiments
    nnictl create --config config.yml
    """
    os.system(cmd)
    files = os.popen('ls ~/nni/experiments').read().strip().split()
    return {'files': files}


@app.get("/nni/experiment/{experiment_id}")
def read_root(experiment_id):
    cmd = f"""
    
    nnictl stop --all
    sleep 3
    nnictl resume {experiment_id}
    """
    os.system(cmd)

    return RedirectResponse("0.0.0.0:8080")


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, reload=True, debug=True)
