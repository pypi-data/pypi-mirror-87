#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : ocr_app
# @Time         : 2020/9/9 10:49 上午
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

ROUTE = "/ocr"
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)

import base64
import requests
import pytesseract
from PIL import Image
from traceback import format_exc  # https://www.cnblogs.com/klchang/p/4635040.html
from mi.sdk import BaiduApi
from tempfile import TemporaryFile

baidu_api = BaiduApi()


@app.post("/ocr/{biz}")
async def ocr(request: Request, kwargs: dict, biz):
    image = kwargs['image']

    options = kwargs.get('options')
    lang = kwargs.get('lang', 'chi_sim')

    try:

        if biz == 'baidu':
            if len(image) < 1024:
                image = requests.get(image).content
                baidu_api

            else:
                image = base64.b64decode(image)
            return baidu_api.ocr_basic_general(image, options)

        elif biz == 'google':
            if len(image) < 1024:
                image = requests.get(image, stream=True).raw
                image = Image.open(image)

                return pytesseract.image_to_string(image, lang=lang)
            else:
                image = base64.b64decode(image)

                with TemporaryFile() as f:
                    # Read/write to the file
                    f.write(image)
                    # Seek back to beginning and read the data
                    f.seek(0)
                    # data = f.read()
                    image = Image.open(f)

                    return pytesseract.image_to_string(image, lang=lang)

    except Exception as e:
        return {'error': format_exc()}


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, debug=True, reload=True)
