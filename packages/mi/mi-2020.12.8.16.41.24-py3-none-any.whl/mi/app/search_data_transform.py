#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : search_data_transform
# @Time         : 2020/6/8 3:31 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import os
import datetime
import numpy as np
import pandas as pd
import jieba.analyse as ja
from tqdm.auto import tqdm
from loguru import logger

from pathlib import Path
from gensim.models.fasttext import load_facebook_model
from concurrent.futures import ProcessPoolExecutor

logger.add('./scheduler.log',
           rotation="100 MB",
           enqueue=True,  # 异步
           encoding="utf-8",
           backtrace=True,
           diagnose=True,
           level="INFO")

_norm = lambda x, ord=2: x / np.linalg.norm(x, ord, axis=len(x.shape) > 1, keepdims=True)

delta = 1
data_name = "search_sequence_data"
base_path = "/user/h_data_platform/platform/browser/algo/data/biz"
date = str(datetime.datetime.now() - datetime.timedelta(delta))[:10].replace("-", "")

# 加载词向量
logger.info("加载词向量")
wv = load_facebook_model("/home/work/yuanjie/skipgram.title").wv


def topk_words_vec(q):
    vec = np.zeros(200)
    ws = ja.tfidf(q, topK=8)
    # print(ws)
    if ws:
        for w in ws:
            vec += wv[w] / len(ws)
        vec = _norm(vec)
    return " ".join(map(str, vec.tolist()))


# 下载数据
logger.info("下载数据")
os.system(f"~/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs -get {base_path}/search/search_sequence_agg/date={date} ./{data_name}")

# 预处理并上传数据
logger.info("创建目录")
os.system(f"~/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs -mkdir -p {base_path}/search/online/v1/date={date}")

# 获取句向量
logger.info("获取句向量")


def get_vec(args):
    i, file_name = args
    df = pd.read_parquet(f"{file_name}") \
        .assign(query=lambda df: df['query'].map(lambda x: " ".join(x))) \
        .assign(features=lambda df: df['query'].map(topk_words_vec)) \
        .rename(columns={'imei': 'id'})

    with open(f'part-{i}', 'w') as f:
        _ = "\n".join(map(str, df[['id', 'features']].to_dict('records')))
        f.write(_)


with ProcessPoolExecutor(16) as pool:
    _ = list(pool.map(get_vec, enumerate(Path(f"./{data_name}").glob("*.parquet"))))

# 上传数据
os.system(f"~/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs -put ./part-* {base_path}/search/online/v1/date={date}")

# 成功标识
logger.info("上传_SUCCESS")
os.system(f"touch ./_SUCCESS")
os.system(f"~/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs -put ./_SUCCESS {base_path}/search/online/v1/date={date}")

# 删除数据
logger.info("删除数据")
os.system(f"rm -rf {data_name} && rm part*")
