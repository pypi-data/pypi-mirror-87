#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : lac_app
# @Time         : 2020/10/20 3:55 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from mi.app.base_app import *
from mi.utils.nlp_utils import nlp_cut


@app.get("/nlp/cut")
def nlp_cut_(request: Request):
    text = request.query_params.get('text', '')
    mode = request.query_params.get('mode', 'seg')
    sep = request.query_params.get('sep', '')
    # return {'text': nlp_cut(text, mode, sep)}
    return nlp_cut(text, mode, sep)


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, debug=True, reload=True)
