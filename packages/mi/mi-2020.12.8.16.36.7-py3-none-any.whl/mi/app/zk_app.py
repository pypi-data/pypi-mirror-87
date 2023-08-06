#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : zk_app
# @Time         : 2020-03-11 14:39
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : app
# @Time         : 2020-03-11 13:54
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : http://zkview.d.xiaomi.net/clusters/tjwqstaging/nodes?path=%2Fmipush%2Fhive&isAdmin=false


import time
import pandas as pd
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *

from kazoo.client import KazooClient
import yaml
from traceback import format_exc  # https://www.cnblogs.com/klchang/p/4635040.html
from collections import OrderedDict

ROUTE = "/zk"
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)


@app.get("/zk/{zk_url}/{zk_path}")
async def zk_cfg(zk_url, zk_path):
    dic = OrderedDict()

    zk_path = zk_path.replace('.', '/')

    zk = KazooClient(hosts=zk_url)
    zk.start()

    try:
        data, stat = zk.get(zk_path)
        cfg = yaml.safe_load(data)

        dic[zk_path] = cfg
        dic['children'] = zk.get_children(zk_path)

    except Exception  as e:
        dic['error'] = format_exc()

    return dic


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, reload=True, debug=True)
