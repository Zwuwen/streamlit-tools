#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 19:52
# @Author  : notI
# @Site    : 
# @File    : app.py
# @Software: streamlitTools
from io import StringIO

import streamlit as st
from more_itertools import first_true
import pandas as pd
import plotly.express as px

# 定义转换函数
def transform_text(text, transformation):
    if transformation == "FREE-CMD-FORMAT":
        filter_strs = ['Mem:']
        text_list = text.splitlines()
        columns = first_true(text_list, pred=lambda x: 'total' in x.decode('utf-8')).decode('utf-8')+'\n'
        filter_content = [text.decode('utf-8').replace('Mem:','mem ') for text in text_list if 'Mem:' in text.decode('utf-8')]
        result = (columns + '\n'.join(filter_content)).encode('utf-8')
        return result
    elif transformation == "大写":
        return text.upper()
    elif transformation == "小写":
        return text.lower()
    elif transformation == "标题":
        return text.title()

# 设置页面标题
st.title("文本处理工具")

# 上传文件
uploaded_file = st.file_uploader("选择一个文件", type=["txt",'log'])

# 设置转换选项
transformation_options = ["FREE-CMD-FORMAT","大写", "小写", "标题"]
selected_transformation = st.radio("选择转换方式", transformation_options,horizontal=True)

# 如果文件存在
if uploaded_file is not None:
    # 将文件内容读入内存
    file_contents = uploaded_file.read()

    # 对文件内容进行操作
    processed_text = transform_text(file_contents, selected_transformation)

    if selected_transformation == "FREE-CMD-FORMAT":
        df = pd.read_csv(StringIO(processed_text.decode('utf-8')),sep='\s+').reset_index(drop=True)/1024
        # st.dataframe(df)
        fig = px.line(df,title='memory usage',labels={'index':'time(min)','value':'memory usage(MB)'})
        st.plotly_chart(fig)

    # 显示操作后的文件内容
    # st.write("处理后的文件内容：")
    # st.write(processed_text)

    # 提供下载操作后的文件
    st.download_button(
        label="下载文件",
        data=processed_text,
        file_name="processed_file.txt",
        mime="text/plain"
    )
