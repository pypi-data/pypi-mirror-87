#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : get_raw_url
# @Time         : 2020/9/29 11:31 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import requests


def get_raw_url(cpDocId, cp='qiehao'):
    json = {'cp': cp, 'url': '', 'cpDocId': cpDocId}
    r = requests.post('http://10.142.116.14:8235/v1/fdl/geturl', json=json)
    return r.text


if __name__ == '__main__':
    docid = 'RZBLab6kOtm0T6LiAXCV07rt6DlGoh41NdgFJsCkBdjlYzQZ3P2QsA2IeI9cX5GqhgzSml9I3t8v8BPKgvA6tz5YUNWXvQuBm42'
    print(get_raw_url(docid))