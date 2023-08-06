#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : zk
# @Time         : 2020-03-11 13:25
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
# https://blog.csdn.net/asty9000/article/details/96430990
# https://www.cnblogs.com/shenh/p/11891878.html

# http://zkview.d.xiaomi.net/clusters/tjwqstaging/nodes


import time
import yaml
from kazoo.client import KazooClient
from ..config import Config

zk = KazooClient(hosts="tjwqstaging.zk.hadoop.srv:11000")
zk.start()


@zk.DataWatch('/mipush/hive')
def watcher(data, stat):  # (data, stat, event)
    cfg = yaml.safe_load(data)
    print(f"Config Version: {stat.version}")
    print(cfg)
    Config.zk_cfg = cfg

    # print("Event is %s" % event)

    
@zk.DataWatch('/mipush/ann/cfg')
def ann_cfg(data, stat):  # (data, stat, event)
    cfg = yaml.safe_load(data)
    print(f"Config Version: {stat.version}")
    print(cfg)
    Config.ann_cfg = cfg

    # print("Event is %s" % event)


def zk_watcher(path='/mipush/hive'):
    @zk.DataWatch(path)
    def watcher(data, stat):  # (data, stat, event)
        cfg = yaml.safe_load(data)
        Config.zk_cfg = cfg


# @zk.DataWatch('/mipush/xx')
# def watcher(data, stat):  # (data, stat, event)
#     cfg = yaml.safe_load(data)
#     Config.zk_cfg = cfg

# import schedule
# def zk_schedule():
#     schedule.every(3).seconds.do(lambda x: x)  # 每隔5秒读一次zk配置
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


if __name__ == '__main__':
    # zk_schedule()
    while True:
        time.sleep(3)
        print('ok')
