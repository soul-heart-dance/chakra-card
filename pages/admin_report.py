import streamlit as st
from counter_utils import get_gsheet
import pandas as pd
import altair as alt

st.set_page_config(page_title="管理者報表", page_icon="📊", layout="centered")

params = st.query_params
if params.get("sara") != ["1"]:
    st.error("🚫 沒有權限訪問此頁面")
    st.stop()

sheet = get_gsheet()
records = sheet.get_all_records()

if not records:
    st.info("尚無資料")
else:
    df = pd.DataFrame(records)
    total_visits = df["訪問數"].sum()
    today = df.iloc[-1]["訪問數"]

    st.markdown(f"### 今日訪問：{today} | 累積訪問：{total_visits}")

    chart = alt.Chart(df).mark_line(point=True).encode(
        x='日期',
        y='訪問數',
        tooltip=['日期', '訪問數']
    ).properties(title="📈 訪問趨勢圖", width=500)

    st.altair_chart(chart, use_container_width=True)
    st.dataframe(df)