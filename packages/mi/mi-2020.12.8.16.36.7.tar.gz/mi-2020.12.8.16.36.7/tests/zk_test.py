#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : test
# @Time         : 2020-03-11 14:56
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import time
import yaml
from kazoo.client import KazooClient

zk = KazooClient(hosts="tjwqstaging.zk.hadoop.srv:11000")
zk.start()



def watcher(data, stat):  # (data, stat, event)
    cfg = yaml.safe_load(data)
    print(f"Config Version: {stat.version}")
    print(cfg)


def zk_watcher(path='/mipush/hive'):
    zk.DataWatch(path)(watcher)


zk_watcher()

if __name__ == '__main__':
    # zk_schedule()
    while True:
        time.sleep(3)
        print('ok')
