import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import io
import base64
import matplotlib
from utils.fonts import setup_custom_font

# 字体设置已统一至 utils.fonts.setup_custom_font

# 使用项目内自定义字体进行初始化（优先使用 font/SimHei.ttf）
setup_custom_font("font/SimHei.ttf")

st.set_page_config(page_title="等高模型", page_icon="📏")

st.title("等高模型")

st.markdown("""
等高模型是几何学中一个重要的概念，主要用于分析和计算三角形面积之间的关系。
通过理解等高模型，我们可以更好地掌握三角形面积的计算方法和相关性质。
""")

# 基本等高模型
st.header("1. 基本等高模型")

st.markdown("""
### 三角形面积公式

三角形面积 = 底 × 高 ÷ 2

用数学符号表示为：$S = \\frac{1}{2} \\times \\text{底} \\times \\text{高}$

**重要结论**：三角形的面积取决于底与高的乘积。
""")

def plot_triangle_area_formula():
    """
    绘制三角形面积公式示意图
    
    返回:
        图像的base64编码字符串
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 定义三角形顶点
    base = 6
    height = 4
    vertices = [(0, 0), (base, 0), (base/2, height)]
    
    # 绘制三角形
    triangle = Polygon(vertices, fill=True, color='lightblue', alpha=0.7, edgecolor='blue', linewidth=2)
    ax.add_patch(triangle)
    
    # 绘制高线
    ax.plot([base/2, base/2], [0, height], 'r--', linewidth=2, label='高')
    ax.plot([0, base], [0, 0], 'g-', linewidth=3, label='底')
    
    # 添加标注
    ax.text(base/2, -0.3, f'底 = {base}', ha='center', fontsize=12, weight='bold')
    ax.text(base/2 + 0.3, height/2, f'高 = {height}', va='center', fontsize=12, weight='bold', color='red')
    ax.text(base/2, height + 0.3, f'面积 = {base} × {height} ÷ 2 = {base*height//2}', ha='center', fontsize=12, weight='bold', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    # 添加顶点标签
    ax.text(-0.3, -0.3, 'A', fontsize=12, weight='bold')
    ax.text(base + 0.2, -0.3, 'B', fontsize=12, weight='bold')
    ax.text(base/2 - 0.3, height + 0.1, 'C', fontsize=12, weight='bold')
    
    # 设置坐标轴
    ax.set_xlim(-1, base + 1)
    ax.set_ylim(-1, height + 1)
    ax.set_aspect('equal')
    
    # 设置标题
    ax.set_title("三角形面积公式示意图", fontsize=14, pad=10)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend()
    
    # 将图像转换为base64编码
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return img_str

# 显示三角形面积公式图
area_formula_img = plot_triangle_area_formula()
st.image(f"data:image/png;base64,{area_formula_img}", caption="三角形面积公式示意图")

# 等高模型的三个基本性质
st.header("2. 等高模型的三个基本性质")

st.markdown("""
基于三角形面积公式，我们可以得出等高模型的三个重要性质：

① **两个三角形高相等，面积比 = 底边比**  
   如果两个三角形的高相等，那么它们的面积比等于底边比。  
   即：$S_1 : S_2 = a : b$（其中 $a$、$b$ 分别为两个三角形的底边长）

② **两个三角形底边相等，面积比 = 高的比**  
   如果两个三角形的底边相等，那么它们的面积比等于高的比。

③ **两个三角形等底等高，则面积相等**  
   如果两个三角形的底边和高都相等，那么它们的面积相等。
""")

# 创建交互式演示
st.subheader("交互式演示")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**调整参数观察等高模型性质**")
    # 第一个三角形参数
    base1 = st.slider("三角形1的底边长度", 2, 8, 4, key="base1")
    height_common = st.slider("共同高度", 2, 6, 3, key="height")
    
    # 第二个三角形参数
    base2 = st.slider("三角形2的底边长度", 2, 8, 6, key="base2")
    
    # 计算面积
    area1 = base1 * height_common / 2
    area2 = base2 * height_common / 2
    
    st.markdown(f"""
    ### 计算结果
    - 三角形1：底 = {base1}，高 = {height_common}，面积 = {area1}
    - 三角形2：底 = {base2}，高 = {height_common}，面积 = {area2}
    
    ### 面积比验证
    - 底边比：{base1} : {base2} = {base1/base2:.2f}
    - 面积比：{area1} : {area2} = {area1/area2:.2f}
    
    **结论**：面积比 = 底边比 ✓
    """)

with col2:
    def plot_equal_height_triangles(base1, base2, height):
        """
        绘制等高三角形对比图
        
        参数:
            base1: 第一个三角形的底边长度
            base2: 第二个三角形的底边长度
            height: 共同高度
        
        返回:
            图像的base64编码字符串
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 第一个三角形
        triangle1 = Polygon([(0, 0), (base1, 0), (base1/2, height)], 
                           fill=True, color='lightblue', alpha=0.7, 
                           edgecolor='blue', linewidth=2)
        ax.add_patch(triangle1)
        
        # 第二个三角形（右侧）
        offset = base1 + 2
        triangle2 = Polygon([(offset, 0), (offset + base2, 0), (offset + base2/2, height)], 
                           fill=True, color='lightcoral', alpha=0.7, 
                           edgecolor='red', linewidth=2)
        ax.add_patch(triangle2)
        
        # 绘制高线
        ax.plot([base1/2, base1/2], [0, height], 'b--', linewidth=2)
        ax.plot([offset + base2/2, offset + base2/2], [0, height], 'r--', linewidth=2)
        
        # 绘制底边
        ax.plot([0, base1], [0, 0], 'b-', linewidth=3)
        ax.plot([offset, offset + base2], [0, 0], 'r-', linewidth=3)
        
        # 添加标注
        ax.text(base1/2, -0.3, f'a = {base1}', ha='center', fontsize=12, weight='bold', color='blue')
        ax.text(offset + base2/2, -0.3, f'b = {base2}', ha='center', fontsize=12, weight='bold', color='red')
        
        ax.text(base1/2 + 0.3, height/2, f'h = {height}', va='center', fontsize=11, weight='bold', color='blue')
        ax.text(offset + base2/2 + 0.3, height/2, f'h = {height}', va='center', fontsize=11, weight='bold', color='red')
        
        # 面积标注
        area1 = base1 * height / 2
        area2 = base2 * height / 2
        ax.text(base1/2, height/3, f'$S_1 = {area1}$', ha='center', va='center', 
                fontsize=12, weight='bold', color='blue',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
        ax.text(offset + base2/2, height/3, f'$S_2 = {area2}$', ha='center', va='center', 
                fontsize=12, weight='bold', color='red',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
        
        # 设置坐标轴
        ax.set_xlim(-0.5, offset + base2 + 0.5)
        ax.set_ylim(-0.5, height + 0.5)
        ax.set_aspect('equal')
        
        # 设置标题
        ax.set_title(f"等高三角形面积比较：$S_1 : S_2 = {base1} : {base2} = {area1} : {area2}$", 
                    fontsize=14, pad=10)
        
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # 将图像转换为base64编码
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close(fig)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_str
    
    # 显示等高三角形对比图
    equal_height_img = plot_equal_height_triangles(base1, base2, height_common)
    st.image(f"data:image/png;base64,{equal_height_img}", caption="等高三角形面积比较")

# 等高模型的运用——动点原理
st.header("3. 等高模型的运用——动点原理")

st.markdown("""
动点原理是等高模型的重要应用，主要体现在以下几个方面：

### 动点原理的核心思想

当一个点在一条直线上移动时，以这条直线为底边的所有三角形都具有相同的高，
因此这些三角形的面积只与底边长度有关。

### 主要应用场景

1. **平行线间的动点**：在两条平行线之间移动的点到两条平行线的距离（高）保持不变
2. **同底边的三角形**：共享同一底边的三角形，当顶点在平行于底边的直线上移动时面积不变
3. **面积比的计算**：利用动点原理可以快速计算复杂图形中三角形面积的比值
""")

# 动点原理演示
st.subheader("动点原理交互演示")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**调整动点位置观察面积变化**")
    
    # 固定底边
    base_length = 8
    fixed_height = 4
    
    # 动点位置
    point_x = st.slider("动点的水平位置", 1, 7, 4, key="point_x")
    
    # 计算面积（高度固定）
    area_dynamic = base_length * fixed_height / 2
    
    st.markdown(f"""
    ### 参数设置
    - 固定底边长度：{base_length}
    - 固定高度：{fixed_height}
    - 动点水平位置：{point_x}
    
    ### 观察结果
    - 三角形面积：{area_dynamic}（保持不变）
    
    **结论**：无论动点在平行线上如何移动，三角形面积始终保持不变！
    """)

with col4:
    def plot_dynamic_point_demo(base_length, height, point_x):
        """
        绘制动点原理演示图
        
        参数:
            base_length: 底边长度
            height: 固定高度
            point_x: 动点的水平位置
        
        返回:
            图像的base64编码字符串
        """
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # 绘制底边（固定）
        ax.plot([0, base_length], [0, 0], 'k-', linewidth=4, label='固定底边')
        
        # 绘制平行线（动点轨迹）
        ax.plot([-1, base_length + 1], [height, height], 'g--', linewidth=2, alpha=0.7, label='动点轨迹线')
        
        # 绘制当前三角形
        triangle = Polygon([(0, 0), (base_length, 0), (point_x, height)], 
                          fill=True, color='lightgreen', alpha=0.6, 
                          edgecolor='green', linewidth=2)
        ax.add_patch(triangle)
        
        # 绘制高线
        ax.plot([point_x, point_x], [0, height], 'r--', linewidth=2, label='高')
        
        # 标记动点
        ax.plot(point_x, height, 'ro', markersize=10, label='动点')
        
        # 显示其他可能位置的三角形（虚线）
        for x_pos in [2, 6]:
            if x_pos != point_x:
                triangle_ghost = Polygon([(0, 0), (base_length, 0), (x_pos, height)], 
                                       fill=False, edgecolor='gray', linewidth=1, 
                                       linestyle='--', alpha=0.5)
                ax.add_patch(triangle_ghost)
                ax.plot(x_pos, height, 'o', color='gray', markersize=6, alpha=0.5)
        
        # 添加标注
        ax.text(base_length/2, -0.3, f'底边 = {base_length}', ha='center', fontsize=12, weight='bold')
        ax.text(point_x + 0.3, height/2, f'高 = {height}', va='center', fontsize=12, weight='bold', color='red')
        ax.text(point_x, height + 0.3, f'动点({point_x}, {height})', ha='center', fontsize=11, weight='bold', color='red')
        
        # 面积标注
        area = base_length * height / 2
        ax.text(base_length/2, height/3, f'面积 = {area}\n(保持不变)', ha='center', va='center', 
                fontsize=12, weight='bold', color='green',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))
        
        # 顶点标签
        ax.text(-0.3, -0.2, 'A', fontsize=12, weight='bold')
        ax.text(base_length + 0.2, -0.2, 'B', fontsize=12, weight='bold')
        ax.text(point_x - 0.3, height + 0.1, 'C', fontsize=12, weight='bold', color='red')
        
        # 设置坐标轴
        ax.set_xlim(-1, base_length + 1)
        ax.set_ylim(-0.5, height + 1)
        ax.set_aspect('equal')
        
        # 设置标题
        ax.set_title("动点原理演示：动点在平行线上移动时三角形面积不变", 
                    fontsize=14, pad=10)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.legend(loc='upper right')
        
        # 将图像转换为base64编码
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close(fig)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_str
    
    # 显示动点原理演示图
    dynamic_point_img = plot_dynamic_point_demo(base_length, fixed_height, point_x)
    st.image(f"data:image/png;base64,{dynamic_point_img}", caption="动点原理演示")

# 实际应用示例
st.header("4. 实际应用示例")

st.markdown("""
### 例题：利用等高模型求面积比

**题目**：如图所示，在三角形ABC中，D是BC边上的一点，且BD:DC = 2:3。
求三角形ABD与三角形ACD的面积比。

**解题思路**：
1. 三角形ABD和三角形ACD有共同的顶点A
2. 它们的底边分别是BD和DC，位于同一直线BC上
3. 因此它们的高相等（都是点A到直线BC的距离）
4. 根据等高模型性质①：面积比 = 底边比

**解答**：
$S_{\\triangle ABD} : S_{\\triangle ACD} = BD : DC = 2 : 3$
""")

def plot_application_example():
    """
    绘制应用示例图
    
    返回:
        图像的base64编码字符串
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 定义三角形顶点
    A = (4, 5)
    B = (0, 0)
    C = (8, 0)
    D = (3.2, 0)  # BD:DC = 2:3，所以D点位置为 B + 2/5 * (C - B)
    
    # 绘制三角形ABC
    triangle_ABC = Polygon([A, B, C], fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(triangle_ABC)
    
    # 绘制三角形ABD（蓝色）
    triangle_ABD = Polygon([A, B, D], fill=True, color='lightblue', alpha=0.6, 
                          edgecolor='blue', linewidth=2)
    ax.add_patch(triangle_ABD)
    
    # 绘制三角形ACD（红色）
    triangle_ACD = Polygon([A, D, C], fill=True, color='lightcoral', alpha=0.6, 
                          edgecolor='red', linewidth=2)
    ax.add_patch(triangle_ACD)
    
    # 绘制高线
    ax.plot([A[0], A[0]], [A[1], 0], 'g--', linewidth=2, label='共同高')
    
    # 标记点
    ax.plot(*A, 'ko', markersize=8)
    ax.plot(*B, 'ko', markersize=8)
    ax.plot(*C, 'ko', markersize=8)
    ax.plot(*D, 'ro', markersize=8)
    
    # 添加标签
    ax.text(A[0] - 0.2, A[1] + 0.2, 'A', fontsize=14, weight='bold')
    ax.text(B[0] - 0.3, B[1] - 0.3, 'B', fontsize=14, weight='bold')
    ax.text(C[0] + 0.2, C[1] - 0.3, 'C', fontsize=14, weight='bold')
    ax.text(D[0], D[1] - 0.3, 'D', fontsize=14, weight='bold', color='red')
    
    # 标注线段长度
    ax.text((B[0] + D[0])/2, -0.5, 'BD = 2', ha='center', fontsize=12, weight='bold', color='blue')
    ax.text((D[0] + C[0])/2, -0.5, 'DC = 3', ha='center', fontsize=12, weight='bold', color='red')
    
    # 标注面积
    ax.text((A[0] + B[0] + D[0])/3, (A[1] + B[1] + D[1])/3, '$S_1$', 
            ha='center', va='center', fontsize=14, weight='bold', color='blue')
    ax.text((A[0] + D[0] + C[0])/3, (A[1] + D[1] + C[1])/3, '$S_2$', 
            ha='center', va='center', fontsize=14, weight='bold', color='red')
    
    # 添加结论
    ax.text(4, -1.5, '$S_1 : S_2 = BD : DC = 2 : 3$', ha='center', fontsize=14, weight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.8))
    
    # 设置坐标轴
    ax.set_xlim(-1, 9)
    ax.set_ylim(-2, 6)
    ax.set_aspect('equal')
    
    # 设置标题（统一使用全局字体设置）
    ax.set_title("等高模型应用示例：求三角形面积比", fontsize=14, pad=10)
    
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend()
    
    # 将图像转换为base64编码
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return img_str

# 显示应用示例图
application_img = plot_application_example()
st.image(f"data:image/png;base64,{application_img}", caption="等高模型应用示例")

# 总结
st.header("5. 总结")

st.markdown("""
### 等高模型的核心要点

1. **基础公式**：三角形面积 = 底 × 高 ÷ 2

2. **三个基本性质**：
   - 等高三角形：面积比 = 底边比
   - 等底三角形：面积比 = 高的比
   - 等底等高三角形：面积相等

3. **动点原理**：点在平行线上移动时，三角形面积保持不变

4. **实际应用**：
   - 快速计算复杂图形中的面积比
   - 解决几何证明题
   - 分析动态几何问题

### 学习建议

- 理解等高模型的本质：面积取决于底与高的乘积
- 多练习识别等高或等底的三角形
- 学会利用动点原理简化复杂问题
- 在实际应用中灵活运用等高模型的性质
""")