#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : report
# @Time         : 2020-03-21 18:51
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import pandas as pd

""":arg
[['source', 'deviceid'],
 ['1', '9736971fbceefd95b55bee7c9de441ad'],
 ['1', '8ec2741c37e1a6030b4e87bfd63b7c81'],
 ['1', 'b0cc41b7b3f6b0411edccfbc3e8f6ac3'],
 ['1', 'ae7ef70abe557100cc716a979b143afb'],
 ['1', 'ae7ef70abe557100cc716a979b143afb']]
"""


def __getattribute__(job_type):
    return eval(job_type)


def hive(data_str):
    if data_str:
        data = eval(data_str)
        return pd.DataFrame(data[1:], columns=data[0])
    else:
        return pd.DataFrame()


def spark(data_str):
    if data_str:
        return pd.DataFrame(eval(data_str))  # TODO:spark统一格式
    else:
        return pd.DataFrame()
