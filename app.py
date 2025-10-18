import streamlit as st
from pages.chakra_card import render_chakra_card
from pages.admin_report import render_admin_report

# --- 頁面設定 ---
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"  # 隱藏左側 sidebar
)

# --- 載入全域 CSS ---
with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- 依網址參數決定頁面 ---
query_params = st.query_params
sara_key = query_params.get("sara", ["0"])[0]

if sara_key == "1":
    render_admin_report()
else:
    render_chakra_card()