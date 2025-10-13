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
if "shine_toggle" not in st.session_state:
    st.session_state.shine_toggle = False  # 用來切換動畫類名
if "has_drawn_once" not in st.session_state:
    st.session_state.has_drawn_once = False

# -------------------------
# Header
# -------------------------
logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"
st.markdown(
    f"""
<div class="header">
  <img src="{logo_url}" alt="Soul Heart Dance Logo" class="logo">
  <div class="title">
    <div class="title-line1">Soul Heart Dance</div>
    <div class="title-line2">七脈輪靈魂共振卡</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# -------------------------
# 抽卡按鈕（key 固定、置中）
# -------------------------
button_label = "🔮 抽卡" if not st.session_state.has_drawn_once else "🌙 再抽一張"
st.markdown('<div class="cta">', unsafe_allow_html=True)
clicked = st.button(button_label, key="draw_button_fixed")
st.markdown('</div>', unsafe_allow_html=True)

# 抽卡動作
if clicked:
    chakra = random.choice(list(data.keys()))
    meta = data[chakra]
    card = random.choice(meta["cards"])

    st.session_state.current_card = {
        "name": chakra,                 # 例：芽莯（心輪）
        "seed": meta["seed"],           # 例：Yam
        "color": meta["color"],         # 例：#90EE90
        "glow": meta["class"],          # 例：heart-glow
        "sentence": card["sentence"],
        "angel_number": card["angel_number"],
        "angel_meaning": card["angel_meaning"],
    }

    # 固定按鈕 key，改用切換類名來重啟動畫
    st.session_state.shine_toggle = not st.session_state.shine_toggle
    st.session_state.has_drawn_once = True

# -------------------------
# 顯示卡片
# -------------------------
if st.session_state.current_card:
    c = st.session_state.current_card
    # 兩個互斥類名，切換就會重新跑動畫
    shine_class = "shineA" if st.session_state.shine_toggle else "shineB"

    st.markdown(
        f"""
<div class="card-wrapper {c['glow']} {shine_class}">
  <div class="card-container">
    <h3 style="color:{c['color']}">🌈 {c['name']} {c['seed']}</h3>
    <div class="sentence">{c['sentence']}</div>
    <div class="angel">🪽 天使數字：{c['angel_number']}</div>
    <div class="meaning">✨ {c['angel_meaning']}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.markdown("<p class='hint'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------
st.markdown(
    """
<div class="footer">© 2025 Soul Heart Dance · 與靈魂之心共舞</div>
""",
    unsafe_allow_html=True,
)