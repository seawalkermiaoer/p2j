import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from utils.fonts import setup_custom_font

# 设置页面和字体
setup_custom_font("font/SimHei.ttf")
st.set_page_config(page_title="蝴蝶翅膀的面积计算器", page_icon="🦋")

st.title("🦋 蝴蝶翅膀的面积计算器")
st.write("探索蝴蝶模型中四个翅膀面积之间隐藏的秘密！")

with st.expander("揭秘！魔法咒语为什么会生效？（点击查看数学推导）"):
    st.markdown("""
    这个秘密的背后，是另一个关于三角形面积的简单道理：“**等高的三角形，面积的比就等于底边的比**”。
    
    我们把它想象成**切披萨**来理解：
    """)
    
    st.markdown("#### 1. 看左边和上边的翅膀（S1和S2）")
    st.markdown("""
    - 把对角线BD看作是桌子边缘。三角形S1（△AOD）和S2（△AOB）都“站”在这条桌子边上。
    - 从顶点A，我们可以向桌子边BD做一条高。对于S1和S2这两个三角形来说，这条高是**一样**的！
    - 所以，它们的面积大小，就完全取决于它们在桌子边上的“底边”有多长（OD 和 OB）。
    - 因此我们得到第一个关系：
    """)
    st.latex(r''' \frac{S_1}{S_2} = \frac{OD}{OB} ''')

    st.markdown("#### 2. 看下边和右边的翅膀（S4和S3）")
    st.markdown("""
    - 同样，S4（△COD）和S3（△COB）也“站”在桌子边BD上。
    - 从顶点C，我们也向桌子边BD做一条高，这条高对于S4和S3也是**一样**的。
    - 所以，S4和S3的面积大小，也只取决于它们的底边（OD 和 OB）。
    - 因此我们得到第二个关系：
    """)
    st.latex(r''' \frac{S_4}{S_3} = \frac{OD}{OB} ''')
    
    st.markdown("#### 3. 发现真相！")
    st.markdown("""
    - 我们得到了两个都等于 `OD / OB` 的比例：
    """)
    st.latex(r''' \frac{S_1}{S_2} = \frac{OD}{OB} \quad \text{和} \quad \frac{S_4}{S_3} = \frac{OD}{OB} ''')
    st.markdown("- 这说明这两个比例是完全相等的！")
    st.latex(r''' \frac{S_1}{S_2} = \frac{S_4}{S_3} ''')
    st.markdown("- 我们把这个等式两边交叉相乘（内项积等于外项积），就得到了那个终极咒语：")
    st.latex(r''' S_1 \times S_3 = S_2 \times S_4 ''')
    st.success("魔法被我们破解啦！")

# --- 布局 ---
col1, col2 = st.columns([0.5, 0.5])

# --- 左侧：蝴蝶模型示意图 ---
def draw_static_butterfly():
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # 顶点
    A, B, C, D = (0, 8), (10, 8), (12, 0), (2, 0)
    O = (6, 4.8) # 交点

    # 绘制四边形
    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-')
    # 绘制对角线
    ax.plot([A[0], C[0]], [A[1], C[1]], 'k--')
    ax.plot([B[0], D[0]], [B[1], D[1]], 'k--')

    # 填充区域并标注S1, S2, S3, S4
    ax.fill([A[0], D[0], O[0], A[0]], [A[1], D[1], O[1], A[1]], '#FFB6C1', alpha=0.7)
    ax.text(2.5, 6, 'S1', fontsize=18, ha='center', va='center', color='black')

    ax.fill([A[0], B[0], O[0], A[0]], [A[1], B[1], O[1], A[1]], '#ADD8E6', alpha=0.7)
    ax.text(5, 7.5, 'S2', fontsize=18, ha='center', va='center', color='black')

    ax.fill([B[0], C[0], O[0], B[0]], [B[1], C[1], O[1], B[1]], '#FFB6C1', alpha=0.7)
    ax.text(9.5, 6, 'S3', fontsize=18, ha='center', va='center', color='black')

    ax.fill([D[0], C[0], O[0], D[0]], [D[1], C[1], O[1], D[1]], '#ADD8E6', alpha=0.7)
    ax.text(7, 2, 'S4', fontsize=18, ha='center', va='center', color='black')
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_aspect('equal')
    
    return fig

with col1:
    st.header("蝴蝶模型示意图")
    st.pyplot(draw_static_butterfly())
    st.info("**魔法咒语:** 相对的翅膀，面积乘起来是一样的！")
    st.latex(r''' S_1 \times S_3 = S_2 \times S_4 ''')


# --- 右侧：互动区 ---
with col2:
    st.header("输入任意三个翅膀的面积")
    
    s1 = st.number_input("S1 (左翅膀) 的面积:", min_value=0.0, value=10.0, format="%.1f")
    s2 = st.number_input("S2 (上翅膀) 的面积:", min_value=0.0, value=20.0, format="%.1f")
    s3 = st.number_input("S3 (右翅膀) 的面积:", min_value=0.0, value=30.0, format="%.1f")
    s4 = st.number_input("S4 (下翅膀) 的面积:", min_value=0.0, value=0.0, format="%.1f")

    st.info("请将你想计算的那个翅膀的面积留空或设为0，然后填写其他三个。")

    if st.button("🦋 开始计算！"):
        inputs = {'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4}
        zeros = [k for k, v in inputs.items() if v == 0.0]

        if len(zeros) != 1:
            st.error("错误：请确保有且仅有一个面积为0，作为需要计算的目标。")
        else:
            unknown_s = zeros[0]
            
            try:
                if unknown_s == 'S1':
                    result = (s2 * s4) / s3
                    s1 = result
                elif unknown_s == 'S2':
                    result = (s1 * s3) / s4
                    s2 = result
                elif unknown_s == 'S3':
                    result = (s2 * s4) / s1
                    s3 = result
                elif unknown_s == 'S4':
                    result = (s1 * s3) / s2
                    s4 = result
                
                st.success(f"计算得出，未知翅膀 {unknown_s} 的面积是：**{result:.2f}**！")

                st.subheader("魔法验证第一步：验证终极咒语")
                st.latex(r''' S_1 \times S_3 = S_2 \times S_4 ''')
                prod13 = s1 * s3
                prod24 = s2 * s4
                st.write(f"{s1:.2f} × {s3:.2f} = **{prod13:.2f}**")
                st.write(f"{s2:.2f} × {s4:.2f} = **{prod24:.2f}**")
                if np.isclose(prod13, prod24):
                    st.write("✅ 看，它们完全相等！")
                else:
                    st.write("❌ 咦，好像哪里不对劲？")

                st.subheader("魔法验证第二步：验证比例关系")
                # 验证 S1/S2 = S4/S3
                st.latex(r''' \frac{S_1}{S_2} = \frac{S_4}{S_3} ''')
                ratio12 = s1 / s2
                ratio43 = s4 / s3
                st.write(f"S1/S2 = {s1:.2f} / {s2:.2f} = **{ratio12:.3f}**")
                st.write(f"S4/S3 = {s4:.2f} / {s3:.2f} = **{ratio43:.3f}**")
                if np.isclose(ratio12, ratio43):
                    st.write("✅ 比例相等！")

                # 验证 S1/S4 = S2/S3
                st.latex(r''' \frac{S_1}{S_4} = \frac{S_2}{S_3} ''')
                ratio14 = s1 / s4
                ratio23 = s2 / s3
                st.write(f"S1/S4 = {s1:.2f} / {s4:.2f} = **{ratio14:.3f}**")
                st.write(f"S2/S3 = {s2:.2f} / {s3:.2f} = **{ratio23:.3f}**")
                if np.isclose(ratio14, ratio23):
                    st.write("✅ 比例也相等！")

            except ZeroDivisionError:
                st.error("计算错误：输入的值中不能有0（除了要求解的那个），否则无法计算比例。")