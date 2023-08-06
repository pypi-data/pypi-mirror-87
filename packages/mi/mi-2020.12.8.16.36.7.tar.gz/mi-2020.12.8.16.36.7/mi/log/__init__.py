#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : __init__.py
# @Time         : 2019-12-10 17:24
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import sys
from loguru import logger
trace1 = logger.add(
    'runtime_{time}.log',
    rotation="100 MB",
    retention='10 days',
    level="INFO",
    catch=True
)
logger.info("xxxx")
logger.debug('this is a debug message')
logger.info('this is a info message')


if __name__ == '__main__':
    @logger.catch()
    def f():
        1 / 0
        return 1111


    print(f())
