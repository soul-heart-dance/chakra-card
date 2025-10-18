import streamlit as st
import pandas as pd
import plotly.express as px
from counter_utils import fetch_report

def render_admin_report():
    st.set_page_config(page_title="Soul Heart Dance｜訪問統計（管理者）", page_icon="📊")

    try:
        data = fetch_report()
        rows = data.get("rows", [])
        today = data.get("today", 0)
        total = data.get("total", 0)
    except Exception as e:
        st.markdown(
            f"""
            <div style='text-align:center; color:#ffb6c1;'>
                <h3>📊 訪問統計（管理者）</h3>
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