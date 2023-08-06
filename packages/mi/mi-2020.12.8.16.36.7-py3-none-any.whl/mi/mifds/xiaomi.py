#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : xiaomi
# @Time         : 2020-03-03 19:19
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://github.com/XiaoMi/galaxy-fds-sdk-python

# galaxy-fds-sdk
from fds import GalaxyFDSClient, GalaxyFDSClientException, FDSClientConfiguration

config = FDSClientConfiguration(
    endpoint="cnbj1.fds.api.xiaomi.com",
    enable_cdn_for_upload=False,
    enable_cdn_for_download=False,
)
client = GalaxyFDSClient(
    access_key="AKYPIJU65VF5BW6HNW",
    access_secret="pZKCf0leb+dywTnN5WVxkueST+rq24wPSgS/9FqU",
    config=config
)

try:
    client.create_bucket("bucket-name-demo")
except GalaxyFDSClientException as e:
    print(e.message)

client.delete_bucket("bucket-name-demo")

# 上传
client.put_object("browser-algo-nanjing", 'xx.txt', open('xx.txt'))

# 下载
a = client.list_all_objects("browser-algo-nanjing", 'c').__next__()
a = client.get_object('browser-algo-nanjing', 'clr_callback.py')
a.get_next_chunk_as_string()
