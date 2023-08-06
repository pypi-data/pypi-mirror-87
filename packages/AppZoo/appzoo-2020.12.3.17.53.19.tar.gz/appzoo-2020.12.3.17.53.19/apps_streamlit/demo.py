#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : demo
# @Time         : 2020/11/5 8:21 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import streamlit as st

st.title("Hello World")

x = st.slider('Select a value')
st.write(x, 'squared is', x * x)

# Magic commands implicitly `st.write()`
''' _This_ is some __Markdown__ '''
