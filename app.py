import json
import random
import streamlit as st
import uuid

st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)

# ---------- 載入資料與樣式 ----------
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

# ---------- 初始化 ----------
if "card" not in st.session_state:
    st.session_state.card = None
if "anim_class" not in st.session_state:
    st.session_state.anim_class = "shineA"

# ---------- Header ----------
logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"
st.markdown(f"""
<div class="header">
  <img src="{logo_url}" class="logo" alt="Soul Heart Dance Logo">
  <div class="title">
    <div class="title-line1">Soul Heart Dance</div>
    <div class="title-line2">七脈輪靈魂共振卡</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- 抽卡邏輯 ----------
def draw_card():
    chakra = random.choice(list(data.keys()))
    meta = data[chakra]
    card = random.choice(meta["cards"])
    # 每次抽卡切換動畫 class，強制重播動畫
    st.session_state.anim_class = "shineB" if st.session_state.anim_class == "shineA" else "shineA"
    st.session_state.card = {
        "chakra": chakra,
        "seed": meta["seed"],
        "color": meta["color"],
        "glow": meta["class"],
        "sentence": card["sentence"],
        "angel_number": card["angel_number"],
        "angel_meaning": card["angel_meaning"],
        "uid": str(uuid.uuid4()),
        "anim": st.session_state.anim_class
    }

# ---------- 按鈕 ----------
button_text = "🔮 抽卡" if st.session_state.card is None else "🌙 再抽一張"
st.markdown('<div class="button-center">', unsafe_allow_html=True)
st.button(button_text, on_click=draw_card, key="draw_button")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- 顯示卡片 ----------
if st.session_state.card:
    c = st.session_state.card
    st.markdown(f"""
    <div class="card-wrapper {c['glow']} {c['anim']}" id="{c['uid']}">
        <div class="card-container">
            <h3 style="color:{c['color']}">🌈 {c['chakra']} {c['seed']}</h3>
            <div class="sentence">{c['sentence']}</div>
            <div class="angel">🪽 天使數字：{c['angel_number']}</div>
            <div class="meaning">✨ {c['angel_meaning']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p class='hint'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)