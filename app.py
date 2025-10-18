import streamlit as st
from pages.chakra_card import render_chakra_card
from pages.admin_report import render_admin_report

st.set_page_config(page_title="Soul Heart Dance｜七脈輪靈魂共振卡", page_icon="🔮", layout="centered")

q = st.query_params
sara = q.get("sara", ["0"])[0]
page = q.get("page", ["card"])[0]

if sara == "1":
    render_admin_report()
elif page == "admin":
    st.error("🚫 沒有權限訪問此頁面。")
else:
    render_chakra_card()