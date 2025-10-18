# pages/admin_report.py
import streamlit as st
import pandas as pd
from datetime import datetime
from counter_utils import read_counter

st.set_page_config(page_title="SHD｜訪問統計", page_icon="📊", layout="centered")

# 權限檢查
if st.query_params.get("sara") != ["1"]:
    st.error("🚫 沒有權限訪問此頁面")
    st.stop()

# 基本樣式（不干擾訪客頁）
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;margin-top:0'>📊 訪問統計</h2>", unsafe_allow_html=True)

data = read_counter()
today = datetime.now().strftime("%Y-%m-%d")
today_count = data["dates"].get(today, 0)
total_count = data["total"]

# 數字（只有管理者看到）
st.markdown(
    f"<div style='text-align:center;font-size:1.05rem;color:#FFD6F6;'>今日：<b>{today_count}</b>　|　累積：<b>{total_count}</b></div>",
    unsafe_allow_html=True
)

# 明細表
if data["dates"]:
    df = pd.DataFrame(sorted(data["dates"].items()), columns=["日期", "訪問次數"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 趨勢圖（使用內建 Altair，不需額外套件）
    st.line_chart(df.set_index("日期"), height=260, use_container_width=True)
else:
    st.info("目前沒有資料。")