#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 19:52
# @Author  : notI
# @Site    : 
# @File    : app.py
# @Software: streamlitTools
from io import StringIO
from collections import defaultdict

import streamlit as st
from more_itertools import first_true
import pandas as pd
import plotly.express as px

# 设置宽屏
st.set_page_config(layout="wide")

# # 设置页面标题
# st.title("Memory show")

FREE_CMD = 'watch -n 60 free'
SYSTEM_CMD = './system_status.sh'

# 定义转换函数
def transform_text(text, transformation):
    if transformation == FREE_CMD:
        text_list = text.splitlines()
        columns = first_true(text_list, pred=lambda x: 'total' in x.decode('utf-8')).decode('utf-8')+'\n'
        filter_content = [text.decode('utf-8').replace('Mem:','mem ') for text in text_list if 'Mem:' in text.decode('utf-8')]
        result = (columns + '\n'.join(filter_content)).encode('utf-8')

        df = pd.read_csv(StringIO(result.decode('utf-8')), sep='\s+').reset_index(drop=True) / 1024
        df['used-buffer'] = df['used'] - df['buffers']
        df['free+cached'] = df['free'] + df['cached']

        fig = px.line(df, title='memory usage', labels={'index': 'time(min)', 'value': 'memory usage(MB)'})
        st.plotly_chart(fig)
    elif transformation == SYSTEM_CMD:
        memory_map = defaultdict(list)
        for text in text.splitlines():
            text_str = text.decode('utf-8')
            for key in ['VmHWM', 'VmRSS']:
                if key in text_str:
                    digit = text_str.split(':')[1].split('MB')[0].strip()
                    memory_map[key].append(digit)
        df = pd.DataFrame(memory_map)
        fig = px.line(df, title='memory usage', labels={'index': 'time(min)', 'value': 'memory usage(MB)'})
        st.plotly_chart(fig)

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

left_column, _, right_column= st.columns([1,0.15,1])
with left_column:
    show('left-uploader','left-radio')
with right_column:
    show('right-uploader','right-radio')
