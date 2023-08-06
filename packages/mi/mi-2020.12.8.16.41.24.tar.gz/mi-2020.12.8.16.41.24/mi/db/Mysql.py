#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : Mysql
# @Time         : 2020/4/16 8:12 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import pymysql


class Mysql(object):

    def __init__(self, host='10.136.128.113', port=6071, user='browser_c3_s', passwd='8d8b9339efef09794c8ea2267589b2bc',
                 db='browser'):
        """
        m = Mysql()
        df = pd.read_sql('select doc_id, title from push_daily_news limit 10', m.conn)

        sql = "select * from algo_job_common where job_id='每日浏览器push--大数据94%vs自建旧3%vs自建新3%'"

        :param host:
        :param port:
        :param user:
        :param passwd:
        :param db:
        """
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
