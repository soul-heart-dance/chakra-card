import streamlit as st
import pandas as pd
from counter_utils import fetch_report

def render_admin_report():
    # 載入樣式
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # 顯示 loader（不暫停）
    st.markdown("""
    <div class="loader-wrapper">
        <div class="glow-circle"></div>
        <div class="loader-text">🌙 正在載入訪問報表...</div>
    </div>
    """, unsafe_allow_html=True)

    # 主內容
    data = fetch_report()
    rows = data["rows"]

    st.markdown("<div class='admin-title'>📊 訪問統計（管理者）</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='admin-sub'>🌸 今日訪問：{data['today']}　🌕 累積訪問：{data['total']}</div>", unsafe_allow_html=True)

    if not rows:
        st.info("目前尚無訪問資料")
        return

    df = pd.DataFrame(rows, columns=["日期", "當日訪問", "累積訪問"])
    st.line_chart(df.set_index("日期")[["當日訪問", "累積訪問"]])
    st.dataframe(df, hide_index=True)
    st.markdown("<div class='footer'>© 2025 Soul Heart Dance · 與靈魂之心共舞</div>", unsafe_allow_html=True)