import streamlit as st
import pandas as pd
import altair as alt
from counter_utils import load_counter

def render_admin_report():
    """Sara 專用後台統計畫面"""
    st.title("📊 七脈輪靈魂共振卡｜訪問統計報表")

    try:
        data = load_counter()
        if not data or not data.get("dates"):
            st.info("目前尚無訪問資料 🌙")
            return

        # 將資料轉成 DataFrame
        df = pd.DataFrame(list(data["dates"].items()), columns=["日期", "訪問數"])

        # 顯示統計表格
        st.dataframe(df, use_container_width=True)

        # 折線圖
        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(x="日期", y="訪問數")
            .properties(title="每日訪問趨勢")
        )
        st.altair_chart(chart, use_container_width=True)

        st.markdown(f"🌕 累積訪問次數：**{data['total']}**")

    except Exception as e:
        st.error(f"⚠️ 無法載入報表資料：{e}")