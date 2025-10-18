import streamlit as st
import pandas as pd
import altair as alt
from counter_utils import load_counter

def show_admin_report():
    query_params = st.query_params
    if query_params.get("sara") != ["1"]:
        st.error("🚫 沒有權限訪問此頁面")
        return

    st.title("📊 訪問統計報表")

    counter = load_counter()
    if not counter["dates"]:
        st.info("尚無資料可顯示 🌙")
        return

    today = pd.Timestamp.today().strftime("%Y-%m-%d")
    today_count = counter["dates"].get(today, 0)
    st.markdown(f"✨ 今日訪問：**{today_count}**　|　累積訪問：**{counter['total']}**")

    df = pd.DataFrame(list(counter["dates"].items()), columns=["日期", "訪問次數"])
    st.table(df)

    if len(df) > 1:
        chart = alt.Chart(df).mark_line(point=True).encode(
            x="日期", y="訪問次數"
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)