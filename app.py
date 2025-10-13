import streamlit as st
import json
import random
from pathlib import Path

# === 頁面設定 ===
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)

# === 載入 CSS ===
def load_css():
    css_path = Path("style.css")
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === 載入 JSON ===
@st.cache_data
def load_data():
    path = Path("chakras_affirmations.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
load_css()

# === 顯示 Logo 與標題 ===
logo_path = Path("file/shop_logo.png")
logo_html = f'<img src="{logo_path.as_posix()}" class="logo" alt="Soul Heart Dance Logo">' if logo_path.exists() else ""

st.markdown(f"""
<div class="header">
    {logo_html}
    <div class="title-container">
        <div class="title-line1">Soul Heart Dance</div>
        <div class="title-line2">七脈輪靈魂共振卡</div>
    </div>
</div>
""", unsafe_allow_html=True)

# === 初始化狀態 ===
if "drawn" not in st.session_state:
    st.session_state.drawn = False
    st.session_state.button_label = "🔮 抽卡"
    st.session_state.card = None
    st.session_state.chakra = None
    st.session_state.seed = ""
    st.session_state.chakra_class = ""

# === 抽卡邏輯 ===
def draw_card():
    chakra = random.choice(list(data.keys()))
    info = data[chakra]
    seed = info.get("seed", "")
    cards = info.get("cards", [])
    if not cards:
        return None, None, "", ""
    card = random.choice(cards)
    chakra_class = info.get("class", "root-glow")
    return chakra, card, seed, chakra_class

# === 抽卡區 ===
st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

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
            st.rerun()

# === 顯示抽卡結果 ===
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
        <h3 class="chakra-title">🌈 {chakra.split('（')[0]} {seed}（{chakra.split('（')[1]}</h3>
        <div class="sentence">{sentence}</div>
        <div class="angel">天使數字：{angel_number}</div>
        <div class="meaning">{angel_meaning}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p class='hint-text'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# === 頁尾 ===
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)