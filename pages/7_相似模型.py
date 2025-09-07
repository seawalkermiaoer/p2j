import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from utils.fonts import setup_custom_font

# 设置页面和字体
setup_custom_font("font/SimHei.ttf")
st.set_page_config(page_title="神奇的缩放魔法屋", page_icon="🧙‍♂️")

# --- 数学计算函数 ---
def calculate_side_lengths(vertices):
    """计算三角形的边长"""
    return [
        np.linalg.norm(vertices[1] - vertices[0]),
        np.linalg.norm(vertices[2] - vertices[1]),
        np.linalg.norm(vertices[0] - vertices[2])
    ]

def calculate_angles(sides):
    """使用余弦定理计算角度（返回角度制）"""
    angles = []
    # angle at vertex 0 (opposite side[1])
    angle0 = np.arccos((sides[0]**2 + sides[2]**2 - sides[1]**2) / (2 * sides[0] * sides[2]))
    angles.append(np.degrees(angle0))
    # angle at vertex 1 (opposite side[2])
    angle1 = np.arccos((sides[0]**2 + sides[1]**2 - sides[2]**2) / (2 * sides[0] * sides[1]))
    angles.append(np.degrees(angle1))
    # angle at vertex 2 (opposite side[0])
    angle2 = np.arccos((sides[1]**2 + sides[2]**2 - sides[0]**2) / (2 * sides[1] * sides[2]))
    angles.append(np.degrees(angle2))
    return angles

# --- 绘图函数 ---
def draw_similar_triangles(original_vertices, scaled_vertices, scale_factor):
    """绘制原始三角形和缩放后的相似三角形"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制原始三角形
    original_triangle = Polygon(original_vertices, facecolor='skyblue', alpha=0.7, label='原始三角形')
    ax.add_patch(original_triangle)
    ax.plot(*zip(*np.vstack([original_vertices, original_vertices[0]])), color='blue', marker='o')

    # 绘制魔法三角形
    scaled_triangle = Polygon(scaled_vertices, facecolor='salmon', alpha=0.7, label=f'魔法三角形 (缩放 {scale_factor:.2f} 倍)')
    ax.add_patch(scaled_triangle)
    ax.plot(*zip(*np.vstack([scaled_vertices, scaled_vertices[0]])), color='red', marker='o')

    # 标注顶点
    labels = ['A', 'B', 'C']
    for i, label in enumerate(labels):
        ax.text(original_vertices[i, 0] - 0.5, original_vertices[i, 1], f'{label}', fontsize=14, color='blue')
        ax.text(scaled_vertices[i, 0] + 0.3, scaled_vertices[i, 1], f"{label}'", fontsize=14, color='red')

    # 设置图形
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()
    ax.set_title("原始三角形 vs. 魔法三角形", fontsize=16)
    
    # 动态调整坐标轴范围
    all_vertices = np.vstack([original_vertices, scaled_vertices])
    x_min, y_min = np.min(all_vertices, axis=0)
    x_max, y_max = np.max(all_vertices, axis=0)
    ax.set_xlim(x_min - 2, x_max + 2)
    ax.set_ylim(y_min - 2, y_max + 2)

    return fig

# --- 主应用界面 ---
st.title("🧙‍♂️ 神奇的缩放魔法屋")
st.markdown("""
欢迎来到这个充满魔法的世界！在这里，我们将一起探索“相似”的秘密。
“相似”就像是给物体拍照，形状完全一样，但大小可以不同。
""")

# 1. 定义原始三角形 (一个边长为2, 3, 4的一般三角形)
# 使用海伦公式计算三角形顶点坐标
# 边长分别为a=2, b=3, c=4
a, b, c = 2, 3, 4
# 将边长为c的边放在x轴上，从(0,0)到(4,0)
x1, y1 = 0, 0
x2, y2 = c, 0
# 计算第三个顶点的坐标
x3 = (c**2 + a**2 - b**2) / (2 * c)
y3 = np.sqrt(a**2 - x3**2)
original_vertices = np.array([[x1, y1], [x2, y2], [x3, y3]])

# 2. 创建布局
col1, col2 = st.columns([2, 3])

with col1:
    st.header("🕹️ 控制区")
    
    # 创建“魔法缩放尺”滑块
    scale_factor = st.slider("魔法缩放尺", min_value=0.5, max_value=5.0, value=1.5, step=0.1)

    # 计算魔法三角形的顶点
    # 将原始三角形的每个顶点坐标都乘以缩放倍数
    scaled_vertices = original_vertices * scale_factor

    # 计算边长和角度
    original_sides = calculate_side_lengths(original_vertices)
    original_angles = calculate_angles(original_sides)
    
    scaled_sides = calculate_side_lengths(scaled_vertices)
    scaled_angles = calculate_angles(scaled_sides)

    st.subheader("📊 数据对比")
    
    # 显示信息
    st.markdown("**原始三角形 (蓝色)**")
    st.write(f"- **边长**: {original_sides[0]:.2f}, {original_sides[1]:.2f}, {original_sides[2]:.2f}")
    st.write(f"- **角度**: {original_angles[0]:.1f}°, {original_angles[1]:.1f}°, {original_angles[2]:.1f}°")

    st.markdown("**魔法三角形 (红色)**")
    st.write(f"- **边长**: {scaled_sides[0]:.2f}, {scaled_sides[1]:.2f}, {scaled_sides[2]:.2f}")
    st.write(f"- **角度**: {scaled_angles[0]:.1f}°, {scaled_angles[1]:.1f}°, {scaled_angles[2]:.1f}°")
    
    st.info("**魔法揭秘**：快拖动上面的缩放尺看看！你会发现，无论三角形怎么缩放，它们的**角度**永远不会变！而它们的边长，永远保持着相同的**缩放比例**。这就是相似的秘密！")

with col2:
    st.header("🖼️ 展示区")
    
    # 绘制图形
    fig = draw_similar_triangles(original_vertices, scaled_vertices, scale_factor)
    st.pyplot(fig)

st.markdown("--- ")
st.header("🤔 相似模型有什么用？")
st.markdown("""
还记得那个测量金字塔高度的聪明数学家泰勒斯吗？他用的就是相似模型的魔法！
1.  他在地上立了一根**已知高度**的木棍。
2.  阳光照下来，木棍和金字塔都会有**影子**。
3.  **木棍和它的影子**组成了一个小直角三角形，**金字塔和它的影子**也组成了一个大直角三角形。
4.  因为太阳光是平行的，所以这两个三角形是**相似**的！
5.  所以，它们的边长一定是按**同一个倍数**缩放的。
    > **（金字塔的高度 / 木棍的高度）= （金字塔影子的长度 / 木棍影子的长度）**
这样，只用测量地上的影子，就能算出无法攀登的金字塔的高度啦！
""")