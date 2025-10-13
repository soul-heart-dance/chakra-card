import json
import random
import streamlit as st
import time
import uuid

# -------------------------
# 頁面設定
# -------------------------
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)

# -------------------------
# 快取載入
# -------------------------
@st.cache_data
def load_data():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        return f.read()

data = load_data()
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

# -------------------------
# 狀態初始化
# -------------------------
if "current_card" not in st.session_state:
    st.session_state.current_card = None
if "has_drawn" not in st.session_state:
    st.session_state.has_drawn = False
if "card_key" not in st.session_state:
    st.session_state.card_key = str(uuid.uuid4())

# -------------------------
# Header
# -------------------------
logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"
st.markdown(f"""
<div class="header">
  <img src="{logo_url}" alt="Soul Heart Dance Logo" class="logo">
  <div class="title">
    <div class="title-line1">Soul Heart Dance</div>
    <div class="title-line2">七脈輪靈魂共振卡</div>
  </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# 按鈕
# -------------------------
button_label = "🔮 抽卡" if not st.session_state.has_drawn else "🌙 再抽一張"

st.markdown('<div class="button-container">', unsafe_allow_html=True)
clicked = st.button(button_label, key="draw_button_fixed")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# 抽卡邏輯
# -------------------------
if clicked:
    st.session_state.has_drawn = True

    chakra = random.choice(list(data.keys()))
    meta = data[chakra]
    card = random.choice(meta["cards"])

    st.session_state.current_card = {
        "name": chakra,
        "seed": meta["seed"],
        "color": meta["color"],
        "glow": meta["class"],
        "sentence": card["sentence"],
        "angel_number": card["angel_number"],
        "angel_meaning": card["angel_meaning"]
    }

    # 每次抽卡都重新給一個新的 key，強制 DOM 重建（確保閃爍）
    st.session_state.card_key = str(uuid.uuid4())

# -------------------------
# 顯示卡片
# -------------------------
if st.session_state.current_card:
    c = st.session_state.current_card
    st.markdown(
        f"""
        <div class="card-wrapper {c['glow']}" id="{st.session_state.card_key}">
            <div class="card-container animate">
                <h3 style="color:{c['color']}">🌈 {c['name']} {c['seed']}</h3>
                <div class="sentence">{c['sentence']}</div>
                <div class="angel">🪽 天使數字：{c['angel_number']}</div>
                <div class="meaning">✨ {c['angel_meaning']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("<p class='hint'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------
st.markdown("""
<div class="footer">
    © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)