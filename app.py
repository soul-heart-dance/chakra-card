import json
import random
import streamlit as st
from pathlib import Path

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)

# 載入 CSS 樣式
def load_css():
    css_path = Path("style.css")
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 載入 JSON 資料
@st.cache_data
def load_data():
    data_path = Path("chakras_affirmations.json")
    if data_path.exists():
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.error("找不到 chakras_affirmations.json 檔案。")
        return {}

data = load_data()
load_css()

# 標題與 logo
logo_path = Path("file/shop_logo.png")
if logo_path.exists():
    st.markdown(f"""
    <div class="header">
        <img src="file/shop_logo.png" alt="Soul Heart Dance Logo" class="logo">
        <div class="title-container">
            <div class="title-line1">Soul Heart Dance</div>
            <div class="title-line2">七脈輪靈魂共振卡</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="header">
        <div class="title-container">
            <div class="title-line1">Soul Heart Dance</div>
            <div class="title-line2">七脈輪靈魂共振卡</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 初始化狀態
if "drawn" not in st.session_state:
    st.session_state.drawn = False
    st.session_state.button_label = "🔮 抽卡"
    st.session_state.card = None
    st.session_state.chakra = None
    st.session_state.seed = ""
    st.session_state.chakra_class = ""

# 抽卡邏輯
def draw_card():
    chakra = random.choice(list(data.keys()))
    chakra_data = data[chakra]
    seed = chakra_data.get("seed", "")
    cards = chakra_data.get("cards", [])
    if not cards:
        st.error(f"{chakra} 沒有可用卡片資料。")
        return None, None, "", ""
    card = random.choice(cards)

    chakra_class = chakra.replace("（", "").split("）")[0]  # 用於光圈 class
    return chakra, card, seed, chakra_class

# 顯示提示文字
st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# 抽卡按鈕置中
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(st.session_state.button_label, use_container_width=True):
        chakra, card, seed, chakra_class = draw_card()
        if card:
            st.session_state.drawn = True
            st.session_state.button_label = "🌙 再抽一張"
            st.session_state.card = card
            st.session_state.chakra = chakra
            st.session_state.seed = seed
            st.session_state.chakra_class = chakra_class
            st.experimental_rerun()

# 顯示抽卡結果
if st.session_state.drawn and st.session_state.card:
    chakra = st.session_state.chakra
    card = st.session_state.card
    seed = st.session_state.seed
    chakra_class = st.session_state.chakra_class

    sentence = card.get("sentence", "宇宙正在透過你傳遞訊息。")
    angel_number = card.get("angel_number", "")
    angel_meaning = card.get("angel_meaning", "")

    st.markdown(f"""
    <div class="card-container {chakra_class}">
        <h3 style="color:#FFD6F6; margin-top:0.8rem;">
            🌈 {chakra.split('（')[0]} {seed}（{chakra.split('（')[1]}
        </h3>
        <div class="sentence">{sentence}</div>
        <div class="angel">天使數字：{angel_number}</div>
        <div class="meaning">{angel_meaning}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align:center;color:#FFE6F7;'>點擊上方按鈕開始抽卡</p>", unsafe_allow_html=True)

# 頁尾
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)