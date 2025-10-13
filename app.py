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

# ---------- 狀態 ----------
if "draw_count" not in st.session_state:
    st.session_state.draw_count = 0
if "card_html" not in st.session_state:
    st.session_state.card_html = None

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

# ---------- 抽卡按鈕 ----------
button_text = "🔮 抽卡" if st.session_state.draw_count == 0 else "🌙 再抽一張"

st.markdown('<div class="button-center">', unsafe_allow_html=True)
clicked = st.button(button_text)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- 抽卡邏輯 ----------
if clicked:
    st.session_state.draw_count += 1
    chakra = random.choice(list(data.keys()))
    meta = data[chakra]
    card = random.choice(meta["cards"])

    # 為每次抽卡產生新的 UUID → 強制 DOM 重建
    unique_id = str(uuid.uuid4())

    st.session_state.card_html = f"""
    <div class="card-wrapper {meta['class']}" id="{unique_id}">
        <div class="card-container animate">
            <h3 style="color:{meta['color']}">🌈 {chakra} {meta['seed']}</h3>
            <div class="sentence">{card['sentence']}</div>
            <div class="angel">🪽 天使數字：{card['angel_number']}</div>
            <div class="meaning">✨ {card['angel_meaning']}</div>
        </div>
    </div>
    """

# ---------- 顯示卡片 ----------
if st.session_state.card_html:
    st.markdown(st.session_state.card_html, unsafe_allow_html=True)
else:
    st.markdown("<p class='hint'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)