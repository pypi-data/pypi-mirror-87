#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : fds2hdfs
# @Time         : 2020/11/20 5:20 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

# 上传数据: ls -a && rm .data.tsv.crc
logger.info("上传数据")
hdfs = "/fds/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs"
os.system(f"rm .*.crc && touch _SUCCESS")
os.system("kinit -k -t /fds/data/h_browser.keytab h_browser@XIAOMI.HADOOP && klist")
logger.info(os.popen(f"{hdfs} -ls").read())
os.system(f"{hdfs} -put -f _SUCCESS /user/h_data_platform/platform/browser/content_daily/date=20201119")
