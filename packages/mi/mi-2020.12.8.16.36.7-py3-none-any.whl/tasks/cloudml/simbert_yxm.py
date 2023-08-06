#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : simbert
# @Time         : 2020/11/20 2:50 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import tensorflow as tf

from meutils.pipe import *
from meutils.bert_utils import SimBert
from meutils.np_utils import normalize
from meutils.io_utils import tf_read_text
from meutils.date_utils import date_difference

# Bert
simbert = SimBert()
_ = simbert.texts2vec(['第一条文本', '第二条文本'])
logger.info(_)

# Path
hdfs = "/fds/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs"
in_path = "/user/h_data_platform/platform/browser/browser_intermediate/data/o2o_title_add_daily"
out_path = "/user/h_data_platform/platform/browser/browser_intermediate/data/o2o_simbert_vector"

    # 加载数据

for days in range(1, 13):

    logger.info("加载数据")
    date = date_difference('%Y%m%d', days=days)
    file = f'/fds/data/{date}_data.tsv'

    data = tf_read_text(tf, f"{in_path}/date={date}/*")


    def parse_fn(data):
        for line in tqdm(data):
            line = line.numpy().decode()
            line = line.strip().split('\t')
            if len(line) == 7:  # 7个字段
                yield line
            else:
                logger.warning(line)


    data = list(parse_fn(data))

    cloumns = data[0]
    df = (
        pd.DataFrame(data[1:], columns=cloumns)[lambda df: df.iloc[:, 0] != cloumns[0]]  # 多文件去掉表头
            .drop_duplicates("title", ignore_index=True)
            .assign(title=lambda df: df['title'].astype(str))
    )

    # 转换向量
    logger.info("转换向量")

    df['vector'] = normalize(simbert.texts2vec(tqdm(df['title']), is_lite=0)[:, range(0, 768, 3)]).tolist()
    df.to_csv(file, '\t', index=False)





# # 上传数据: ls -a && rm .data.tsv.crc
# logger.info("上传数据")
# os.system(f"rm .*.crc && touch _SUCCESS")
# os.system("kinit -k -t /fds/data/h_browser.keytab h_browser@XIAOMI.HADOOP && klist")
#
# os.system(f"{hdfs} -mkdir -p {out_path}/date=000_{date}")  # todo: 覆盖
# os.system(f"{hdfs} -put -f {file} {out_path}/date=000_{date}")
# os.system(f"{hdfs} -put -f _SUCCESS {out_path}/date=000_{date}")
