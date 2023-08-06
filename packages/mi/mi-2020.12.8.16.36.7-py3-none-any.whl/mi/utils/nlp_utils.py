#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : nlp_utils
# @Time         : 2020/10/20 4:16 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from LAC import LAC
from functools import lru_cache

lac_lac = LAC(mode='lac')
lac_seg = LAC(mode='seg')


@lru_cache(512)
def nlp_cut(text, mode='seg', sep=""):
    lac = lac_seg if mode == 'seg' else lac_lac
    _ = lac.run(text)
    return sep.join(_) if sep else _
