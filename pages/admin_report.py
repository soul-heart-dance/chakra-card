import streamlit as st
import time
from counter_utils import fetch_report
import pandas as pd

def render_admin_report():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- 載入動畫 ---
    st.markdown("""
    <div class="loader-wrapper" id="soul-loader">
        <div class="glow-circle"></div>
        <div class="loader-text">🌸 資料同步中...</div>
    </div>
    <script>
    setTimeout(function(){
        const loader = document.getElementById('soul-loader');
        if (loader){
            loader.style.opacity='0';
            setTimeout(()=>loader.remove(),1600);
        }
    }, 2200);
    </script>
    """, unsafe_allow_html=True)
    time.sleep(2.2)

    data = fetch_report()
    rows = data["rows"]

    st.markdown("<div class='admin-title'>📊 訪問統計報表</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='admin-sub'>今日訪問：{data['today']}　|　累積訪問：{data['total']}</div>", unsafe_allow_html=True)

    if not rows:
        st.info("目前尚無訪問資料")
        return

    df = pd.DataFrame(rows, columns=["日期", "當日訪問", "累積訪問"])
    st.line_chart(df.set_index("日期")[["當日訪問", "累積訪問"]])
    st.dataframe(df, hide_index=True)