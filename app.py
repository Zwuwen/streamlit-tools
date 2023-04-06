#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 19:52
# @Author  : notI
# @Site    : 
# @File    : app.py
# @Software: streamlitTools

import streamlit as st

# 页面标题
st.title("文件转换应用")

# 上传文件
uploaded_file = st.file_uploader("请选择要上传的文件：", type=["txt"])

# 如果有文件上传
if uploaded_file is not None:
    # 读取文件内容
    file_contents = uploaded_file.getvalue().decode("utf-8")

    # 转换文件内容为大写字母
    transformed_contents = file_contents.upper()

    # # 显示转换后的文件内容
    # st.write("转换后的文件内容：")
    # st.write(transformed_contents)

    # 提供下载链接
    st.download_button(
        label="点击下载转换后的文件",
        data=transformed_contents.encode("utf-8"),
        file_name="converted_file.txt",
        mime="text/plain"
    )
