#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 19:52
# @Author  : notI
# @Site    : 
# @File    : app.py
# @Software: streamlitTools
from io import StringIO
from collections import defaultdict
from toolz.curried import do

import streamlit as st
from more_itertools import first_true, consume
import pandas as pd
import plotly.express as px

# 设置宽屏
st.set_page_config(layout="wide")

FREE_CMD = 'watch -n 60 free'
SYSTEM_CMD = './system_status.sh'

# 定义转换函数
def transform_text(text, transformation):
    def _transform_free(txt):
        text_list = txt.decode('utf-8').splitlines()

        columns = first_true(text_list, pred=lambda x: 'total' in x) + '\n'
        format_str = columns + '\n'.join(t.replace('Mem:', 'mem ') for t in text_list if 'Mem:' in t)

        df = pd.read_csv(StringIO(format_str), sep='\s+').reset_index(drop=True) / 1024
        df['used-buffer'] = df['used'] - df['buffers']
        df['free+cached'] = df['free'] + df['cached']

        fig = px.line(df, title='memory usage', labels={'index': 'time(min)', 'value': 'memory usage(MB)'})
        st.plotly_chart(fig)
    def _transform_system(txt):
        text_list =txt.decode('utf-8').splitlines()

        keys = ('VmHWM', 'VmRSS')
        get_digit = lambda x: x.split(':')[1].split('MB')[0].strip()
        mem_map = defaultdict(list)

        consume(do(lambda x: mem_map[key].append(x))(get_digit(t)) for t in text_list for key in keys if key in t)
        if mem_map:
            df = pd.DataFrame(mem_map)
            fig = px.line(df, title='memory usage', labels={'index': 'time(min)', 'value': 'memory usage(MB)'})
            st.plotly_chart(fig)
        else:
            st.error('file format error')

    if transformation == FREE_CMD:
        _transform_free(text)
    elif transformation == SYSTEM_CMD:
        _transform_system(text)

def show(uploader_key,radio_key):
    # 上传文件
    uploaded_file = st.file_uploader("File to show", type=["txt", 'log'], key=uploader_key)

    # 设置转换选项
    transformation_options = [FREE_CMD, SYSTEM_CMD]
    selected_transformation = st.radio("Created by", transformation_options, horizontal=True, key=radio_key)

    # 如果文件存在
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        try:
            transform_text(file_contents, selected_transformation)
        except Exception as e:
            st.error(e)
            raise

left_column, _, right_column= st.columns([1,0.15,1])
with left_column:
    show('left-uploader','left-radio')
with right_column:
    show('right-uploader','right-radio')
