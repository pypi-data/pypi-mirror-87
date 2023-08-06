#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : zk_utils
# @Time         : 2020/7/2 5:26 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from kazoo.client import KazooClient

zk = KazooClient(hosts="tjwqstaging.zk.hadoop.srv:11000")
zk.start()

# 注册节点
zk.create('/mipush/biz/search', b'this is test',makepath=True)

# 获取节点及值
zk.get_children('/mipush/biz')
zk.get('/mipush/biz/search')

# 更改节点的值
# zk.set


import socket

ip = socket.gethostbyname(socket.gethostname())
biz = 'search'
scenes = 'autopush'

# session 中断后自动删除该节点, 实例重启后自动更新节点
zk.create(f'/mipush/ann/{biz}/{scenes}/{ip}', b'create ip nodes', makepath=True, ephemeral=True)