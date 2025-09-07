import streamlit as st

st.set_page_config(
    page_title="几何问题",
    page_icon="📐",
    layout="wide"
)

st.title("几何问题")

st.markdown("""
## 欢迎来到几何问题学习平台！

这个应用将帮助你学习和理解各种几何问题。请从侧边栏选择一个主题开始学习。

### 当前可用的主题：
- 三角形分类
- 勾股定理
- 等高模型
- 一半模型
- 燕尾模型

更多主题即将推出！
""")