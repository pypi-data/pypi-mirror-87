#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : ann_content
# @Time         : 2020/11/18 7:46 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.np_utils import normalize

from tql.nlp.utils.bert_utils import Bert
from bert4keras.snippets import sequence_padding

# Bert
bert = Bert()

tokenizer = bert.tokenizer
simbert_encoder = bert.simbert_encoder


def texts2vec(texts, is_lite=0, batch_size=1000, maxlen=64):
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
        vecs = vecs[:, range(0, 768, 4)]

    return normalize(vecs)


# p = Path('/fds/1_Work/3_ANN/date=20201117')
#
#
# def reader(p):
#     return pd.read_csv(p, '\t', names=['id', 'category', 'source', 'title', 'url'])
#
#
# df = (
#     pd.concat(p.glob("*") | xProcessPoolExecutor(reader, 8))
#         .dropna(subset=['id', 'category', 'title'])
#         .drop_duplicates('title')
#     [lambda df: df.title.str.len() >= 5][lambda df: df.title.str.len() <= 64]
#     [lambda df: ~df.id.str.contains('duokan')]
# )
# df['vector'] = texts2vec(tqdm(df['title'].astype(str))).tolist()
# df.to_hdf('title.h5', 'w')

df = pd.read_hdf('/fds/1_Work/3_ANN/title.h5').assign(title=lambda df: df['title'].astype(str))

df['vector'] = texts2vec(tqdm(df['title'])).tolist()

df.to_hdf('/fds/1_Work/3_ANN/title_vec.h5', 'w', complib='blosc', complevel=8)
