import streamlit as st
from counter_utils import update_counter
from datetime import datetime
import os
import json

# ----------- 頁面設定 -----------
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)

# ----------- 訪問記錄 -----------
counter_data = update_counter()

# ----------- 判斷是否為管理者 -----------
qp = st.query_params.to_dict()
is_admin = qp.get("sara") in ("1", ["1"])

# ----------- 動態載入對應頁面 -----------
if is_admin:
    from pages.admin_report import show_admin_report
    show_admin_report(counter_data)
else:
    from pages.chakra_draw import show_chakra_draw
    show_chakra_draw(counter_data)

# ----------- Footer -----------
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)