# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 18:20:08 2025

@author: Administrator
"""

import streamlit as st

# 设置页面配置（图标、标题，可选）
st.set_page_config(page_title="绝对零度的Python网站", page_icon="😜")

# 1. 用 radio 实现互斥页面切换（核心修改）
st.sidebar.header("操作菜单")
# 定义可选页面，默认选中“首页”
selected_page = st.sidebar.radio("选择页面", ["首页", "关于我"])

# 根据选中的页面显示对应内容
if selected_page == "首页":
    st.title("欢迎来到绝对零度的网站！")
    st.subheader("纯Python编写")
    st.subheader("此站可免费下载关于绝对零度的软件，相关网站网址")
    st.write("建于2025年11月26日")
    # 按钮（无跳转，仅展示交互效果）
    if st.button("点击和作者打个招呼"):
        st.write("感谢访问！！您的访问是绝对零度的动力")

elif selected_page == "关于我":
    st.title("🔧 关于这个网站")
    st.subheader("技术栈：Python + Streamlit")
    st.write("作者：绝对零度 抖音号@绝对零度")
    # 为什么选择Streamlit？
    st.write("### 🤔 为什么用Streamlit？")
    st.write("✅ 零前端基础：不用学HTML/CSS/JS，纯Python编写")
    st.write("✅ 快速开发：几行代码就能实现复杂的Web功能")
    st.write("✅ 免费部署：Streamlit Community Cloud支持免费上线")
    st.write("✅ 动态交互：支持按钮、表单、滑块等多种交互组件")
    
    # 核心功能实现原理
    st.write("### 🛠️ 核心功能实现")
    st.write("1. **页面切换**：用 `st.sidebar.selectbox` 控制不同页面的显示/隐藏")
    st.write("3. **文件下载**：用 `st.file_uploader` 接收文件，将文件内容存储到持久化存储中")
    st.write("5. **动态交互**：用 `st.button` 触发事件，`st.form` 处理表单提交，`st.rerun()` 刷新页面")
    st.write("5. **文本展示**：用 `st.title` 设置标题，`st.subheader` 设置副标题，` st.write` 显示文本")
    # 部署步骤（免费上线）
    st.write("### 🚀 如何部署到公网？")
    st.write("1. **注册GitHub账号**：访问 [GitHub](https://github.com/) 注册，这是代码托管平台")
    st.write("2. **创建仓库**：在GitHub上创建一个新仓库，命名为 `my-python-website`")
    st.write("3. **上传代码**：将这个 `app.py` 文件上传到GitHub仓库中")
    st.write("4. **部署到Streamlit**：访问 [Streamlit Community Cloud](https://share.streamlit.io/)，登录后点击 `New app`，选择你的GitHub仓库和 `app.py` 文件，点击 `Deploy`")
    st.write("5. **等待上线**：几分钟后，Streamlit会生成一个公网链接，你可以分享给别人访问！")
    
    # 未来功能计划
    st.write("### 🌟 未来功能计划")
    st.write("1. 增加用户登录功能（用 `streamlit-authenticator`）")
    st.write("2. 支持日记分类和标签")
    st.write("3. 实现Python代码在线运行功能")
    st.write("4. 添加评论功能，让别人可以回复你的日记")
    
    # 联系作者
    st.write("### 📞 联系我")
    st.write("如果你有任何问题或建议，欢迎通过以下方式联系我：")
    st.write("抖音号：@绝对零度（私信或留言）")
    st.write("GitHub：@jdld-ybd")
    
    # 感谢语
    st.write("### ❤️ 感谢支持")
    st.write("这个网站是我学习Python的小项目，希望能帮助到更多喜欢编程的人～")
    st.write("如果你喜欢这个网站，别忘了在抖音给我点赞关注哦！")
    st.write("再次感谢支持🌹🌹🌹")

# 4. 添加图片（仅在当前选中的页面显示，不会叠加）
st.image("https://picsum.photos/800/300", caption="随机展示图片", use_container_width=True)
