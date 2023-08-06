#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : base_app
# @Time         : 2020-03-21 15:40
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import time
import uvicorn
import pandas as pd

from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *

from collections import OrderedDict
from traceback import format_exc  # https://www.cnblogs.com/klchang/p/4635040.html

app = FastAPI()


class App(object):

    def __init__(self, verbose=True):
        self.app = FastAPI()
        self.verbose = verbose

    def run(self, app=None, host="0.0.0.0", port=8000, workers=1, access_log=True, debug=True, reload=True, **kwargs):
        """

        :param app:   app字符串可开启热更新
        :param host:
        :param port:
        :param workers:
        :param access_log:
        :param debug:
        :param reload:
        :param kwargs:
        :return:
        """
        uvicorn.run(
            app if app else self.app,
            host=host, port=port, workers=workers, access_log=access_log, debug=debug, reload=reload
        )
