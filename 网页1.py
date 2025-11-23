# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 18:20:08 2025

@author: Administrator
"""

import streamlit as st

# 设置页面配置（图标、标题，可选）
st.set_page_config(page_title="我的Python网站", page_icon="😜")

# 1. 实现“页面切换”（替代HTML的路由）
page = st.sidebar.selectbox("选择页面", ["首页", "关于我"])

# 2. 首页内容（对应原index.html）
if page == "首页":
    st.title("欢迎来到我的网站！")
    st.subheader("纯Python编写，零HTML基础也能做～")
    st.write("这是复刻的首页，支持页面切换、文字展示、按钮交互！")
    
    # 模拟原网站的“用户信息”动态展示
    user_info = {"name": "绝对零度", "age": 13}
    st.success(f"当前用户：{user_info['name']} | 年龄：{user_info['age']}")
    
    # 按钮（无跳转，仅展示交互效果）
    if st.button("点击打招呼"):
        st.write("你好呀！这个网站别人也能访问哦～")

# 3. 关于页内容（对应原about.html）
elif page == "关于我":
    st.title("关于这个网站")
    st.subheader("技术栈：Python + Streamlit")
    st.write("✅ 零HTML/CSS/JS")
    st.write("✅ 纯Python代码编写")
    st.write("✅ 支持免费部署上线")
    st.write("✅ 新手友好，5分钟上手")
    st.write("作者：绝对零度")
# 4. 添加图片（和原网站一致）

st.image("https://picsum.photos/800/300", caption="随机展示图片", use_column_width=True)
