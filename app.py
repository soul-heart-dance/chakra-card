import streamlit as st
from pages.chakra_card import render_chakra_card
from pages.admin_report import render_admin_report
from pathlib import Path

# ---- 頁面設定 ----
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",  # 關閉側邊欄
)

# ---- 先插入 CSS （用 style 標籤覆蓋預設樣式）----
css_path = Path("style.css")
if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# ---- 插入 loader ----
st.markdown("""
<div id="loader">
  <div class="glow-circle"></div>
  <div class="loader-text">🌸 靈魂正在連線中...</div>
</div>
""", unsafe_allow_html=True)

# ---- 控制頁面 ----
query_params = st.query_params
mode = query_params.get("page", ["card"])[0]
sara_key = query_params.get("sara", ["0"])[0]

if sara_key == "1":
    render_admin_report()
elif mode == "admin":
    st.error("🚫 沒有權限訪問此頁面。")
else:
    render_chakra_card()