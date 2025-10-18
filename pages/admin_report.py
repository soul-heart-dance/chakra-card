import streamlit as st
import pandas as pd
from counter_utils import fetch_report

def render_admin_report():
    st.markdown("<style>.stApp{color:#FFE6F7;}</style>", unsafe_allow_html=True)
    st.title("📊 訪問統計（管理者）")

    try:
        data = fetch_report()
    except Exception as e:
        st.error(f"讀取統計資料失敗：{e}")
        return

    st.markdown(
        f"**今日訪問**：{data['today']}　|　**累積訪問**：{data['total']}"
    )

    rows = data["rows"]
    if not rows:
        st.info("目前還沒有資料。")
        return

    df = pd.DataFrame(rows, columns=["日期", "訪問數", "累積訪問"])
    st.dataframe(df, use_container_width=True)

    # 簡單折線圖（使用 Streamlit 內建）
    st.line_chart(df.set_index("日期")[["訪問數","累積訪問"]])