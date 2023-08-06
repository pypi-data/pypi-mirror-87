#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : Hive
# @Time         : 2020/4/22 4:56 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import os
from pyhive import hive


class Hive(object):

    def __init__(self, keytab="/fds/data/h_browser.keytab"):
        self.kinit(keytab)

    @property
    def conn(self):
        """
        conn = hive_conn()
        sql='select count(1) from browser.mipush_browser_label'
        def get_df(sql):
            df = pd.read_sql(sql, conn)
            df.columns = [col.split('.')[1] if '.' in col else col for col in df.columns]
            return df

        """

        conn = hive.connect(
            host="zjyprc-hadoop.hive.srv", port=10000,
            auth="KERBEROS", kerberos_service_name="sql_prc",
            configuration={
                'mapreduce.map.memory.mb': '10240',
                'mapreduce.reduce.memory.mb': '10240',
                'mapreduce.map.java.opts': '-Xmx3072m',
                'mapreduce.reduce.java.opts': '-Xmx3072m',
                'hive.input.format': 'org.apache.hadoop.hive.ql.io.HiveInputFormat',
                'hive.limit.optimize.enable': 'false',
                'mapreduce.job.queuename': 'root.production.miui_group.browser.miui_browser_zjy_1',  # zjy
            },
        )
        return conn

    @staticmethod
    def kinit(keytab="/fds/data/h_browser.keytab"):
        cmd = f"kinit -k -t {keytab} h_browser@XIAOMI.HADOOP && klist"
        _ = os.popen(cmd).read()
        print(_)
