#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : ts_predict
# @Time         : 2020/7/22 12:58 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


def ts_predict(df):
    from fbprophet import Prophet
    from fbprophet.plot import plot_plotly
    import plotly.offline as py
    py.init_notebook_mode()

    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=31)
    forecast = m.predict(future)

    fig = plot_plotly(m, forecast)  # This returns a plotly Figure
    py.iplot(fig)
    return forecast