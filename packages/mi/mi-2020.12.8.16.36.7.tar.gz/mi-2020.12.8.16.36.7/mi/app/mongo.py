#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : watchDog
# @Time         : 2020-03-06 09:41
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
""":arg
/app/mongo/{collection}/{attribute}：insert delete update find count(默认)
querypath+postdata+formdata+date
querypath：
可增加是否发邮件参数(需要润色html或者web或者sreamlit)
可增加一些额外信息：jobid jobtype
增加collection name判断
返回：可选操作前后的文档数、新增的doc、更新后的doc、耗时信息、抛错信息

"""
import re
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
from collections import OrderedDict
from traceback import format_exc  # https://www.cnblogs.com/klchang/p/4635040.html
from collections import Iterable, Iterator
from bson import json_util

from ..db import Mongo, Mysql
from ..utils import email_data_process, send_email, df2html
from ..utils.zk_client import Config

mongo = Mongo()
mysql = Mysql()

ROUTE = "/app"
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)


@app.get(f"{ROUTE}/cfg")
async def report():
    return {k: v for k, v in Config.__dict__.items() if not k.startswith('__')}


@app.get("/app/mongo/{collection}/{attribute}")
async def report(request: Request, collection, attribute):
    """查询"""
    dic = OrderedDict()
    date = datetime.now()
    dic['date'] = date.__str__()[:10]
    dic['datetime'] = date.__str__()
    dic['timestamp'] = date.timestamp()

    dic['form_data'] = dict(await request.form())
    dic['querypath'] = dict(request.query_params)

    try:
        params = dic['querypath']
        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))

        if 'filter' in params:
            params['filter'] = eval(params['filter'])

        _ = mongo.db[collection].__getattribute__(attribute)(**params)
        # _ = list(_) if isinstance(_, Iterator) else _
        dic[f"{collection}.{attribute}"] = eval(json_util.dumps(_))
        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))

    except Exception  as e:
        dic['error'] = format_exc()

    return dic


@app.post("/app/email/{biz}/{jobid}")
async def report(request: Request, kwargs: dict, biz, jobid):
    """
    发邮件
    /app/email/{biz}/{jobid}
    """
    # print(dict(request))
    dic = OrderedDict()
    date = datetime.now()
    dic['date'] = date.__str__()[:10]
    dic['datetime'] = date.__str__()
    dic['timestamp'] = date.timestamp()

    dic['post_data'] = kwargs
    dic['form_data'] = dict(await request.form())  # form_data post_data无法共存?
    dic['querypath'] = dict(request.query_params)

    try:
        # biz config
        email_config = Config.zk_cfg.get('email', {}).get(biz, 'biz').copy()  # zk里配置biz信息
        email_config['subject'] = biz
        email_config['jobid'] = jobid
        email_config['msg'] = kwargs.get('msg', '请求参数缺失msg')

        if 'msg_fn' in email_config:
            # df2html.df2html(email_config['subject'], dic['date'], df.to_html())
            email_config['msg_fn'] = eval(email_config['msg_fn'])
        send_email.send_email(**email_config)

        dic['status'] = 'succeed'

    except Exception  as e:
        dic['error'] = format_exc()

    return dic


@app.post("/app/mongo/form/{collection}/{biz}/{jobid}")
async def report(request: Request, collection, biz, jobid):
    """
    数据工厂http接口：插数、发邮件
    /app/mongo/form/{collection}/{biz}/{jobid}
    """
    # print(dict(request))
    dic = OrderedDict()
    date = datetime.now()
    dic['date'] = date.__str__()[:10]
    dic['datetime'] = date.__str__()
    dic['timestamp'] = date.timestamp()

    dic['form_data'] = dict(await request.form())  # form_data post_data无法共存?
    dic['querypath'] = dict(request.query_params)

    try:
        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))
        mongo.db[collection].insert_one(dic.copy())  # 存储的时候会被改变
        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))

        data = dic.get('form_data', {}).get('data', '')
        df = email_data_process.hive(str(data))

        # biz config
        email_config = Config.zk_cfg.get('email', {}).get(biz, "biz").copy()  # 会变
        email_config['subject'] = email_config.get("subject", " ") + biz
        email_config['jobid'] = jobid
        email_config['msg'] = df2html.df2html(email_config['subject'], dic['date'], df.to_html())
        if 'msg_fn' in email_config:
            email_config['msg_fn'] = eval(email_config['msg_fn'])
        send_email.send_email(**email_config)  # TODO美化：add 责任人
        dic['status'] = 'succeed'

    except Exception  as e:
        dic['error'] = format_exc()

    return dic


@app.post("/app/mongo/post/{collection}")
async def report(request: Request, kwargs: dict, collection):
    """插数、发邮件
    jobtype参数触发邮件服务(需要润色html或者web或者sreamlit)
    TODO: 耗时信息
    """
    # print(dict(request))
    # print(request.path_params) # {'jobtype': 'hive'}
    dic = OrderedDict()
    date = datetime.now()
    dic['date'] = date.__str__()[:10]
    dic['datetime'] = date.__str__()
    dic['timestamp'] = date.timestamp()

    dic['post_data'] = kwargs
    dic['form_data'] = dict(await request.form())  # form_data post_data无法共存?
    dic['querypath'] = dict(request.query_params)

    try:
        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))
        mongo.db[collection].insert_one(dic.copy())  # 存储的时候会被改变
        dic.setdefault("count_documents", []).append(mongo.db[collection].count_documents({}))

        # TODO：要不要舍弃
        params = dic['querypath']
        # job_type in （'hive', 'spark') 触发邮件服务
        if params.get('jobtype') == 'spark':
            dic['status'] = 'succeed'
            data = dic.get('post_data', {}).get('data', '')  # spark post请求 {'post_data': {'data': '...'}}
            df = email_data_process.spark(str(data))
            send_email.send_email(msg=df.to_html())

    except Exception  as e:
        dic['error'] = format_exc()

    return dic


@app.post("/app/mysql/post")
async def data(request: Request, kwargs: dict):
    dic = OrderedDict()
    sql = kwargs.get('sql', 'select * from push_daily_news')
    if 'limit' not in sql:
        sql = sql + ' limit 10000'

    try:
        df = pd.read_sql(sql, mysql.conn)
        dic['data'] = df.to_dict('record')

    except Exception  as e:
        dic['error'] = format_exc()

    return dic


# # 无嵌套
# @app.post("/app/mongo/post/{collection}")
# async def report(request: Request, kwargs: dict, collection):
#     """插数、发邮件
#     jobtype参数触发邮件服务(需要润色html或者web或者sreamlit)
#     TODO: 耗时信息
#     """
#     # print(dict(request))
#     # print(request.path_params) # {'jobtype': 'hive'}
#     dic = OrderedDict()
#     date = datetime.now()
#     dic['date'] = date.__str__()[:10]
#     dic['datetime'] = date.__str__()
#     dic['timestamp'] = date.timestamp()
#
#     dic['post_data'] = kwargs
#     dic['form_data'] = dict(await request.form())  # form_data post_data无法共存?
#     dic['querypath'] = dict(request.query_params)


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, debug=True, reload=True)
