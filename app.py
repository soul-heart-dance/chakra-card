import json
import random
import streamlit as st

# -------------------------
# 頁面設定
# -------------------------
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)

# -------------------------
# 快取載入資料與樣式
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
# 初始化狀態
# -------------------------
if "current_card" not in st.session_state:
    st.session_state.current_card = None
if "shine_key" not in st.session_state:
    st.session_state.shine_key = 0

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
# 抽卡按鈕
# -------------------------
button_label = "🔮 抽卡" if not st.session_state.current_card else "🌙 再抽一張"
st.markdown("<div class='button-wrapper'>", unsafe_allow_html=True)
button_clicked = st.button(button_label, key=f"draw_button_{st.session_state.shine_key}")
st.markdown("</div>", unsafe_allow_html=True)

if button_clicked:
    chakra = random.choice(list(data.keys()))
    card = random.choice(data[chakra]["cards"])
    st.session_state.current_card = {
        "name": chakra,
        "seed": data[chakra]["seed"],
        "color": data[chakra]["color"],
        "class": data[chakra]["class"],
        "sentence": card["sentence"],
        "angel_number": card["angel_number"],
        "angel_meaning": card["angel_meaning"]
    }
    # 每次抽卡都換一個 key 讓卡片重新渲染動畫
    st.session_state.shine_key += 1

# -------------------------
# 顯示卡片
# -------------------------
if st.session_state.current_card:
    c = st.session_state.current_card
    glow_class = c["class"]

    st.markdown(f"""
    <div class="card-wrapper {glow_class} shine-on" key="{st.session_state.shine_key}">
        <div class="card-container">
            <h3 style="color:{c['color']}">🌈 {c['name']} {c['seed']}</h3>
            <div class="sentence">{c['sentence']}</div>
            <div class="angel">🪽 天使數字：{c['angel_number']}</div>
            <div class="meaning">✨ {c['angel_meaning']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
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