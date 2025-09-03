import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import io
import base64
import matplotlib
from utils.fonts import setup_custom_font

# 使用项目内自定义字体进行初始化（优先使用 font/SimHei.ttf）
setup_custom_font("font/SimHei.ttf")

st.set_page_config(page_title="勾股定理", page_icon="📐")

st.title("勾股定理")

st.markdown("""
勾股定理（也称为毕达哥拉斯定理）是平面几何中的一个基本定理，描述了直角三角形中三边长度之间的关系。

### 定理内容

在任何一个平面直角三角形中，两条直角边的平方之和等于斜边的平方。

在 $\\triangle ABC$ 中，若 $\\angle C=90^\\circ$，则 $a^2+b^2=c^2$。

其中：
- $a$ 和 $b$ 是直角三角形的两条直角边的长度
- $c$ 是直角三角形斜边的长度
""")

# 创建绘制直角三角形的函数
def plot_right_triangle(a, b, title, color='skyblue', figsize=(6, 6)):
    """绘制直角三角形并返回图像的 base64 编码。

    Args:
        a: 第一条直角边长度。
        b: 第二条直角边长度。
        title: 图像标题。
        color: 三角形填充颜色。
        figsize: 图像大小。

    Returns:
        图像的 base64 编码字符串。
    """
    c = np.sqrt(a**2 + b**2)
    vertices = [(0, 0), (a, 0), (0, b)]

    fig, ax = plt.subplots(figsize=figsize)

    triangle = Polygon(vertices, fill=True, color=color, alpha=0.6)
    ax.add_patch(triangle)

    ax.plot([0, a], [0, 0], 'k-', linewidth=2)
    ax.plot([0, 0], [0, b], 'k-', linewidth=2)
    ax.plot([a, 0], [0, b], 'k-', linewidth=2)

    ax.plot([0, 0.2], [0, 0], 'k-', linewidth=2)
    ax.plot([0, 0], [0, 0.2], 'k-', linewidth=2)

    ax.text(a/2, -0.3, f'a = {a}', ha='center', fontsize=12)
    ax.text(-0.3, b/2, f'b = {b}', va='center', rotation=90, fontsize=12)
    ax.text(a/2-0.5, b/2+0.3, f'c = {c:.2f}', ha='center', fontsize=12)

    ax.text(-0.2, -0.2, 'C', fontsize=12)
    ax.text(a+0.2, -0.2, 'A', fontsize=12)
    ax.text(-0.2, b+0.2, 'B', fontsize=12)

    ax.set_xlim(-1, a+1)
    ax.set_ylim(-1, b+1)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=14, pad=10)
    ax.grid(True, linestyle='--', alpha=0.7)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str

# 勾股定理可视化
st.header("勾股定理可视化")

col1, col2 = st.columns(2)

with col1:
    st.subheader("设置直角三角形的边长")
    a = st.slider("直角边a的长度", 1, 10, 3)
    b = st.slider("直角边b的长度", 1, 10, 4)
    c = np.sqrt(a**2 + b**2)

    st.markdown(f"""
    ### 计算结果
    - 直角边a = {a}
    - 直角边b = {b}
    - 斜边c = {c:.2f}

    ### 验证勾股定理
    $a^2 + b^2 = {a}^2 + {b}^2 = {a**2} + {b**2} = {a**2 + b**2}$

    $c^2 = {c:.2f}^2 = {c**2:.2f}$

    因此，$a^2 + b^2 = c^2$ 成立。
    """)

with col2:
    triangle_img = plot_right_triangle(a, b, f"直角三角形 (a={a}, b={b}, c={c:.2f})")
    st.image(f"data:image/png;base64,{triangle_img}", caption="勾股定理图示")

# 勾股定理的证明
st.header("勾股定理的证明")

st.markdown("""
勾股定理有很多种证明方法，以下是一种常见的几何证明：

1. 构造一个边长为 $a+b$ 的正方形
2. 在正方形内部放置四个全等的直角三角形，每个三角形的两条直角边分别为 $a$ 和 $b$
3. 这四个三角形围成的中间区域是一个边长为 $c$ 的正方形
4. 正方形的总面积可以表示为：$(a+b)^2 = a^2 + 2ab + b^2$
5. 正方形的总面积也可以表示为：$4 \\cdot \\frac{1}{2}ab + c^2 = 2ab + c^2$
6. 由于这两个表达式相等，我们有：$a^2 + 2ab + b^2 = 2ab + c^2$
7. 化简得到：$a^2 + b^2 = c^2$
""")

# 下面的图像绘制与原逻辑一致，仅移除局部字体设置，改为全局字体
def plot_pythagorean_proof(a, b):
    """
    绘制勾股定理证明图并返回图像的base64编码
    
    参数:
        a: 第一条直角边的长度
        b: 第二条直角边的长度
    
    返回:
        图像的base64编码字符串
    """
    # 计算斜边长度
    c = np.sqrt(a**2 + b**2)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # 第一个图：四个三角形围成的大正方形
    ax1.set_xlim(-0.5, a+b+0.5)
    ax1.set_ylim(-0.5, a+b+0.5)
    
    # 绘制外部正方形
    square = plt.Rectangle((0, 0), a+b, a+b, fill=False, color='black', linewidth=2)
    ax1.add_patch(square)
    
    # 绘制四个全等的直角三角形（正确的顶点坐标）
    triangle1 = Polygon([(0, 0), (a, 0), (0, b)], fill=True, color='skyblue', alpha=0.7, edgecolor='blue')
    triangle2 = Polygon([(a, 0), (a+b, 0), (a+b, a)], fill=True, color='skyblue', alpha=0.7, edgecolor='blue')
    triangle3 = Polygon([(a+b, a), (a+b, a+b), (b, a+b)], fill=True, color='skyblue', alpha=0.7, edgecolor='blue')
    triangle4 = Polygon([(b, a+b), (0, a+b), (0, b)], fill=True, color='skyblue', alpha=0.7, edgecolor='blue')
    
    ax1.add_patch(triangle1)
    ax1.add_patch(triangle2)
    ax1.add_patch(triangle3)
    ax1.add_patch(triangle4)
    
    # 绘制中间的正方形（边长为c的正方形）
    inner_square = Polygon([(a, 0), (a+b, a), (b, a+b), (0, b)], fill=True, color='lightgreen', alpha=0.7, edgecolor='green')
    ax1.add_patch(inner_square)
    
    # 添加边长标签
    ax1.text(a/2, -0.3, f'a = {a}', ha='center', fontsize=12, weight='bold')
    ax1.text(-0.3, b/2, f'b = {b}', va='center', rotation=90, fontsize=12, weight='bold')
    ax1.text(a+b+0.3, a/2, f'a = {a}', va='center', rotation=90, fontsize=12, weight='bold')
    ax1.text((a+b)/2, a+b+0.3, f'b = {b}', ha='center', fontsize=12, weight='bold')
    
    # 添加斜边标签
    ax1.text((a+b/2)/2, (0+a/2)/2, f'c = {c:.1f}', ha='center', va='center', rotation=np.degrees(np.arctan(a/b)), fontsize=10, color='green', weight='bold')
    
    # 添加面积标签
    ax1.text((a+b/2)/2, (a+b+b/2)/2, f'$c^2$', ha='center', va='center', fontsize=14, color='green', weight='bold')
    
    # 设置标题（统一使用全局字体设置）
    ax1.set_title("勾股定理证明：四个三角形 + 中间正方形", fontsize=14, pad=10)
    
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    # 第二个图：重新排列的面积分解
    ax2.set_xlim(-0.5, a+b+0.5)
    ax2.set_ylim(-0.5, a+b+0.5)
    
    # 绘制外部正方形
    square = plt.Rectangle((0, 0), a+b, a+b, fill=False, color='black', linewidth=2)
    ax2.add_patch(square)
    
    # 绘制重新排列的区域：两个正方形和两个矩形
    square_a = plt.Rectangle((0, 0), a, a, fill=True, color='lightcoral', alpha=0.7, edgecolor='red')
    square_b = plt.Rectangle((a, a), b, b, fill=True, color='lightblue', alpha=0.7, edgecolor='blue')
    rect1 = plt.Rectangle((a, 0), b, a, fill=True, color='lightyellow', alpha=0.7, edgecolor='orange')
    rect2 = plt.Rectangle((0, a), a, b, fill=True, color='lightyellow', alpha=0.7, edgecolor='orange')
    
    ax2.add_patch(square_a)
    ax2.add_patch(square_b)
    ax2.add_patch(rect1)
    ax2.add_patch(rect2)
    
    # 添加面积标签
    ax2.text(a/2, a/2, f'$a^2$\n$= {a**2}$', ha='center', va='center', fontsize=12, weight='bold')
    ax2.text(a+b/2, a+b/2, f'$b^2$\n$= {b**2}$', ha='center', va='center', fontsize=12, weight='bold')
    ax2.text(a+b/2, a/2, f'$ab$\n$= {a*b}$', ha='center', va='center', fontsize=11, weight='bold')
    ax2.text(a/2, a+b/2, f'$ab$\n$= {a*b}$', ha='center', va='center', fontsize=11, weight='bold')
    
    # 添加边长标签
    ax2.text(a/2, -0.3, f'a = {a}', ha='center', fontsize=12, weight='bold')
    ax2.text(a+b/2, -0.3, f'b = {b}', ha='center', fontsize=12, weight='bold')
    ax2.text(-0.3, a/2, f'a = {a}', va='center', rotation=90, fontsize=12, weight='bold')
    ax2.text(-0.3, a+b/2, f'b = {b}', va='center', rotation=90, fontsize=12, weight='bold')
    
    # 设置标题（统一使用全局字体设置）
    ax2.set_title(f"面积重新排列：$(a+b)^2 = a^2 + 2ab + b^2 = {(a+b)**2}$", fontsize=14, pad=10)
    
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    
    # 将图像转换为base64编码
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return img_str

# 显示勾股定理证明图
proof_img = plot_pythagorean_proof(a, b)
st.image(f"data:image/png;base64,{proof_img}", caption="勾股定理证明图示")

# 勾股定理的应用
st.header("勾股定理的应用")

st.markdown("""
勾股定理在现实生活中有许多应用，例如：

1. **建筑与工程**：用于确保建筑物的墙壁是垂直的，或者计算斜坡的长度。

2. **导航**：用于计算两点之间的直线距离。

3. **测量**：测量员使用勾股定理来计算难以直接测量的距离。

4. **物理学**：在向量分析中，勾股定理用于计算合力或分解力。

5. **计算机图形学**：用于计算屏幕上两点之间的距离。
""")

# 实际应用示例
st.subheader("实际应用示例：计算梯子高度")

st.markdown("""
假设一个梯子靠在墙上，梯子底部距离墙壁3米，梯子长度为5米，我们可以使用勾股定理计算梯子能够到达的高度。

设梯子能够到达的高度为 $h$，则：

$3^2 + h^2 = 5^2$

$9 + h^2 = 25$

$h^2 = 16$

$h = 4$

因此，梯子能够到达的高度是4米。
""")

# 创建梯子示例图
def plot_ladder_example():
    """
    绘制梯子示例图并返回图像的base64编码
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 绘制墙壁和地面
    ax.plot([0, 0], [0, 5], 'k-', linewidth=3)  # 墙壁
    ax.plot([0, 5], [0, 0], 'k-', linewidth=3)  # 地面
    
    # 绘制梯子
    ax.plot([0, 3], [4, 0], 'r-', linewidth=4)  # 梯子
    
    # 添加标签
    ax.text(1.5, -0.3, '3米', ha='center', fontsize=12)
    ax.text(-0.3, 2, '4米', va='center', rotation=90, fontsize=12)
    ax.text(1.8, 2.2, '5米', ha='center', rotation=-53, fontsize=12)
    
    # 设置坐标轴范围和标题
    ax.set_xlim(-0.5, 5)
    ax.set_ylim(-0.5, 5)
    
    # 设置标题（统一使用全局字体设置）
    ax.set_title("梯子靠墙问题", fontsize=14, pad=10)
    
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 将图像转换为base64编码
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return img_str

# 显示梯子示例图
ladder_img = plot_ladder_example()
st.image(f"data:image/png;base64,{ladder_img}", caption="梯子靠墙问题示例")

# 历史背景
st.header("历史背景")

st.markdown("""
勾股定理的名称来源于中国古代数学家勾股（约公元前6世纪），但在西方世界，这个定理通常被称为毕达哥拉斯定理，以纪念古希腊数学家毕达哥拉斯（约公元前570年-约公元前495年）。

实际上，这个定理在毕达哥拉斯之前就已经被巴比伦人和埃及人所知晓。巴比伦人在公元前1800年左右的粘土板上记录了一些勾股三元组（满足勾股定理的三个整数）。

在中国，《周髀算经》（约公元前1100年至公元前256年）中记载了"勾三股四弦五"的直角三角形，这是最早的勾股三元组之一。
""")