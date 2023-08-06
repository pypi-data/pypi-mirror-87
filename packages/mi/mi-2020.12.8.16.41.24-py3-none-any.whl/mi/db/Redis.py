#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : Redis
# @Time         : 2020/6/18 7:21 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

# from redis import StrictRedis, ConnectionPool
#
#
# class Redis(object):
#
#     def __init__(self, host: str, port=None):
#         if host.__contains__(":"):
#             host, port = host.split(":")
#
#         # 多个Redis实例共享一个连接池，避免每次建立、释放连接的开销。
#         pool = ConnectionPool(host=host, port=port, decode_responses=True)
#         self.client = StrictRedis(connection_pool=pool)
#
#     def randomkey(self):
#         return self.client.randomkey()


from rediscluster import RedisCluster


class Redis(object):

    def __init__(self, host_ports=None, is_dev=True):
        if host_ports is not None:
            pass
        elif is_dev:
            host_ports = "10.38.164.94:7000,10.38.164.94:7001,10.38.164.94:7002,10.38.164.94:7003,10.38.164.94:7004,10.38.164.94:7005"

        self.startup_nodes = [dict(zip(['host', 'port'], host_port.split(':'))) for host_port in host_ports.split(',')]

        self.client = RedisCluster(startup_nodes=self.startup_nodes.copy(), decode_responses=True)
