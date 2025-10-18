import streamlit as st
import pandas as pd
import plotly.express as px
from counter_utils import fetch_report

def render_admin_report():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    data = fetch_report()
    rows = data["rows"]

    st.markdown("<div class='admin-title'>📊 訪問統計（管理者）</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='admin-sub'>🌸 今日訪問：{data['today']}　🌕 累積訪問：{data['total']}</div>", unsafe_allow_html=True)

    if not rows:
        st.info("目前尚無訪問資料")
        return

    df = pd.DataFrame(rows, columns=["日期", "當日訪問", "累積訪問"])

    # 🎨 改回粉金柔光風格折線圖
    fig = px.line(
        df, x="日期", y=["當日訪問", "累積訪問"],
        markers=True,
        color_discrete_sequence=["#f6a8ff", "#ffdecc"]
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFE6F7",
        legend_title_text="📈 指標"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, hide_index=True)

    st.markdown("<div class='footer'>© 2025 Soul Heart Dance · 與靈魂之心共舞</div>", unsafe_allow_html=True)