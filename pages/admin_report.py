import streamlit as st
import pandas as pd
import plotly.express as px
from counter_utils import fetch_report

def render_admin_report():
    st.set_page_config(page_title="Soul Heart Dance｜訪問統計（管理者）", page_icon="🌌")

    try:
        data = fetch_report()
        rows = data.get("rows", [])
        today = data.get("today", 0)
        total = data.get("total", 0)
    except Exception as e:
        st.markdown(
            f"""
            <div style='text-align:center; color:#ffb6c1;'>
                <h3>🌌 訪問統計（管理者）</h3>
                <div style='margin-top:2rem; color:#ff9999; font-size:1.05rem;'>
                    ❌ 讀取統計資料失敗：{e}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # ------------------------------
    # 🌸 頁首標題（粉紫柔光）
    # ------------------------------
    st.markdown("""
    <div style='text-align:center; margin-top:-1.5rem;'>
        <h3 style='color:#FFD6F6; font-weight:600; letter-spacing:1px;'>📊 訪問統計（管理者）</h3>
        <p style='color:#FFE6F7; font-size:1rem; opacity:0.85;'>今日訪問與累積總覽</p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------------
    # 💖 今日與累積統計（柔光展示）
    # ------------------------------
    st.markdown(
        f"""
        <div style='text-align:center; margin:1.2rem 0; color:#FFE6F7; font-size:1.05rem;'>
            🌸 今日訪問：<b style='color:#FFD6F6; font-size:1.2rem;'>{today}</b>　
            🌕 累積訪問：<b style='color:#FFD6F6; font-size:1.2rem;'>{total}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------
    # 📋 表格顯示
    # ------------------------------
    if not rows:
        st.info("目前尚無統計資料。")
        return

    df = pd.DataFrame(rows, columns=["日期", "訪問數", "累積訪問"])
    df = df.sort_values(by="日期", ascending=True).reset_index(drop=True)

    st.dataframe(df, hide_index=True, use_container_width=True)

    # ------------------------------
    # 📈 趨勢圖（柔光粉藍系）
    # ------------------------------
    fig = px.line(
        df,
        x="日期",
        y=["訪問數", "累積訪問"],
        markers=True,
        title="📈 訪問趨勢圖",
        color_discrete_sequence=["#a7b6ff", "#f4a7d9"]
    )
    fig.update_layout(
        title_font=dict(size=18, color="#FFE6F7"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFE6F7"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------
    # 🩵 Footer
    # ------------------------------
    st.markdown("""
    <div style='text-align:center; margin-top:2.5rem; color:#FFE6F7; font-size:0.9rem; opacity:0.7;'>
        © 2025 Soul Heart Dance ・ 與靈魂之心共舞
    </div>
    """, unsafe_allow_html=True)