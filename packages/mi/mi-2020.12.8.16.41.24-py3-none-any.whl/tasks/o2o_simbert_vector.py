#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : o2o_bert_vector
# @Time         : 2020/11/11 1:19 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from tql.pipe import *

os.environ['LOG_PATH'] = f'/home/work/yuanjie/{Path(__file__).name}.log'

from tql.utils.logger_utils import logger
from tql.utils.np_utils import normalize
from tql.nlp.utils.bert_utils import Bert
from bert4keras.snippets import sequence_padding

# Bert
bert = Bert('/home/work/yuanjie/chinese_simbert_L-12_H-768_A-12')

tokenizer = bert.tokenizer
simbert_encoder = bert.simbert_encoder


def texts2vec(texts, is_lite=1, batch_size=1000, maxlen=64):
    X = []
    S = []
    for text in texts:
        token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
        X.append(token_ids)
        S.append(segment_ids)

    data = [sequence_padding(X, length=maxlen), sequence_padding(S, length=maxlen)]

    del text, X, S
    gc.collect()

    vecs = simbert_encoder.predict(data, batch_size=batch_size)

    if is_lite:
        vecs = vecs[:, range(0, 768, 3)]

    return normalize(vecs)


def convert_vector_from_file(file='data.tsv'):
    df = pd.read_csv(file, '\t').drop_duplicates("title", ignore_index=True)
    df['vector'] = texts2vec(tqdm(df['title'].astype(str))).tolist()
    df.to_csv(file, '\t', index=False)


# Path
file = 'data.tsv'
hdfs = "~/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs"
in_path = "/user/h_data_platform/platform/browser/browser_intermediate/data/o2o_title_add_daily"
out_path = "/user/h_data_platform/platform/browser/browser_intermediate/data/o2o_simbert_vector"

# 下载数据
date = str(get_date(-1))[:10].replace('-', '')
logger.info("下载数据")
os.system(f"{hdfs} -getmerge {in_path}/date={date} {file}")

# 转换向量
logger.info("转换向量")
convert_vector_from_file(file)

# 上传数据: ls -a && rm .data.tsv.crc
logger.info("上传数据")
os.system(f"rm .*.crc && touch _SUCCESS")
os.system(f"{hdfs} -mkdir -p {out_path}/date={date}")  # todo: 覆盖
os.system(f"{hdfs} -put -f {file} {out_path}/date={date}")
os.system(f"{hdfs} -put -f _SUCCESS {out_path}/date={date}")

# # 删除数据
# logger.info("删除数据")
# os.system(f"rm *.crc")
