#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 19:52
# @Author  : notI
# @Site    : 
# @File    : app.py
# @Software: streamlitTools
import streamlit as st

# 定义转换函数
def transform_text(text, transformation):
    if transformation == "大写":
        return text.upper()
    elif transformation == "小写":
        return text.lower()
    elif transformation == "标题":
        return text.title()
    else:
        return text

# 设置页面标题
st.title("文件操作")

# 上传文件
uploaded_file = st.file_uploader("选择一个文件")

# 设置转换选项
transformation_options = ["原始", "大写", "小写", "标题"]
selected_transformation = st.radio("选择转换方式", transformation_options)

# 如果文件存在
if uploaded_file is not None:
    # 将文件内容读入内存
    file_contents = uploaded_file.read()

    # 对文件内容进行操作
    processed_text = transform_text(file_contents, selected_transformation)

    # 显示操作后的文件内容
    st.write("处理后的文件内容：")
    st.write(processed_text)

    # 提供下载操作后的文件
    st.download_button(
        label="下载文件",
        data=processed_text,
        file_name="processed_file.txt",
        mime="text/plain"
    )

