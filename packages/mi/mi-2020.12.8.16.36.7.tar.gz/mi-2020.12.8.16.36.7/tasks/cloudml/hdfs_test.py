#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : hdfs_test
# @Time         : 2020/11/19 6:13 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

# import pandas as pd
# import tensorflow as tf


# def tf_read_text(
#         pattern,
#         file='/content_daily/date=20201117/000000_0',
#         prefix='hdfs://zjyprc-hadoop/user/h_data_platform/browser'
# ):
#     pattern = prefix + file
#
#     fs = tf.data.Dataset.list_files(file_pattern=pattern)
#     # ds = tf.data.TFRecordDataset(filenames=fs)
#     data = tf.data.TextLineDataset(fs)
#     column_names = ['id', 'category', 'source', 'title', 'url']
#     df = pd.DataFrame([i.numpy().decode().split('\t') for i in data], columns=column_names)
#     print("#####")
#     print(df.head())

# #  Quote inside a string has to be escaped by another quote
# d = tf.data.experimental.make_csv_dataset(
#     'hdfs://zjyprc-hadoop/user/h_data_platform/platform/browser/browser_intermediate/data/o2o_title_add_daily/date=20201119/part*',
#     batch_size=1,
#     field_delim='\t',
#     num_epochs=1,
#     header=True,
#     shuffle=False,
#     use_quote_delim=False
#
# )
# #
# df = pd.DataFrame(d.as_numpy_iterator())
#
# print("#########")
#
# print(df.head(10))

import os
from meutils.date_utils import date_difference

date = date_difference('%Y%m%d', days=1)
hdfs = "/fds/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs"
in_path = "/user/h_data_platform/platform/browser/browser_intermediate/data/o2o_title_add_daily"
out_path = "/user/h_data_platform/platform/browser/browser_intermediate/data/o2o_simbert_vector"


os.system("kinit -k -t /fds/data/h_browser.keytab h_browser@XIAOMI.HADOOP && klist")
os.system(f"touch _SUCCESS && {hdfs} -put -f _SUCCESS {out_path}/date=000_{date}")
print(os.popen(f"{hdfs} -ls .").read())
