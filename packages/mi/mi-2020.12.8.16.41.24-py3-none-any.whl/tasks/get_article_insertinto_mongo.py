#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : get_article
# @Time         : 2020/12/8 4:29 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.zk_utils import get_zk_config
from meutils.date_utils import date_difference
from mi.db.Hive import Hive
from mi.db import Mongo

mongo_cache_url = get_zk_config()['mongo_cache_url']

hive = Hive('/home/work/keytab/h_browser.keytab')
mongo = Mongo()
ac = mongo.db.articleinfo

date = date_difference('%Y%m%d', days=1)
sql = f"""
select data as id, date
from browser.date_biz_partition
where biz='nh_test' and date={date} 
"""
df = pd.read_sql(sql, hive.conn)


def request(docid='0003899b202871b7fd3dab15f2f9549a', method='get'):
    url = f"{mongo_cache_url}/ac?id={docid}"
    r = requests.request('get', url)
    r.encoding = r.apparent_encoding
    return r.json()['result']


def get_and_insert_ac(docid='yidian_0R18y0XA'):
    # 多请求
    # ac.replace_one({'id': 'yidian_0R18y0XA'}, {'$set': {'id': 'id'}}) # 替换原始值{**d1, **d2}
    if ac.find_one({'id': docid}):
        logger.info(f'dup key: {docid}')
    else:
        doc = {'id': docid, 'ac': str(request(docid))}
        _ = ac.insert(doc, continue_on_error=False)


tqdm(df.id) | xThreadPoolExecutor(get_and_insert_ac, 20)
