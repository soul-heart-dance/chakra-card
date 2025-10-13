import json
import random
import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)

# 載入 CSS
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 載入 JSON
@st.cache_data
def load_data():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
load_css()

# Chakra 對應設定
chakra_info = {
    "菈莯（海底輪）": {"seed": "Lam", "class": "root-glow"},
    "薇莯（臍輪）": {"seed": "Vam", "class": "sacral-glow"},
    "蕊莯（太陽神經叢輪）": {"seed": "Ram", "class": "solar-glow"},
    "芽莯（心輪）": {"seed": "Yam", "class": "heart-glow"},
    "哈莯（喉輪）": {"seed": "Ham", "class": "throat-glow"},
    "歐莯（眉心輪）": {"seed": "Om", "class": "third-glow"},
    "奧莯（頂輪）": {"seed": "Aum", "class": "crown-glow"},
}

# 標題與 Logo
logo_html = '<img src="file/shop_logo.png" alt="Soul Heart Dance Logo">'
st.markdown(f"""
<div class="header">
  <div class="logo-container">{logo_html}</div>
  <div>
    <div class="title-line1">Soul Heart Dance</div>
    <div class="title-line2">七脈輪靈魂共振卡</div>
  </div>
</div>
""", unsafe_allow_html=True)

# 初始化狀態
for key, value in {
    "drawn": False,
    "card": None,
    "chakra": None,
    "chakra_class": "",
    "seed": "",
    "button_label": "🔮 抽卡"
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# 抽卡邏輯
def draw_card():
    if isinstance(data, list):
        card = random.choice(data)
        chakra = card.get("chakra", "未知脈輪")
    elif isinstance(data, dict):
        chakra = random.choice(list(data.keys()))
        card = random.choice(data[chakra])
    else:
        raise ValueError("chakras_affirmations.json 格式錯誤")

    info = chakra_info.get(chakra, {})
    seed = info.get("seed", "")
    chakra_class = info.get("class", "")
    return chakra, card, seed, chakra_class

# 抽卡按鈕
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    clicked = st.button(st.session_state.button_label, key="draw_button")

if clicked:
    chakra, card, seed, chakra_class = draw_card()
    st.session_state.update({
        "chakra": chakra,
        "card": card,
        "seed": seed,
        "chakra_class": chakra_class,
        "drawn": True,
        "button_label": "🌙 再抽一張"
    })
    st.experimental_rerun()

# 顯示結果
if st.session_state.drawn and st.session_state.card:
    chakra = st.session_state.chakra
    card = st.session_state.card
    chakra_class = st.session_state.chakra_class
    seed = st.session_state.seed

    sentence = card.get("sentence", "宇宙正在透過你傳遞訊息。")
    angel_num = card.get("angel_number", "1111")
    angel_mean = card.get("angel_meaning", "信任一切正在完美發生。")

    st.markdown(f"""
    <div class="card-container {chakra_class}">
        <h3 style="color:#FFD6F6; margin-top:0.8rem;">
            🌈 {chakra.split('（')[0]} {seed}（{chakra.split('（')[1]}
        </h3>
        <div class='sentence'>{sentence}</div>
        <div class='angel'>🪽 天使數字：{angel_num}</div>
        <div class='meaning'>✨ {angel_mean}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align:center;color:#FFE6F7;'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# 頁尾
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)