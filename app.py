import streamlit as st
from pages.chakra_card import render_chakra_card
from pages.admin_report import render_admin_report

# 頁面基本設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered",
)

# 使用新版 Streamlit API（沒有警告）
query_params = st.query_params
mode = query_params.get("page", ["card"])[0]
sara_key = query_params.get("sara", ["0"])[0]

# 路由控制
if sara_key == "1":
    render_admin_report()         # 管理者報表
elif mode == "admin":
    st.error("🚫 沒有權限訪問此頁面。")
else:
    render_chakra_card()          # 一般抽卡頁面