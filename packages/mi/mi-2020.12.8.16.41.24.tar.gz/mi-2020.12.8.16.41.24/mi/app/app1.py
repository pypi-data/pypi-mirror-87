#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : demo_app
# @Time         : 2020/10/20 3:57 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from mi.app.base_app import App


@app.get("/get1")
def xxxx(request: Request):
    print(request.query_params.get('a', 'xxxxxxx'))
    return {"Hello": "world"}


if __name__ == '__main__':
    import socket
    import uvicorn

    me = socket.gethostname() == 'yuanjie-Mac.local'
    main_file = __file__.split('/')[-1].split('.')[0]

    # app参数必须是个字符串才能开启热更新
    uvicorn.run(app=f"{main_file}:app", host='0.0.0.0', port=8000, workers=1, debug=True, reload=True)
