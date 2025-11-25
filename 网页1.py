# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 18:20:08 2025

@author: Administrator
"""

# 1. 安装依赖（本地运行时执行）：pip install streamlit streamlit-extras

# 2. 导入库
import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
from streamlit_extras.stored_state import StoredStateClient

# 3. 初始化持久化存储
ssc = StoredStateClient()

# 4. 封装核心函数
def load_diary():
    """从持久化存储加载日记数据"""
    return ssc.get("diary_list", default=[])

def save_diary(diary_list):
    """将日记数据持久化存储"""
    ssc.set("diary_list", diary_list)

def publish_diary(title, content, uploaded_file):
    """发布新日记（含附件处理）"""
    if not title or not content:
        st.error("标题和内容不能为空！")
        return False
    
    # 处理附件（存储文件内容和文件名）
    attachment = None
    if uploaded_file is not None:
        try:
            attachment = {
                "name": uploaded_file.name,
                "content": uploaded_file.getvalue().decode("utf-8")  # 存储文件内容（字符串）
            }
        except Exception as e:
            st.error(f"附件上传失败：{str(e)}")
            return False
    
    # 构造日记数据
    new_diary = {
        "title": title,
        "content": content,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "attachment": attachment
    }
    
    # 保存到持久化存储
    diary_list = load_diary()
    diary_list.insert(0, new_diary)
    save_diary(diary_list)
    
    st.success("日记发布成功！")
    if attachment:
        st.info(f"附件 '{attachment['name']}' 已一同上传。")
    return True

def edit_diary(idx, new_title, new_content, new_uploaded_file=None):
    """编辑指定索引的日记"""
    diary_list = load_diary()
    if not (0 <= idx < len(diary_list)):
        st.error("日记不存在！")
        return False
    
    # 更新标题和内容
    diary = diary_list[idx]
    diary["title"] = new_title
    diary["content"] = new_content
    
    # 更新附件（如果上传了新文件）
    if new_uploaded_file is not None:
        try:
            diary["attachment"] = {
                "name": new_uploaded_file.name,
                "content": new_uploaded_file.getvalue().decode("utf-8")
            }
        except Exception as e:
            st.error(f"附件更新失败：{str(e)}")
            return False
    
    # 保存修改
    save_diary(diary_list)
    st.success("日记编辑成功！")
    return True

def delete_diary(idx):
    """删除指定索引的日记"""
    diary_list = load_diary()
    if not (0 <= idx < len(diary_list)):
        st.error("日记不存在！")
        return False
    
    del diary_list[idx]
    save_diary(diary_list)
    st.success("日记删除成功！")
    return True

def show_diaries():
    """展示历史日记（含编辑/删除功能）"""
    diary_list = load_diary()
    if not diary_list:
        st.write("暂无日记，快去发布你的第一篇日记吧！")
        return
    
    for idx, diary in enumerate(diary_list, 1):  # 从1开始的序号
        with st.expander(f"**{idx}. {diary['title']}** - {diary['date']}", expanded=False):
            # 日记内容
            st.write(diary["content"])
            
            # 附件下载
            if diary.get("attachment"):
                attachment = diary["attachment"]
                st.download_button(
                    label="📥 下载Python附件",
                    data=attachment["content"],
                    file_name=attachment["name"],
                    mime="text/x-python"
                )
            
            # 编辑和删除按钮（两列布局）
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ 编辑", key=f"edit_{idx}"):
                    # 弹出编辑表单
                    with st.form(key=f"edit_form_{idx}"):
                        st.subheader("编辑日记")
                        new_title = st.text_input("新标题", value=diary["title"])
                        new_content = st.text_area("新内容", value=diary["content"], height=150)
                        new_uploaded_file = st.file_uploader(
                            "更新Python文件（可选，不选则保留原文件）",
                            type=["py"],
                            key=f"edit_file_{idx}"
                        )
                        
                        if st.form_submit_button("提交修改"):
                            if edit_diary(idx-1, new_title, new_content, new_uploaded_file):
                                st.rerun()  # 刷新页面，显示修改后的内容
            
            with col2:
                if st.button("🗑️ 删除", key=f"delete_{idx}"):
                    # 弹出确认框
                    st.warning("删除后无法恢复，请谨慎操作！")
                    if st.checkbox("我已确认删除", key=f"confirm_{idx}"):
                        if delete_diary(idx-1):
                            st.rerun()  # 刷新页面，移除删除的日记
        
        st.divider()  # 分隔线

# 5. 页面布局和切换
# 侧边栏（固定导航和作者信息）
with st.sidebar:
    st.header("📌 网站导航")
    st.write("1. 首页 - 网站介绍和Python演示")
    st.write("2. Python日记分享 - 发布/编辑/删除日记")
    st.write("3. 关于我 - 技术栈和部署步骤")
    st.divider()
    st.success("""
    作者：绝对零度  
    抖音号：@绝对零度  
    年龄：13岁  
    爱好：Python编程、分享技术  
    """)

# 页面选择
page = st.sidebar.selectbox("选择页面", ["首页", "python日记分享", "关于我"])

# 首页内容
if page == "首页":
    st.title("🎉 欢迎来到绝对零度的Python网站！")
    st.subheader("纯Python编写，零HTML/CSS/JS基础也能做～")
    st.write("这个网站包含日记分享、文件上传、动态交互等功能，全部用Python实现！")
    
    # Python代码演示
    st.write("### 📝 实时运行Python代码")
    st.write("点击下方按钮，看看Python代码在网页上的运行效果：")
    
    # 示例代码
    sample_code = '''
# 这是一段Python示例代码
print("Hello, Streamlit!")
print("这个网站是用Python写的～")

# 计算1到5的和
total = sum(range(1, 6))
print(f"1+2+3+4+5 = {total}")
'''
    st.code(sample_code, language="python")
    
    # 运行按钮
    if st.button("▶️ 运行代码"):
        st.write("### 运行结果：")
        st.write("Hello, Streamlit!")
        st.write("这个网站是用Python写的～")
        st.write("1+2+3+4+5 = 15")
        st.balloons()  # 弹出气球动画，增加趣味性
    
    # 作者信息卡片
    st.write("### 👨‍💻 作者介绍")
    user_info = {
        "姓名": "绝对零度",
        "抖音号": "@绝对零度",
        "年龄": 13,
        "擅长技术": "Python、Streamlit、数据分析",
        "目标": "分享更多Python小项目，帮助新手入门"
    }
    
    for key, value in user_info.items():
        st.write(f"**{key}**：{value}")
    
    # 互动按钮
    if st.button("❤️ 给作者点个赞"):
        st.success("感谢你的支持！我会继续努力分享更多有用的技术～")

# Python日记分享页面
elif page == "python日记分享":
    st.title("📓 我的Python技术日记")
    st.write("在这里记录你的Python学习心得、项目笔记，还能上传代码文件哦～")
    
    # 发布新日记表单
    st.subheader("✍️ 发布新日记")
    with st.form(key="diary_form", clear_on_submit=True):
        title = st.text_input("日记标题", placeholder="例如：今天学会了Streamlit的文件上传")
        content = st.text_area(
            "日记内容",
            height=200,
            placeholder="例如：今天我用Streamlit实现了文件上传功能，步骤是...\n1. 导入streamlit库\n2. 使用st.file_uploader组件\n3. 处理上传的文件并保存..."
        )
        uploaded_file = st.file_uploader("上传Python文件（可选，例如代码示例）", type=["py"])
        submit_button = st.form_submit_button("🚀 发布日记")
    
    if submit_button:
        publish_diary(title, content, uploaded_file)
    
    # 展示历史日记
    st.subheader("📜 历史日记")
    show_diaries()

# 关于我页面
elif page == "关于我":
    st.title("🔧 关于这个网站")
    st.subheader("技术栈：Python + Streamlit")
    
    # 为什么选择Streamlit？
    st.write("### 🤔 为什么用Streamlit？")
    st.write("✅ 零前端基础：不用学HTML/CSS/JS，纯Python编写")
    st.write("✅ 快速开发：几行代码就能实现复杂的Web功能")
    st.write("✅ 免费部署：Streamlit Community Cloud支持免费上线")
    st.write("✅ 动态交互：支持按钮、表单、滑块等多种交互组件")
    st.write("✅ 适合数据科学：内置图表、数据展示功能，适合分享数据分析项目")
    
    # 核心功能实现原理
    st.write("### 🛠️ 核心功能实现")
    st.write("1. **页面切换**：用 `st.sidebar.selectbox` 控制不同页面的显示/隐藏")
    st.write("2. **日记存储**：用 `streamlit-extras` 的 `StoredStateClient` 实现数据持久化（重启不丢失）")
    st.write("3. **文件上传**：用 `st.file_uploader` 接收文件，将文件内容存储到持久化存储中")
    st.write("4. **编辑/删除**：通过索引操作日记列表，修改后重新保存到持久化存储")
    st.write("5. **动态交互**：用 `st.button` 触发事件，`st.form` 处理表单提交，`st.rerun()` 刷新页面")
    
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
    st.write("GitHub：可以在我的仓库提交Issue（如果有GitHub账号）")
    
    # 感谢语
    st.write("### ❤️ 感谢支持")
    st.write("这个网站是我学习Python的小项目，希望能帮助到更多喜欢编程的人～")
    st.write("如果你喜欢这个网站，别忘了在抖音给我点赞关注哦！")

# 6. 底部图片（所有页面都显示）
st.write("---")  # 分隔线
st.write("### 📸 随机图片展示")
try:
    # 尝试加载随机图片
    st.image("https://picsum.photos/800/300", caption="Python编程相关图片", use_column_width=True)
except Exception as e:
    # 加载失败时显示备用图片
    st.image("https://picsum.photos/id/0/800/300", caption="备用图片", use_column_width=True)

