#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : load_yaml
# @Time         : 2020-03-21 21:40
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import yaml

_ = yaml.safe_load(open("cfg.yaml").read())
print(_)
print(eval(_['email']['biz']['msg_fn'])(777777777))