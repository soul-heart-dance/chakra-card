import json
import random
import base64
from pathlib import Path
import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)

# CSS 樣式載入
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 載入 JSON 資料
@st.cache_data
def load_data():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
load_css()

# 讀取 logo 並轉 base64
def get_base64_image(image_path):
    image = Path(image_path)
    if image.exists():
        return base64.b64encode(image.read_bytes()).decode()
    return None

logo_base64 = get_base64_image("shop_logo.png")

# chakra 對應種子音與光暈 class
chakra_info = {
    "菈莯（海底輪）": {"seed": "Lam", "class": "root-glow"},
    "薇莯（臍輪）": {"seed": "Vam", "class": "sacral-glow"},
    "蕊莯（太陽神經叢輪）": {"seed": "Ram", "class": "solar-glow"},
    "芽莯（心輪）": {"seed": "Yam", "class": "heart-glow"},
    "哈莯（喉輪）": {"seed": "Ham", "class": "throat-glow"},
    "歐莯（眉心輪）": {"seed": "Om", "class": "third-glow"},
    "奧莯（頂輪）": {"seed": "Aum", "class": "crown-glow"},
}

# 頁首 Logo + 標題
st.markdown("""
<div class="header">
    <div class="logo-container">
        <img src="data:image/png;base64,{}" alt="Soul Heart Dance Logo">
    </div>
    <div>
        <div class="title-line1">Soul Heart Dance</div>
        <div class="title-line2">七脈輪靈魂共振卡</div>
    </div>
</div>
""".format(logo_base64 if logo_base64 else ""), unsafe_allow_html=True)

# Session 狀態
if "drawn" not in st.session_state:
    st.session_state.drawn = False
if "card" not in st.session_state:
    st.session_state.card = None
if "chakra" not in st.session_state:
    st.session_state.chakra = None
if "chakra_class" not in st.session_state:
    st.session_state.chakra_class = ""
if "button_label" not in st.session_state:
    st.session_state.button_label = "🔮 抽卡"

# 標題
st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# 抽卡邏輯
def draw_card():
    chakra = random.choice(list(data.keys()))
    card = random.choice(data[chakra])
    chakra_class = chakra_info.get(chakra, {}).get("class", "")
    seed_sound = chakra_info.get(chakra, {}).get("seed", "")
    return chakra, card, chakra_class, seed_sound

# 按鈕區
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(st.session_state.button_label, key="draw_button"):
        chakra, card, chakra_class, seed_sound = draw_card()
        st.session_state.chakra = chakra
        st.session_state.card = card
        st.session_state.chakra_class = chakra_class
        st.session_state.seed_sound = seed_sound
        st.session_state.drawn = True
        st.session_state.button_label = "🌙 再抽一張"
        st.rerun()  # 即時更新按鈕文字

# 顯示結果
if st.session_state.drawn and st.session_state.card:
    chakra = st.session_state.chakra
    card = st.session_state.card
    chakra_class = st.session_state.chakra_class
    seed_sound = st.session_state.seed_sound

    st.markdown(
        f"""
        <div class="card-container {chakra_class}">
            <h3 style="color:#FFD6F6; margin-top:0.8rem;">
                🌈 {chakra.split('（')[0]} {seed_sound}（{chakra.split('（')[1]}
            </h3>
            <div class='sentence'>{card['sentence']}</div>
            <div class='angel'>🪽 天使數字：{card['angel_number']}</div>
            <div class='meaning'>✨ {card['angel_meaning']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("<p style='text-align:center;color:#FFE6F7;'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# 頁尾
st.markdown("""
<div class="footer">
    © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)