#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : xindao_ann
# @Time         : 2020/11/10 5:40 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : mi-run - task xindao_ann --python ~/anaconda3/bin/python

import os
import time
import datetime
import requests

from milvus import DataType

from tql.pipe import *

os.environ['LOG_PATH'] = f'/home/work/yuanjie/{Path(__file__).name}.log'

from tql.utils.logger_utils import logger
from mi.db import Mongo, ANN, Hive

conn = Hive.Hive('/home/work/keytab/h_browser.keytab').conn

mongo = Mongo()
xindao_ann = mongo.db.xindao_ann


def get_vector(titles=["小米", "大米"], sleep=0.3):
    time.sleep(sleep)
    url = 'http://simbert-vector-cl33103.c3.ingress.mice.cc.d.xiaomi.net/simbert'
    json = {"texts": titles}
    r = requests.post(url, json=json)
    return r.json()['vectors']


category_map = {k: xindao_ann.find_one({'category': k})['category_'] for k in xindao_ann.distinct('category')}

ann = ANN('10.119.33.90')

dfs = []
for i in [-1, -2, -3]:
    date_1 = str(get_date(i))[:10].replace('-', '')
    sql = f"""
    select id, xindaoid, title, category[0] category
    from feeds.content_databus_xindao_batch_idx
    where date = {date_1}
    and xindaoid is not null
    and category[0] is not null 
    """
    dfs.append(pd.read_sql(sql, conn))

df_xd = pd.concat(dfs).drop_duplicates(ignore_index=True)

df_xd['xindaoid'] = df_xd['xindaoid'].astype(int)
is_in_mongo = df_xd['xindaoid'].progress_map(lambda x: True if xindao_ann.find_one({'xindaoid': x}) else False)
df_xd = df_xd[~is_in_mongo]

if len(df_xd) > 0:
    logger.info(f"新增内容{len(df_xd)}条，更新ANN服务")

    vecs = (
            df_xd['title'].tolist() | xgroup_by_step(10) |
            xThreadPoolExecutor(get_vector, 10) | xlist
    )

    df_xd['vector'] = np.row_stack(vecs).tolist()

    for category in df_xd['category']:
        category_map[category] = category_map.get(category, max(category_map.values()) + 1)

    df_xd['category_'] = df_xd['category'].map(category_map)

    # mongo insert
    xindao_ann.insert_many(df_xd.to_dict('r'), False)

    # ann instert
    collection_name = 'demo'
    ids = df_xd.xindaoid.tolist()
    hybrid_entities = [
        {"name": "category_", "values": df_xd.category_.tolist(), "type": DataType.INT32},
        {"name": "embedding", "values": df_xd.vector.tolist(), "type": DataType.FLOAT_VECTOR},
    ]

    _ = ann.client.insert(collection_name, hybrid_entities, ids)

else:
    logger.info("无新增内容，无需更新ANN服务")
