#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : hdfs2fds
# @Time         : 2020/11/20 2:25 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *

from meutils.io_utils import tf_read_text

import tensorflow as tf

data = tf_read_text(tf, "/user/h_data_platform/work/kolibre/output/20201120/adhoc_194518/*")

for i in data:
    print(i.numpy().decode(), '########')
    break
data = list(map(lambda x: x.numpy().decode().split('\t'), data))
df = pd.DataFrame(data[1:], columns=data[0])
df.to_csv('/fds/1_Work/5_ocr/data2.txt', '\t', index=False)
