import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.font_manager import FontProperties
from utils.fonts import setup_custom_font

# 设置中文字体
setup_custom_font("font/SimHei.ttf")

# 页面配置
st.set_page_config(
    page_title="🐦 鸟头模型 - 神奇的几何小鸟",
    page_icon="🐦",
    layout="wide"
)

# 标题和介绍
st.title("🐦 鸟头模型 - 神奇的几何小鸟")
st.markdown("欢迎来到神奇的几何世界！今天我们要认识一位特别的朋友——鸟头模型！")

# 侧边栏配置
with st.sidebar:
    st.header("🎯 小鸟控制面板")
    
    st.subheader("大鸟的翅膀")
    big_wing1 = st.slider("大翅膀1长度", 1.0, 10.0, 5.0, 0.5)
    big_wing2 = st.slider("大翅膀2长度", 1.0, 10.0, 6.0, 0.5)
    
    st.subheader("小鸟的翅膀")
    small_wing1 = st.slider("小翅膀1长度", 0.5, 5.0, 2.0, 0.5)
    small_wing2 = st.slider("小翅膀2长度", 0.5, 5.0, 3.0, 0.5)
    
    st.subheader("🎨 显示选项")
    show_labels = st.checkbox("显示标签", True)
    show_ratio = st.checkbox("显示面积比例", True)

# 计算面积比例
def calculate_area_ratio(wing1_big, wing2_big, wing1_small, wing2_small):
    """计算两个三角形的面积比例"""
    big_product = wing1_big * wing2_big
    small_product = wing1_small * wing2_small
    ratio = big_product / small_product
    return big_product, small_product, ratio

big_product, small_product, ratio = calculate_area_ratio(
    big_wing1, big_wing2, small_wing1, small_wing2
)

# 创建可视化
tab1, tab2, tab3, tab4 = st.tabs(["🐦 小鸟图形", "📏 数学原理", "🎮 互动练习", "🏆 挑战关卡"])

with tab1:
    st.header("🐦 看！我们的几何小鸟！")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        
        # 绘制大三角形
        angle = np.pi/4  # 45度角
        x1_big = 0
        y1_big = 0
        x2_big = big_wing1 * np.cos(angle)
        y2_big = big_wing1 * np.sin(angle)
        x3_big = big_wing2 * np.cos(0)
        y3_big = big_wing2 * np.sin(0)
        
        big_triangle = np.array([[x1_big, y1_big], [x2_big, y2_big], [x3_big, y3_big]])
        
        # 绘制小三角形
        scale = 0.6
        x1_small = 0
        y1_small = 0
        x2_small = small_wing1 * np.cos(angle) * scale
        y2_small = small_wing1 * np.sin(angle) * scale
        x3_small = small_wing2 * np.cos(0) * scale
        y3_small = small_wing2 * np.sin(0) * scale
        
        small_triangle = np.array([[x1_small, y1_small], [x2_small, y2_small], [x3_small, y3_small]])
        
        # 绘制三角形
        big_patch = Polygon(big_triangle, fill=True, facecolor='lightblue', 
                           edgecolor='blue', alpha=0.7, linewidth=2)
        small_patch = Polygon(small_triangle, fill=True, facecolor='lightcoral', 
                             edgecolor='red', alpha=0.7, linewidth=2)
        
        ax.add_patch(big_patch)
        ax.add_patch(small_patch)
        
        # 添加标签
        if show_labels:
            ax.text(x2_big/2, y2_big/2, f"大翅膀1: {big_wing1}", ha='center', va='center')
            ax.text(x3_big/2, y3_big/2, f"大翅膀2: {big_wing2}", ha='center', va='center')
            ax.text(x2_small/2, y2_small/2, f"小翅膀1: {small_wing1}", ha='center', va='center')
            ax.text(x3_small/2, y3_small/2, f"小翅膀2: {small_wing2}", ha='center', va='center')
        
        ax.set_xlim(-1, max(x2_big, x3_big) + 1)
        ax.set_ylim(-1, max(y2_big, y3_big) + 1)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title("🐦 鸟头模型可视化")
        
        st.pyplot(fig)
    
    with col2:
        st.info("💡 **小鸟观察笔记**")
        st.write(f"大鸟的两个翅膀相乘：{big_wing1} × {big_wing2} = {big_product}")
        st.write(f"小鸟的两个翅膀相乘：{small_wing1} × {small_wing2} = {small_product}")
        st.success(f"**面积比例**：大鸟是小鸟的 {ratio:.1f} 倍！")

with tab2:
    st.header("📏 鸟头模型的数学咒语")

    # --- 绘制推导过程的示意图 ---
    fig_proof, ax_proof = plt.subplots(figsize=(10, 7))

    # 定义顶点
    A = np.array([0, 0])
    B = np.array([10, 0])
    C = np.array([4, 6])
    D = np.array([6, 0])  # D在AB上
    E = np.array([2, 3])  # E在AC上

    # 绘制大三角形ABC
    triangle_ABC = Polygon([A, B, C], facecolor='skyblue', alpha=0.5, label='△ABC (大鸟)')
    ax_proof.add_patch(triangle_ABC)
    ax_proof.plot(*zip(A, B, C, A), color='blue', marker='o')

    # 绘制小三角形ADE
    triangle_ADE = Polygon([A, D, E], facecolor='salmon', alpha=0.7, label='△ADE (小鸟)')
    ax_proof.add_patch(triangle_ADE)
    ax_proof.plot(*zip(A, D, E, A), color='red', marker='o')

    # 标注顶点
    ax_proof.text(A[0] - 0.5, A[1] - 0.5, 'A (鸟嘴)', fontsize=12)
    ax_proof.text(B[0] + 0.2, B[1], 'B', fontsize=12)
    ax_proof.text(C[0], C[1] + 0.3, 'C', fontsize=12)
    ax_proof.text(D[0] - 0.5, D[1] - 0.5, 'D', fontsize=12)
    ax_proof.text(E[0] - 0.5, E[1] + 0.3, 'E', fontsize=12)

    # 绘制高 h1 和 h2
    # h1: 从E到AB的垂线
    F = np.array([E[0], 0])
    ax_proof.plot([E[0], F[0]], [E[1], F[1]], 'g--', label='高 h₁')
    ax_proof.text(F[0] + 0.1, F[1] + 1.5, 'h₁', color='green', fontsize=12)
    ax_proof.text(F[0], F[1] - 0.5, 'F', fontsize=12)

    # h2: 从C到AB的垂线
    G = np.array([C[0], 0])
    ax_proof.plot([C[0], G[0]], [C[1], G[1]], 'm--', label='高 h₂')
    ax_proof.text(G[0] + 0.1, G[1] + 3, 'h₂', color='purple', fontsize=12)
    ax_proof.text(G[0], G[1] - 0.5, 'G', fontsize=12)

    # 设置图形
    ax_proof.set_aspect('equal', adjustable='box')
    ax_proof.set_xlim(-1, 11)
    ax_proof.set_ylim(-1, 7)
    ax_proof.grid(True, linestyle=':', alpha=0.6)
    ax_proof.set_title("鸟头模型推导示意图", fontsize=16)
    ax_proof.legend()

    st.pyplot(fig_proof)
    # --- 示意图绘制结束 ---
    
    st.markdown("""
    ### 🪄 魔法咒语：
    **面积大小的秘密，藏在鸟嘴两边的翅膀里！**
    
    ### 📐 数学公式：
    当两个三角形共用一个角时：
    
    **小三角形面积 : 大三角形面积 = (小翅膀1 × 小翅膀2) : (大翅膀1 × 大翅膀2)**
    
    ### 🔍 为什么这个公式成立？让我们一步步揭开秘密！
    
    #### 第一步：给三角形找"高"
    我们有两个三角形：
    - 小三角形△ADE（小鸟）
    - 大三角形△ABC（大鸟）
    它们共用顶点A（鸟嘴）
    
    **面积公式**：三角形面积 = (1/2) × 底 × 高
    
    #### 第二步：发现"高"里面的秘密
    从顶点E向底边AD画高h₁，从顶点C向底边AB画高h₂
    
    **重要发现**：h₁和h₂都垂直于同一条直线，所以它们是**平行的**！
    
    #### 第三步：利用相似三角形
    因为h₁ ∥ h₂，我们得到一对相似直角三角形：
    
    **相似比例**：h₁ / h₂ = AE / AC
    
    #### 第四步：代入面积公式
    ```
    面积比例 = S△ADE / S△ABC
             = [(1/2) × AD × h₁] / [(1/2) × AB × h₂]
             = (AD / AB) × (h₁ / h₂)
             = (AD / AB) × (AE / AC)
             = (AD × AE) / (AB × AC)
    ```
    
    ### 🍰 蛋糕例子验证：
    - 大蛋糕：边长5cm和6cm → 5×6=30
    - 小蛋糕：边长2cm和3cm → 2×3=6
    - 面积比例：30 ÷ 6 = 5倍！
    
    ### ⚡ 快速方法（三角函数）
    如果你学过三角函数，还有一个更快的推导：
    
    **面积公式**：S = (1/2)ab·sinC
    
    ```
    S△ADE = (1/2) × AD × AE × sinA
    S△ABC = (1/2) × AB × AC × sinA
    
    面积比例 = (AD × AE) / (AB × AC)
    ```
    
    ### 🎯 关键理解：
    1. **共用鸟嘴**：两个三角形必须共用一个顶点（鸟嘴）
    2. **翅膀长度**：从鸟嘴出发的两条边就是翅膀
    3. **数学证明**：通过相似三角形或三角函数严格证明
    4. **直接比例**：翅膀乘积的比就是面积比
    """)

with tab3:
    st.header("🎮 互动练习时间")
    
    st.markdown("让我们来做几道有趣的题目吧！")
    
    # 练习题1
    st.subheader("🧩 练习1：蛋糕店老板的问题")
    st.write("蛋糕店有一个大三角形蛋糕，两条边分别是8cm和10cm。现在要切出一个小蛋糕，两条边分别是4cm和5cm。大蛋糕是小蛋糕的几倍？")
    
    answer1 = st.number_input("输入你的答案", min_value=0.0, max_value=50.0, step=0.1, key="q1")
    
    correct1 = (8 * 10) / (4 * 5)
    if st.button("检查答案1", key="check1"):
        if abs(answer1 - correct1) < 0.1:
            st.success(f"🎉 答对了！8×10=80，4×5=20，80÷20=4倍！")
        else:
            st.error(f"再想想看，正确答案是{correct1}倍")
    
    # 练习题2
    st.subheader("🧩 练习2：建筑师的问题")
    st.write("建筑师设计了两个共用一个角的三角形屋顶，大屋顶的两条边是12m和15m，小屋顶的两条边是3m和4m。面积比例是多少？")
    
    answer2 = st.number_input("输入你的答案", min_value=0.0, max_value=100.0, step=0.1, key="q2")
    
    correct2 = (12 * 15) / (3 * 4)
    if st.button("检查答案2", key="check2"):
        if abs(answer2 - correct2) < 0.1:
            st.success(f"🎉 太棒了！12×15=180，3×4=12，180÷12=15倍！")
        else:
            st.error(f"再想想看，正确答案是{correct2}倍")

with tab4:
    st.header("🏆 终极挑战关卡")
    
    st.markdown("### 🎯 挑战：神秘的几何图形")
    
    challenge_col1, challenge_col2 = st.columns(2)
    
    with challenge_col1:
        st.write("观察下面的图形，思考：")
        
        # 创建一个复杂的图形
        fig2, ax2 = plt.subplots(1, 1, figsize=(8, 6))
        
        # 绘制基础图形
        x = [0, 6, 3, 0]
        y = [0, 0, 4, 0]
        ax2.fill(x, y, alpha=0.3, color='lightblue')
        
        # 内部小三角形
        x2 = [0, 2, 1, 0]
        y2 = [0, 0, 1.5, 0]
        ax2.fill(x2, y2, alpha=0.7, color='lightcoral')
        
        ax2.set_xlim(-0.5, 6.5)
        ax2.set_ylim(-0.5, 4.5)
        ax2.grid(True, alpha=0.3)
        ax2.set_title("🔍 观察这个图形")
        
        st.pyplot(fig2)
    
    with challenge_col2:
        st.write("**问题**：大三角形的两条边是6和4，小三角形的两条边是2和1.5。它们的面积比例是多少？")
        
        challenge_answer = st.number_input("输入挑战答案", min_value=0.0, max_value=20.0, step=0.1)
        
        challenge_correct = (6 * 4) / (2 * 1.5)
        
        if st.button("🏆 提交挑战答案"):
            if abs(challenge_answer - challenge_correct) < 0.1:
                st.balloons()
                st.success(f"🎊 恭喜！你成功破解了鸟头模型的秘密！6×4=24，2×1.5=3，24÷3=8倍！")
            else:
                st.error(f"很接近了！再想想看，正确答案是{challenge_correct}倍")

# 底部信息
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🐦 鸟头模型 - 让几何学习变得有趣！</p>
    <p>记住我们的魔法咒语：<strong>"面积大小的秘密，藏在鸟嘴两边的翅膀里！"</strong></p>
</div>
""", unsafe_allow_html=True)