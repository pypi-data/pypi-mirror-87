#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : __init__.py
# @Time         : 2020-03-04 14:45
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import os
import re
import socket
from pathlib import Path

dev = False if re.search('.c3_|.c4_', os.environ.get('DOCKER_JOBNAME', '')) else True
prd = Path('/home/work').exists()

isMac = socket.gethostname() == 'yuanjie-Mac.local'

get_module_path = lambda path, file=__file__: \
    os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))
