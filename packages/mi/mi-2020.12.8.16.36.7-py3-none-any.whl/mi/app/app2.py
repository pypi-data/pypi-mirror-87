#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : demo_app
# @Time         : 2020/10/20 3:57 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from mi.app.app1 import *


@app.get("/get2/{xxx}")
def xxxx(request: Request, xxx):
    print(type(request.query_params))
    print(request.query_params.get('a', 'xxxxxxx'))
    return {"Hello": xxx}

@app.get("/get3/{xxx}")
def xxxx(**kwargs):
    request = kwargs['request']
    print(type(request.query_params))
    print(request.query_params.get('a', 'xxxxxxx'))
    return {"Hello": kwargs['xxx']}

def func(request: Request):
    print(request.query_params.get('a', 'xxxxxxx'))
    return {"Hello": "world"}



# app.get()
# app.post('/')
app.api_route(path='/xxx', methods=["GET"])(func)

if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=9000, workers=1, debug=True, reload=True)
