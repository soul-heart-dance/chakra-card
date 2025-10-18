import streamlit as st
import time
import pandas as pd
from counter_utils import fetch_report

def render_admin_report():
    # --- 套用 CSS ---
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- 載入動畫 ---
    st.markdown("""
    <div class="loader-wrapper" id="soul-loader">
        <div class="glow-circle"></div>
        <div class="loader-text">🌙 正在載入訪問報表...</div>
    </div>
    <script>
    setTimeout(() => {
      const loader = document.getElementById("soul-loader");
      if (loader) {
        loader.style.opacity = "0";
        loader.style.transition = "opacity 1.6s ease-in-out";
        setTimeout(() => loader.remove(), 1800);
      }
    }, 2200);
    </script>
    """, unsafe_allow_html=True)

    time.sleep(1.8)

    # --- 資料讀取 ---
    data = fetch_report()
    rows = data["rows"]

    st.markdown("<div class='admin-title'>📊 訪問統計報表</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='admin-sub'>🌸 今日訪問：{data['today']}　|　🌕 累積訪問：{data['total']}</div>", unsafe_allow_html=True)

    if not rows:
        st.info("目前尚無訪問資料")
        return

    df = pd.DataFrame(rows, columns=["日期", "當日訪問", "累積訪問"])
    st.line_chart(df.set_index("日期")[["當日訪問", "累積訪問"]])
    st.dataframe(df, hide_index=True)
    st.markdown("<div class='footer'>© 2025 Soul Heart Dance · 與靈魂之心共舞</div>", unsafe_allow_html=True)