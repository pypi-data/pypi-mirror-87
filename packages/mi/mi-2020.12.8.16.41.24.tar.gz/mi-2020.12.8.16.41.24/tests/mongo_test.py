#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : test
# @Time         : 2020-03-21 17:15
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
""":argument
zk配置接口 http://0.0.0.0:8000/app/cfg
email post 接口: http://0.0.0.0:8000/app/{biz}  {'msg': 'xx'}
mongo查询get接口:
    http://0.0.0.0:8000/app/mongo/test/count_documents?filter={}
    http://tql.algo.browser.miui.srv/app/mongo/word2vec.tag2vec/find?filter={%27w%27:%20%27%E4%B8%AD%E5%9B%BD%27}

mongo插数post接口 http://0.0.0.0:8000/app/mongo/post/test?jobid=xxxxxxxxxx&jobtype=hive
数据工厂http回调post form接口 http://0.0.0.0:8000/app/mongo/form/test?jobid=xxxxxxxxxx&jobtype=hive


"""

import uvicorn
from mi.app import mongo

app = mongo.app
uvicorn.run(app, host='0.0.0.0', port=8000, workers=1, debug=True)
