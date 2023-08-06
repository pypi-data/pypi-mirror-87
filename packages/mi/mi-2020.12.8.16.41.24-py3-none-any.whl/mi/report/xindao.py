#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : xindao
# @Time         : 2020/9/1 2:57 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from tqdm.auto import tqdm

tqdm.pandas()

from tql.data_plot import WordCloud
from tql.pipe import *
from pathlib import Path
import cufflinks as cf
from tql.algo_nlp.utils import TextClean
from mi.db import Mysql

m = Mysql(
    host='10.136.128.113',
    port=6071,
    user='browser_c3_s',
    passwd='8d8b9339efef09794c8ea2267589b2bc',
    db='browser',
)
sql = """
select *
from xindao_subject2comment 
where comment_videos is not null 
and comment_videos != "" 
and comment_style='video'
and comment_videos like '%url%'
and comment_source = "bilibili" 
and comment_final_id is not null
and comment_article_title!=''
"""
df = pd.read_sql(sql, m.conn)

df = (
    df.assign(origin_features=lambda df: df['origin_features'].map(json.loads))
        .assign(OriginCat=lambda df: df['origin_features'].map(lambda x: x['OriginCat']))
        .assign(OriginSubCat=lambda df: df['origin_features'].map(lambda x: x['OriginSubCat']))

)

tc = TextClean()


def create_word_cloud(series: pd.Series):
    wc = {}
    new_col = []
    for s in tqdm(series):
        ws = list(tc.get_noun(s))
        new_col.append(' '.join(ws))
        for w in ws:
            wc[w] = wc.get(w, 0) + 1

    WordCloud(wc.items()).wc.render(f"WordCloud_{series.name}.html")

    wc_ = pd.DataFrame(wc.items(), columns=['word', 'frequency'])
    df_noun = series.to_frame().assign(noun=new_col)

    return df_noun, wc_
