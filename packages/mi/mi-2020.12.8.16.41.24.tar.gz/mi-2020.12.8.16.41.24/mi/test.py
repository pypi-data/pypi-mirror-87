#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : test
# @Time         : 2020-03-11 14:56
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from mi.app.zk_app import app

if __name__ == '__main__':
    import os
    import socket

    me = socket.gethostname() == 'yuanjie-Mac.local'

    uvicorn = "uvicorn" if me else "/opt/soft/python3/bin/uvicorn"

    main_file = __file__.split('/')[-1].split('.')[0]

    # --reload测试环境
    os.system(f"uvicorn {main_file}:app --reload --host 0.0.0.0 --port 8000")
