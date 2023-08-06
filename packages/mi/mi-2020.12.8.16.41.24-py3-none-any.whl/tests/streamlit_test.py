#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : s
# @Time         : 2019-11-01 10:23
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://docs.streamlit.io/api.html?highlight=markdown#display-progress-and-status
# https://docs.streamlit.io/cli.html
# streamlit run your_script.py --server.port 80
# 8051
# https://github.com/streamlit/streamlit/tree/develop/lib/streamlit/hello

import os
import time
import datetime
import numpy as np
import pandas as pd
import streamlit as st
from mi.db import Mongo
from bson import json_util

m = Mongo()
# side
date = st.sidebar.date_input('设置日期', datetime.datetime.today()).__str__()
biz = st.sidebar.selectbox('业务场景', ('browser', 'xiangkan', 'newhome'), index=1)
collection = m.db[f"push.{biz}"]
st.sidebar.markdown("> Params:")
st.sidebar.json({'date': date, 'biz': biz})

# mongo
st.sidebar.markdown('---')
st.sidebar.markdown('**Mongo Find**')
mongo_filter = st.sidebar.text_input('', {'date': date})  # **kwargs
_ = collection.find_one(eval(mongo_filter))
st.sidebar.json(json_util.dumps(_))

# TODO: 增加其他特性 email/常用api/

# body
st.title("Push实验报告")  # st.markdown("# Push Report")


# @st.cache(suppress_st_warning=True)
def get_data(jobid, date):
    try:
        _ = collection.find({'jobid': jobid, 'date': date})
        df = pd.DataFrame(list(_)[0]['data'])
    except Exception as e:
        st.markdown(f"`{e}`")
        df = pd.DataFrame()
    return df


def multi_select_df(df, subset=None, axis=0, color="yellow"):
    cols = st.multiselect('MultiSelect', df.columns.tolist(), df.columns.tolist())
    st.dataframe(df[cols].style.highlight_max(subset, color, axis))


df = get_data('想看vs大数据', date).set_index("experimentName")
multi_select_df(df)

df = df.drop('date', 1).T
multi_select_df(df, axis=1)
