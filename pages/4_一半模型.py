import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import io
import base64
import matplotlib

# 设置matplotlib支持中文显示（仅在系统存在中文字体时才启用，避免findfont警告）
try:
    from matplotlib.font_manager import FontProperties
    font_names = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS', 'STSong']
    font = None
    # 逐个尝试常见中文字体；仅当findfont确认存在实际字体文件时才使用
    for font_name in font_names:
        try:
            path = matplotlib.font_manager.findfont(FontProperties(family=font_name), fallback_to_default=False)
            font = FontProperties(fname=path)
            break
        except Exception:
            continue
    if font is not None:
        matplotlib.rcParams['font.sans-serif'] = [font.get_name()]
    else:
        # 如果系统未安装常见中文字体，回退到默认无衬线字体，避免SimHei缺失警告
        matplotlib.rcParams['font.sans-serif'] = ['sans-serif']
    # 正常显示负号
    matplotlib.rcParams['axes.unicode_minus'] = False
except Exception as e:
    st.warning(f"无法设置中文字体: {e}")
    # 使用默认字体

st.set_page_config(page_title="一半模型", page_icon="📐")

st.title("一半模型")

st.markdown("""
一半模型是几何学中一个重要的概念，主要研究三角形与平行四边形之间的面积关系。
通过理解一半模型，我们可以更好地掌握不同几何图形面积之间的内在联系。
""")

# 基本概念
st.header("1. 一半模型的基本概念")

st.markdown("""
### 核心原理

一半模型基于以下两个重要性质：

**性质1：等底等高的平行四边形面积相等**  
如果两个平行四边形具有相同的底边长度和高度，那么它们的面积相等。
这个性质适用于所有平行四边形，包括正方形和长方形这些特殊情况。

**性质2：三角形面积等于等底等高平行四边形面积的一半**  
任意三角形的面积等于与它具有相同底边和高度的平行四边形面积的一半。

用数学公式表示：
- 平行四边形面积：$S_{平行四边形} = \\text{底} \\times \\text{高}$
- 三角形面积：$S_{三角形} = \\frac{1}{2} \\times \\text{底} \\times \\text{高} = \\frac{1}{2} \\times S_{平行四边形}$
""")

def plot_basic_concept():
    """
    绘制一半模型基本概念示意图
    
    返回:
        图像的base64编码字符串
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 左图：等底等高的平行四边形
    base = 6
    height = 4
    
    # 第一个平行四边形（长方形）
    rect1 = Rectangle((0, 0), base, height, fill=True, color='lightblue', 
                     alpha=0.7, edgecolor='blue', linewidth=2)
    ax1.add_patch(rect1)
    
    # 第二个平行四边形（斜平行四边形）
    offset = 8
    parallelogram = Polygon([(offset, 0), (offset + base, 0), 
                           (offset + base + 1.5, height), (offset + 1.5, height)], 
                          fill=True, color='lightcoral', alpha=0.7, 
                          edgecolor='red', linewidth=2)
    ax1.add_patch(parallelogram)
    
    # 添加标注
    ax1.text(base/2, -0.5, f'底 = {base}', ha='center', fontsize=12, weight='bold', color='blue')
    ax1.text(-0.5, height/2, f'高 = {height}', va='center', fontsize=12, weight='bold', color='blue', rotation=90)
    
    ax1.text(offset + base/2 + 0.75, -0.5, f'底 = {base}', ha='center', fontsize=12, weight='bold', color='red')
    ax1.text(offset - 0.5, height/2, f'高 = {height}', va='center', fontsize=12, weight='bold', color='red', rotation=90)
    
    # 面积标注
    area = base * height
    ax1.text(base/2, height/2, f'面积 = {area}', ha='center', va='center', 
            fontsize=12, weight='bold', color='blue',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    ax1.text(offset + base/2 + 0.75, height/2, f'面积 = {area}', ha='center', va='center', 
            fontsize=12, weight='bold', color='red',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    ax1.set_xlim(-1, offset + base + 3)
    ax1.set_ylim(-1, height + 1)
    ax1.set_aspect('equal')
    ax1.set_title("性质1：等底等高的平行四边形面积相等", fontsize=14, pad=10)
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    # 右图：三角形与平行四边形的关系
    # 平行四边形
    rect2 = Rectangle((0, 0), base, height, fill=True, color='lightyellow', 
                     alpha=0.5, edgecolor='orange', linewidth=2)
    ax2.add_patch(rect2)
    
    # 三角形
    triangle = Polygon([(0, 0), (base, 0), (base/2, height)], 
                      fill=True, color='lightgreen', alpha=0.8, 
                      edgecolor='green', linewidth=3)
    ax2.add_patch(triangle)
    
    # 添加标注
    ax2.text(base/2, -0.5, f'底 = {base}', ha='center', fontsize=12, weight='bold')
    ax2.text(-0.5, height/2, f'高 = {height}', va='center', fontsize=12, weight='bold', rotation=90)
    
    # 面积标注
    triangle_area = base * height / 2
    parallelogram_area = base * height
    
    ax2.text(base/4, height/3, f'三角形\n面积 = {triangle_area}', ha='center', va='center', 
            fontsize=11, weight='bold', color='green',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
    ax2.text(3*base/4, height/3, f'平行四边形\n面积 = {parallelogram_area}', ha='center', va='center', 
            fontsize=11, weight='bold', color='orange',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
    
    # 关系说明
    ax2.text(base/2, height + 0.5, f'{triangle_area} = {parallelogram_area} ÷ 2', 
            ha='center', fontsize=12, weight='bold', color='purple',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))
    
    ax2.set_xlim(-1, base + 1)
    ax2.set_ylim(-1, height + 1.5)
    ax2.set_aspect('equal')
    ax2.set_title("性质2：三角形面积 = 平行四边形面积 ÷ 2", fontsize=14, pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    
    # 将图像转换为base64编码
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return img_str

# 显示基本概念图
basic_concept_img = plot_basic_concept()
st.image(f"data:image/png;base64,{basic_concept_img}", caption="一半模型基本概念示意图")

# 交互式演示
st.header("2. 交互式演示")

st.subheader("2.1 等底等高平行四边形面积比较")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**调整参数观察平行四边形面积变化**")
    
    # 参数控制
    base_length = st.slider("底边长度", 3, 10, 6, key="base_para")
    height_para = st.slider("高度", 2, 8, 4, key="height_para")
    skew_angle = st.slider("倾斜角度 (度)", 0, 60, 30, key="skew_angle")
    
    # 计算面积
    area_rect = base_length * height_para
    area_para = base_length * height_para  # 平行四边形面积与长方形相同
    
    st.markdown(f"""
    ### 计算结果
    - 长方形：底 = {base_length}，高 = {height_para}，面积 = {area_rect}
    - 平行四边形：底 = {base_length}，高 = {height_para}，面积 = {area_para}
    
    **结论**：等底等高的平行四边形面积相等 ✓
    """)

with col2:
    def plot_parallelogram_comparison(base, height, angle):
        """
        绘制等底等高平行四边形比较图
        
        参数:
            base: 底边长度
            height: 高度
            angle: 倾斜角度（度）
        
        返回:
            图像的base64编码字符串
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 长方形
        rect = Rectangle((0, 0), base, height, fill=True, color='lightblue', 
                        alpha=0.7, edgecolor='blue', linewidth=2)
        ax.add_patch(rect)
        
        # 平行四边形
        offset = base + 2
        skew = height * np.tan(np.radians(angle))
        parallelogram = Polygon([(offset, 0), (offset + base, 0), 
                               (offset + base + skew, height), (offset + skew, height)], 
                              fill=True, color='lightcoral', alpha=0.7, 
                              edgecolor='red', linewidth=2)
        ax.add_patch(parallelogram)
        
        # 绘制高线
        ax.plot([0, 0], [0, height], 'b--', linewidth=2, alpha=0.7)
        ax.plot([offset + skew, offset + skew], [0, height], 'r--', linewidth=2, alpha=0.7)
        
        # 添加标注
        ax.text(base/2, -0.3, f'底 = {base}', ha='center', fontsize=12, weight='bold', color='blue')
        ax.text(-0.3, height/2, f'高 = {height}', va='center', fontsize=12, weight='bold', color='blue', rotation=90)
        
        ax.text(offset + base/2 + skew/2, -0.3, f'底 = {base}', ha='center', fontsize=12, weight='bold', color='red')
        ax.text(offset + skew - 0.3, height/2, f'高 = {height}', va='center', fontsize=12, weight='bold', color='red', rotation=90)
        
        # 面积标注
        area = base * height
        ax.text(base/2, height/2, f'面积 = {area}', ha='center', va='center', 
                fontsize=12, weight='bold', color='blue',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
        ax.text(offset + base/2 + skew/2, height/2, f'面积 = {area}', ha='center', va='center', 
                fontsize=12, weight='bold', color='red',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
        
        # 设置坐标轴
        ax.set_xlim(-0.5, offset + base + skew + 0.5)
        ax.set_ylim(-0.5, height + 0.5)
        ax.set_aspect('equal')
        ax.set_title(f"等底等高平行四边形面积比较（倾斜角度：{angle}°）", fontsize=14, pad=10)
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # 将图像转换为base64编码
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close(fig)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_str
    
    # 显示平行四边形比较图
    para_comparison_img = plot_parallelogram_comparison(base_length, height_para, skew_angle)
    st.image(f"data:image/png;base64,{para_comparison_img}", caption="等底等高平行四边形面积比较")

st.subheader("2.2 三角形与平行四边形面积关系")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**调整参数观察三角形与平行四边形面积关系**")
    
    # 参数控制
    tri_base = st.slider("底边长度", 3, 10, 6, key="tri_base")
    tri_height = st.slider("高度", 2, 8, 4, key="tri_height")
    triangle_type = st.selectbox("三角形类型", ["等腰三角形", "直角三角形", "一般三角形"], key="tri_type")
    
    # 计算面积
    triangle_area = tri_base * tri_height / 2
    parallelogram_area = tri_base * tri_height
    
    st.markdown(f"""
    ### 计算结果
    - 三角形：底 = {tri_base}，高 = {tri_height}，面积 = {triangle_area}
    - 平行四边形：底 = {tri_base}，高 = {tri_height}，面积 = {parallelogram_area}
    
    ### 面积关系验证
    - 三角形面积：{triangle_area}
    - 平行四边形面积的一半：{parallelogram_area} ÷ 2 = {parallelogram_area/2}
    
    **结论**：三角形面积 = 平行四边形面积 ÷ 2 ✓
    """)

with col4:
    def plot_triangle_parallelogram_relation(base, height, tri_type):
        """
        绘制三角形与平行四边形面积关系图
        
        参数:
            base: 底边长度
            height: 高度
            tri_type: 三角形类型
        
        返回:
            图像的base64编码字符串
        """
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # 绘制平行四边形（背景）
        rect = Rectangle((0, 0), base, height, fill=True, color='lightyellow', 
                        alpha=0.4, edgecolor='orange', linewidth=2, linestyle='--')
        ax.add_patch(rect)
        
        # 根据三角形类型绘制不同的三角形
        if tri_type == "等腰三角形":
            triangle = Polygon([(0, 0), (base, 0), (base/2, height)], 
                              fill=True, color='lightgreen', alpha=0.8, 
                              edgecolor='green', linewidth=3)
        elif tri_type == "直角三角形":
            triangle = Polygon([(0, 0), (base, 0), (0, height)], 
                              fill=True, color='lightgreen', alpha=0.8, 
                              edgecolor='green', linewidth=3)
        else:  # 一般三角形
            triangle = Polygon([(0, 0), (base, 0), (base*0.3, height)], 
                              fill=True, color='lightgreen', alpha=0.8, 
                              edgecolor='green', linewidth=3)
        
        ax.add_patch(triangle)
        
        # 绘制高线
        if tri_type == "等腰三角形":
            ax.plot([base/2, base/2], [0, height], 'g--', linewidth=2, label='高')
            apex_x = base/2
        elif tri_type == "直角三角形":
            ax.plot([0, 0], [0, height], 'g--', linewidth=2, label='高')
            apex_x = 0
        else:
            ax.plot([base*0.3, base*0.3], [0, height], 'g--', linewidth=2, label='高')
            apex_x = base*0.3
        
        # 添加标注
        ax.text(base/2, -0.3, f'底 = {base}', ha='center', fontsize=12, weight='bold')
        ax.text(-0.3, height/2, f'高 = {height}', va='center', fontsize=12, weight='bold', rotation=90)
        
        # 面积标注
        triangle_area = base * height / 2
        parallelogram_area = base * height
        
        # 三角形面积标注
        if tri_type == "直角三角形":
            ax.text(base/3, height/3, f'三角形\n面积 = {triangle_area}', ha='center', va='center', 
                    fontsize=11, weight='bold', color='green',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
        else:
            ax.text(apex_x/2 + base/4, height/3, f'三角形\n面积 = {triangle_area}', ha='center', va='center', 
                    fontsize=11, weight='bold', color='green',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
        
        # 平行四边形面积标注（在三角形外部区域）
        if tri_type == "直角三角形":
            ax.text(2*base/3, height/2, f'平行四边形\n面积 = {parallelogram_area}', ha='center', va='center', 
                    fontsize=11, weight='bold', color='orange',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
        else:
            ax.text(3*base/4, height/2, f'平行四边形\n面积 = {parallelogram_area}', ha='center', va='center', 
                    fontsize=11, weight='bold', color='orange',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
        
        # 关系说明
        ax.text(base/2, height + 0.5, f'关系：{triangle_area} = {parallelogram_area} ÷ 2', 
                ha='center', fontsize=12, weight='bold', color='purple',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))
        
        # 设置坐标轴
        ax.set_xlim(-0.5, base + 0.5)
        ax.set_ylim(-0.5, height + 1)
        ax.set_aspect('equal')
        ax.set_title(f"{tri_type}与平行四边形面积关系", fontsize=14, pad=10)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.legend()
        
        # 将图像转换为base64编码
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close(fig)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_str
    
    # 显示三角形与平行四边形关系图
    tri_para_img = plot_triangle_parallelogram_relation(tri_base, tri_height, triangle_type)
    st.image(f"data:image/png;base64,{tri_para_img}", caption="三角形与平行四边形面积关系")

# 实际应用示例
st.header("3. 实际应用示例")

st.markdown("""
### 例题1：利用一半模型求面积

**题目**：如图所示，在平行四边形ABCD中，E是BC边的中点，F是AD边的中点。
求三角形AEF的面积与平行四边形ABCD面积的比值。

**解题思路**：
1. 利用一半模型的性质
2. 分析三角形与平行四边形的底高关系
3. 计算面积比值
""")

def plot_application_example():
    """
    绘制应用示例图
    
    返回:
        图像的base64编码字符串
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 定义平行四边形顶点
    A = (0, 0)
    B = (6, 0)
    C = (8, 4)
    D = (2, 4)
    
    # E是BC中点，F是AD中点
    E = ((B[0] + C[0])/2, (B[1] + C[1])/2)
    F = ((A[0] + D[0])/2, (A[1] + D[1])/2)
    
    # 绘制平行四边形ABCD
    parallelogram = Polygon([A, B, C, D], fill=True, color='lightblue', 
                           alpha=0.3, edgecolor='blue', linewidth=2)
    ax.add_patch(parallelogram)
    
    # 绘制三角形AEF
    triangle_AEF = Polygon([A, E, F], fill=True, color='lightcoral', 
                          alpha=0.7, edgecolor='red', linewidth=3)
    ax.add_patch(triangle_AEF)
    
    # 标记点
    points = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F}
    for name, point in points.items():
        ax.plot(*point, 'ko', markersize=8)
        if name in ['E', 'F']:
            ax.text(point[0], point[1] + 0.3, name, ha='center', fontsize=14, 
                   weight='bold', color='red')
        else:
            ax.text(point[0] - 0.3, point[1] - 0.3, name, ha='center', fontsize=14, 
                   weight='bold', color='blue')
    
    # 绘制辅助线
    ax.plot([A[0], E[0]], [A[1], E[1]], 'r-', linewidth=2, alpha=0.8)
    ax.plot([E[0], F[0]], [E[1], F[1]], 'r-', linewidth=2, alpha=0.8)
    ax.plot([F[0], A[0]], [F[1], A[1]], 'r-', linewidth=2, alpha=0.8)
    
    # 标注中点
    ax.text((B[0] + E[0])/2, (B[1] + E[1])/2 - 0.3, 'BE = EC', ha='center', 
           fontsize=10, color='green', weight='bold')
    ax.text((A[0] + F[0])/2, (A[1] + F[1])/2 + 0.3, 'AF = FD', ha='center', 
           fontsize=10, color='green', weight='bold')
    
    # 面积标注
    # 平行四边形面积
    para_center_x = (A[0] + B[0] + C[0] + D[0]) / 4
    para_center_y = (A[1] + B[1] + C[1] + D[1]) / 4
    ax.text(para_center_x + 1, para_center_y, '平行四边形ABCD', ha='center', va='center', 
           fontsize=12, weight='bold', color='blue',
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
    
    # 三角形面积
    tri_center_x = (A[0] + E[0] + F[0]) / 3
    tri_center_y = (A[1] + E[1] + F[1]) / 3
    ax.text(tri_center_x, tri_center_y, '△AEF', ha='center', va='center', 
           fontsize=12, weight='bold', color='red',
           bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
    
    # 设置坐标轴
    ax.set_xlim(-1, 9)
    ax.set_ylim(-1, 5)
    ax.set_aspect('equal')
    ax.set_title("应用示例：利用一半模型求面积比", fontsize=16, pad=15)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # 添加解题步骤
    solution_text = """
解题步骤：
1. 设平行四边形ABCD的面积为S
2. 由于E、F分别是中点，可以利用一半模型
3. 通过面积分割和组合计算得出结果
4. △AEF的面积 = S/4
    """
    
    ax.text(9.5, 2, solution_text, fontsize=11, va='center',
           bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9))
    
    # 将图像转换为base64编码
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return img_str

# 显示应用示例图
application_img = plot_application_example()
st.image(f"data:image/png;base64,{application_img}", caption="一半模型应用示例")

# 动态证明演示
st.header("4. 动态证明演示")

st.markdown("""
### 一半模型的动态证明

通过动态演示来理解为什么三角形面积等于平行四边形面积的一半。
""")

col5, col6 = st.columns(2)

with col5:
    st.markdown("**证明方法选择**")
    
    proof_method = st.selectbox("选择证明方法", 
                               ["拼接法证明", "分割法证明", "平移法证明"], 
                               key="proof_method")
    
    demo_base = st.slider("演示图形底边长度", 4, 8, 6, key="demo_base")
    demo_height = st.slider("演示图形高度", 3, 6, 4, key="demo_height")
    
    st.markdown(f"""
    ### 证明说明
    
    **{proof_method}**：
    
    - 底边长度：{demo_base}
    - 高度：{demo_height}
    - 平行四边形面积：{demo_base * demo_height}
    - 三角形面积：{demo_base * demo_height / 2}
    """)

with col6:
    def plot_dynamic_proof(base, height, method):
        """
        绘制动态证明图
        
        参数:
            base: 底边长度
            height: 高度
            method: 证明方法
        
        返回:
            图像的base64编码字符串
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if method == "拼接法证明":
            # 绘制两个相同的三角形拼接成平行四边形
            triangle1 = Polygon([(0, 0), (base, 0), (base/2, height)], 
                               fill=True, color='lightgreen', alpha=0.7, 
                               edgecolor='green', linewidth=2)
            triangle2 = Polygon([(base/2, height), (base, 0), (base + base/2, height)], 
                               fill=True, color='lightcoral', alpha=0.7, 
                               edgecolor='red', linewidth=2)
            
            ax.add_patch(triangle1)
            ax.add_patch(triangle2)
            
            # 标注
            ax.text(base/4, height/3, '三角形1', ha='center', va='center', 
                   fontsize=11, weight='bold', color='green')
            ax.text(3*base/4 + base/4, height/3, '三角形2', ha='center', va='center', 
                   fontsize=11, weight='bold', color='red')
            
            ax.text(base/2 + base/4, height + 0.3, 
                   f'两个相同三角形拼成平行四边形\n面积 = 2 × {base*height/2} = {base*height}', 
                   ha='center', fontsize=12, weight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))
            
            ax.set_xlim(-0.5, base + base/2 + 0.5)
            
        elif method == "分割法证明":
            # 绘制平行四边形，用对角线分割
            rect = Rectangle((0, 0), base, height, fill=True, color='lightyellow', 
                           alpha=0.5, edgecolor='orange', linewidth=2)
            ax.add_patch(rect)
            
            # 绘制对角线
            ax.plot([0, base], [0, height], 'k--', linewidth=2, label='对角线')
            
            # 标注两个三角形
            ax.text(base/3, height/3, '△1', ha='center', va='center', 
                   fontsize=14, weight='bold', color='blue')
            ax.text(2*base/3, 2*height/3, '△2', ha='center', va='center', 
                   fontsize=14, weight='bold', color='red')
            
            ax.text(base/2, height + 0.3, 
                   f'对角线将平行四边形分成两个相等的三角形\n每个三角形面积 = {base*height} ÷ 2 = {base*height/2}', 
                   ha='center', fontsize=12, weight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))
            
            ax.set_xlim(-0.5, base + 0.5)
            
        else:  # 平移法证明
            # 绘制三角形和通过平移得到的平行四边形
            triangle = Polygon([(0, 0), (base, 0), (base/3, height)], 
                              fill=True, color='lightgreen', alpha=0.7, 
                              edgecolor='green', linewidth=2)
            ax.add_patch(triangle)
            
            # 平移后的三角形（虚线）
            triangle_moved = Polygon([(base/3, height), (base + base/3, height), (2*base/3, 0)], 
                                   fill=False, edgecolor='red', linewidth=2, linestyle='--')
            ax.add_patch(triangle_moved)
            
            # 形成的平行四边形轮廓
            parallelogram_outline = Polygon([(0, 0), (base, 0), (base + base/3, height), (base/3, height)], 
                                          fill=False, edgecolor='blue', linewidth=3)
            ax.add_patch(parallelogram_outline)
            
            # 箭头表示平移
            ax.annotate('', xy=(2*base/3, height/2), xytext=(base/6, height/2),
                       arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
            ax.text(base/2, height/2 + 0.3, '平移', ha='center', fontsize=12, 
                   weight='bold', color='purple')
            
            ax.text(base/2 + base/6, height + 0.3, 
                   f'通过平移构造平行四边形\n三角形面积 = 平行四边形面积 ÷ 2', 
                   ha='center', fontsize=12, weight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))
            
            ax.set_xlim(-0.5, base + base/3 + 0.5)
        
        ax.set_ylim(-0.5, height + 1)
        ax.set_aspect('equal')
        ax.set_title(f"{method}演示", fontsize=14, pad=10)
        ax.grid(True, linestyle='--', alpha=0.3)
        
        if method == "分割法证明":
            ax.legend()
        
        # 将图像转换为base64编码
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close(fig)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        return img_str
    
    # 显示动态证明图
    proof_img = plot_dynamic_proof(demo_base, demo_height, proof_method)
    st.image(f"data:image/png;base64,{proof_img}", caption=f"{proof_method}演示")

# 总结
st.header("5. 总结")

st.markdown("""
### 一半模型的核心要点

1. **基本性质**：
   - 等底等高的平行四边形面积相等
   - 三角形面积 = 等底等高平行四边形面积 ÷ 2

2. **数学表达**：
   - $S_{平行四边形} = \\text{底} \\times \\text{高}$
   - $S_{三角形} = \\frac{1}{2} \\times \\text{底} \\times \\text{高} = \\frac{1}{2} \\times S_{平行四边形}$

3. **证明方法**：
   - 拼接法：两个相同三角形拼成平行四边形
   - 分割法：对角线将平行四边形分成两个相等三角形
   - 平移法：通过平移构造等底等高的平行四边形

4. **实际应用**：
   - 快速计算复杂图形面积
   - 解决几何证明题
   - 分析图形面积关系

### 学习建议

- 理解一半模型的几何本质
- 掌握多种证明方法
- 练习识别等底等高的图形关系
- 在实际问题中灵活运用一半模型
- 结合等高模型等其他几何模型综合应用
""")