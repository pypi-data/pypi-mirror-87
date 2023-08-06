#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : BaiduApi
# @Time         : 2020/9/9 10:26 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import random

from functools import lru_cache
from aip import AipOcr
from kazoo.client import KazooClient


class BaiduApi(object):

    def __init__(self):
        self.keys = self.__get_keys()

    # @lru_cache(512)
    def ocr_basic_general(self, image, options=None):
        """

        :param image:
            import requests
            image = requests.get("https://tva1.sinaimg.cn/large/007S8ZIlly1gik7a734ahj308y02qaac.jpg").content
            image = open('file', 'rb').read()
        :param options:
            options = {}
            options["language_type"] = "CHN_ENG"
            options["detect_direction"] = "true"
            options["detect_language"] = "true"
            options["probability"] = "true"
        :return:
        """
        _ = self._ocr_api().basicGeneral(image, options=options)
        return _

    def _ocr_api(self):
        APP_ID = '11516632'
        API_KEY = 'gAw0HlllOyi9sQcZulvPlmSB'
        SECRET_KEY = 'RlseXLG6SGCxXAYCbliTkCZF7KOxRMZA '

        api = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        return api

    # @property
    # def api(self):
    #     self.key = random.choice(self.keys)
    #     return AipOcr(*key)

    def __get_keys(self):
        zk = KazooClient(hosts="tjwqstaging.zk.hadoop.srv:11000")
        zk.start()
        return eval(zk.get('/tql/baidu_sdk')[0])
