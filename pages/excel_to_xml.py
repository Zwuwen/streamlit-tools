#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/4/17 16:33
# @Author  : notI
# @Site    : 
# @File    : excel_to_xml.py
# @Software: streamlitTools

import streamlit as st
import pandas as pd

# 定义将Excel转换为XML的函数
def excel_to_xml(file):
    # 读取Excel文件
    df = pd.read_excel(file)

    # 将DataFrame转换为XML
    xml = df.to_xml()

    # 返回XML字符串
    return xml

# Streamlit应用程序
def main():
    # 添加页面标题
    st.title("Excel转XML")

    # 添加文件上传组件
    uploaded_file = st.file_uploader("上传Excel文件", type="xlsx")

    # 如果文件上传成功
    if uploaded_file is not None:
        # 将Excel转换为XML
        xml = excel_to_xml(uploaded_file)

        # 显示XML
        st.code(xml, language="xml")

        # 添加下载XML文件的链接
        st.download_button("下载XML文件", data=xml, file_name="output.xml", mime="text/xml")

# 运行应用程序
if __name__ == "__main__":
    main()
