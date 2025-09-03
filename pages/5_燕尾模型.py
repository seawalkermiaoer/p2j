import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

st.set_page_config(page_title="燕尾模型（修正版）", page_icon="🕊️")

st.title("燕尾模型：左右燕尾面积比 = 对应底边比")

# 说明与核心公式（使用 LaTeX 展示所有公式）
st.markdown("在△ABC中，取点 F∈BC，点 E∈AC，连 AF 与 BE 交于 O。定义四块面积如下：")
st.latex(r"S_1=S_{\triangle AOB},\ S_2=S_{\triangle AOC},\ S_3=S_{\triangle BOF},\ S_4=S_{\triangle COF}")
st.markdown("核心结论：")
st.latex(r"\frac{S_1}{S_2}=\frac{S_3}{S_4}=\frac{BF}{FC}")
# 参考与等价表述（只做知识性引用，不依赖具体图形编号）
st.markdown("等价表述：")
st.latex(r"\frac{S_1+S_3}{S_2+S_4}=\frac{BD}{DC}")
st.latex(r"\frac{S_{\triangle ABD}}{S_{\triangle ADC}}=\frac{BE}{EC}")

st.subheader("交互演示")
col1, col2 = st.columns([1,1])

with col1:
    st.write("在底边BC上移动点F，在边AC上移动点E，观察比值是否恒等于BF/FC。")
    t = st.slider("F在BC上的位置 (BF/BC)", 0.1, 0.9, 0.4, 0.01)
    s = st.slider("E在AC上的位置 (AE/AC)", 0.1, 0.9, 0.6, 0.01)

# 几何构造
A = np.array([0.5, 1.0]); B = np.array([0.0, 0.0]); C = np.array([1.0, 0.0])
F = B*(1-t) + C*t            # F∈BC
E = A*(1-s) + C*s            # E∈AC

# 线段交点 O = AF ∩ BE
def intersect(P1, P2, Q1, Q2):
    """计算线段P1P2与Q1Q2的交点。

    Args:
        P1, P2: 第一条线段的端点，形如 np.array([x, y]).
        Q1, Q2: 第二条线段的端点，形如 np.array([x, y]).

    Returns:
        np.array: 两线段的交点坐标（假定两线不平行且存在唯一交点）。
    """
    u = P2-P1; v = Q2-Q1; w = Q1-P1
    M = np.array([[u[0], -v[0]], [u[1], -v[1]]])
    x = np.linalg.solve(M, w)
    return P1 + x[0]*u
O = intersect(A, F, B, E)

# 三角形面积
area = lambda P,Q,R: 0.5*abs(np.cross(Q-P, R-P))
S1 = area(A, B, O); S2 = area(A, C, O); S3 = area(B, F, O); S4 = area(C, F, O)
BF = np.linalg.norm(B-F); FC = np.linalg.norm(F-C)

ratio12 = S1/S2 if S2>0 else np.nan
ratio34 = S3/S4 if S4>0 else np.nan
ratioBF = BF/FC if FC>0 else np.nan

with col2:
    fig, ax = plt.subplots(figsize=(6,5))
    tri = Polygon([A,B,C], fill=False, ec='k', lw=2); ax.add_patch(tri)
    # 填充四块“燕尾”
    ax.add_patch(Polygon([A,B,O], fc='#FFE08A', ec='orange', alpha=0.8))  # S1
    ax.add_patch(Polygon([A,C,O], fc='#F9A8D4', ec='crimson', alpha=0.8))  # S2
    ax.add_patch(Polygon([B,F,O], fc='#93C5FD', ec='navy', alpha=0.85))    # S3
    ax.add_patch(Polygon([C,F,O], fc='#86EFAC', ec='green', alpha=0.85))   # S4
    ax.plot([A[0],F[0]],[A[1],F[1]],'k--',lw=1.2)
    ax.plot([B[0],E[0]],[B[1],E[1]],'k--',lw=1.2)
    for name,P in {"A":A,"B":B,"C":C,"E":E,"F":F,"O":O}.items():
        ax.plot(P[0],P[1],'ko',ms=6); ax.text(P[0]+0.02,P[1]+0.02,name,fontsize=10)
    ax.set_aspect('equal'); ax.set_xlim(-0.05,1.05); ax.set_ylim(-0.05,1.05)
    ax.set_title("燕尾模型示意图")
    st.pyplot(fig)

st.subheader("数值验证")
st.write(f"S1={S1:.4f}, S2={S2:.4f}, S3={S3:.4f}, S4={S4:.4f};  BF={BF:.4f}, FC={FC:.4f}")
# 使用 LaTeX 展示理论等式与数值近似
st.latex(r"\frac{S_1}{S_2}=\frac{S_3}{S_4}=\frac{BF}{FC}")
st.latex(rf"\frac{{S_1}}{{S_2}}\approx {ratio12:.4f}\ ,\ \frac{{S_3}}{{S_4}}\approx {ratio34:.4f}\ ,\ \frac{{BF}}{{FC}}\approx {ratioBF:.4f}")
