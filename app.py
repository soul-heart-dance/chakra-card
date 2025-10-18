import streamlit as st
from pages.chakra_card import render_chakra_card
from pages.admin_report import render_admin_report

# 頁面基本設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered",
)

# 取得網址參數
query_params = st.experimental_get_query_params()  # ✅ 改用舊版相容寫法
mode = query_params.get("page", ["card"])[0]
sara_key = query_params.get("sara", ["0"])[0]

# 路由控制
if sara_key == "1":
    # 管理者頁面（顯示統計報表）
    render_admin_report()
elif mode == "admin":
    # 非管理者禁止進入
    st.error("🚫 沒有權限訪問此頁面。")
else:
    # 一般訪客頁面（抽卡）
    render_chakra_card()