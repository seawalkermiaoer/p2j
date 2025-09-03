import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import io
import base64
import matplotlib

# 设置matplotlib支持中文显示
try:
    # 尝试使用系统可用的中文字体
    from matplotlib.font_manager import FontProperties
    # 尝试多种可能的中文字体
    font_names = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS', 'STSong']
    font = None
    
    for font_name in font_names:
        try:
            font = FontProperties(fname=matplotlib.font_manager.findfont(font_name))
            break
        except:
            continue
    
    if font is not None:
        matplotlib.rcParams['font.sans-serif'] = [font.get_name()]
    else:
        # 如果找不到中文字体，使用系统默认字体
        matplotlib.rcParams['font.sans-serif'] = ['sans-serif']
        
    matplotlib.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
except Exception as e:
    st.warning(f"无法设置中文字体: {e}")
    # 使用默认字体

st.set_page_config(page_title="三角形分类", page_icon="📐")

st.title("三角形分类")

st.markdown("""
三角形是由三条线段连接三个点组成的平面图形。根据三角形的特性，我们可以从不同角度对其进行分类。
""")

# 创建绘制三角形的函数
def plot_triangle(vertices, title, color='skyblue', figsize=(4, 4)):
    """
    绘制三角形并返回图像的base64编码
    
    参数:
        vertices: 三角形的三个顶点坐标，形如 [(x1,y1), (x2,y2), (x3,y3)]
        title: 图像标题
        color: 三角形填充颜色
        figsize: 图像大小
    
    返回:
        图像的base64编码字符串
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 创建三角形
    triangle = Polygon(vertices, fill=True, color=color, alpha=0.6)
    ax.add_patch(triangle)
    
    # 绘制三角形边
    for i in range(3):
        ax.plot([vertices[i][0], vertices[(i+1)%3][0]], 
                [vertices[i][1], vertices[(i+1)%3][1]], 'k-', linewidth=2)
    
    # 添加顶点标签
    for i, (x, y) in enumerate(vertices):
        ax.text(x, y, f'P{i+1}', fontsize=12)
    
    # 设置坐标轴范围和标题
    ax.set_xlim(min([v[0] for v in vertices]) - 0.5, max([v[0] for v in vertices]) + 0.5)
    ax.set_ylim(min([v[1] for v in vertices]) - 0.5, max([v[1] for v in vertices]) + 0.5)
    ax.set_aspect('equal')
    
    # 尝试使用系统可用的字体设置标题
    try:
        from matplotlib.font_manager import FontProperties
        # 尝试获取中文字体
        font_prop = FontProperties(family='sans-serif')
        ax.set_title(title, fontsize=14, pad=10, fontproperties=font_prop)
    except:
        # 如果失败，使用默认设置
        ax.set_title(title, fontsize=14, pad=10)
    
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 将图像转换为base64编码
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return img_str

# 按角分类
st.header("1. 按角分类")

st.subheader("1.1 锐角三角形")
st.markdown("**锐角三角形**：三个内角都是锐角（小于90°）的三角形。")

# 锐角三角形示例
acute_vertices = [(0, 0), (2, 3), (4, 1)]
acute_img = plot_triangle(acute_vertices, "锐角三角形")
st.image(f"data:image/png;base64,{acute_img}", caption="锐角三角形示例")

st.subheader("1.2 直角三角形")
st.markdown("**直角三角形**：有一个内角是直角（等于90°）的三角形。")

# 直角三角形示例
right_vertices = [(0, 0), (0, 3), (4, 0)]
right_img = plot_triangle(right_vertices, "直角三角形")
st.image(f"data:image/png;base64,{right_img}", caption="直角三角形示例")

st.subheader("1.3 钝角三角形")
st.markdown("**钝角三角形**：有一个内角是钝角（大于90°）的三角形。")

# 钝角三角形示例
obtuse_vertices = [(0, 0), (1, 3), (5, 0)]
obtuse_img = plot_triangle(obtuse_vertices, "钝角三角形")
st.image(f"data:image/png;base64,{obtuse_img}", caption="钝角三角形示例")

# 按边分类
st.header("2. 按边分类")

st.subheader("2.1 等边三角形")
st.markdown("**等边三角形**：三条边长度相等的三角形。等边三角形的三个内角也都相等，均为60°。")

# 等边三角形示例
equilateral_vertices = [(2, 0), (0, 3.464), (4, 3.464)]  # 近似等边三角形
equilateral_img = plot_triangle(equilateral_vertices, "等边三角形", color='lightgreen')
st.image(f"data:image/png;base64,{equilateral_img}", caption="等边三角形示例")

st.subheader("2.2 等腰三角形")
st.markdown("**等腰三角形**：有两条边长度相等的三角形。等腰三角形的两个底角也相等。")

# 等腰三角形示例
isosceles_vertices = [(2, 0), (0, 3), (4, 3)]
isosceles_img = plot_triangle(isosceles_vertices, "等腰三角形", color='lightsalmon')
st.image(f"data:image/png;base64,{isosceles_img}", caption="等腰三角形示例")

st.subheader("2.3 不等边三角形")
st.markdown("**不等边三角形**：三条边长度都不相等的三角形。")

# 不等边三角形示例
scalene_vertices = [(0, 0), (2, 3), (5, 1)]
scalene_img = plot_triangle(scalene_vertices, "不等边三角形", color='lightpink')
st.image(f"data:image/png;base64,{scalene_img}", caption="不等边三角形示例")

# 补充说明
st.header("补充说明")
st.markdown("""
1. 三角形的内角和总是等于180°。
2. 等边三角形也是等腰三角形的一种特殊情况。
3. 三角形可以同时属于多种分类，例如：
   - 可以同时是锐角三角形和等腰三角形
   - 可以同时是直角三角形和等腰三角形
""")