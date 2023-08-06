#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : helloworld
# @Time         : 2020-01-09 10:38
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
from typing import Optional
from fastapi import FastAPI, Form, Depends
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import *

app = FastAPI(debug=True)


# app = FastAPI(
#     openapi_url="/poetry/openapi.json",
#     docs_url="/poetry/docs",
#     redoc_url="/poetry/redoc",
#     swagger_ui_oauth2_redirect_url="/poetry/docs/oauth2-redirect"
# )


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


async def parse_my_form(request: Request) -> dict:
    form_data = await request.form()
    return dict(form_data)


@app.post("/my-form-endpoint")
def my_endpoint(form_data: dict = Depends(parse_my_form)):

    print(form_data)
    return "post succeed"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def create_item(item_id: int,
                      item: Item,
                      q: str = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# @app.put("/data/{data}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


if __name__ == '__main__':
    import os
    import socket

    me = socket.gethostname() == 'yuanjie-Mac.local'

    uvicorn = "uvicorn" if me else "/opt/soft/python3/bin/uvicorn"

    main_file = __file__.split('/')[-1].split('.')[0]

    os.system(f"uvicorn {main_file}:app --reload --host 0.0.0.0")

    # os.system(f"gunicorn -c gun.py -w 1 -k uvicorn.workers.UvicornWorker {main_file}:app")
