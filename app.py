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

# CSS 載入
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
load_css()

# 轉 Base64 Logo
def get_base64_image(image_path):
    path = Path(image_path)
    if not path.exists():
        return None
    return base64.b64encode(path.read_bytes()).decode("utf-8")

logo_base64 = get_base64_image("shop_logo.png")

# 脈輪設定
chakra_info = {
    "菈莯（海底輪）": {"seed": "Lam", "class": "root-glow"},
    "薇莯（臍輪）": {"seed": "Vam", "class": "sacral-glow"},
    "蕊莯（太陽神經叢輪）": {"seed": "Ram", "class": "solar-glow"},
    "芽莯（心輪）": {"seed": "Yam", "class": "heart-glow"},
    "哈莯（喉輪）": {"seed": "Ham", "class": "throat-glow"},
    "歐莯（眉心輪）": {"seed": "Om", "class": "third-glow"},
    "奧莯（頂輪）": {"seed": "Aum", "class": "crown-glow"},
}

# 標題區
logo_html = (
    f'<img src="data:image/png;base64,{logo_base64}" alt="logo">'
    if logo_base64
    else ""
)

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
if "drawn" not in st.session_state:
    st.session_state.drawn = False
if "card" not in st.session_state:
    st.session_state.card = None
if "chakra" not in st.session_state:
    st.session_state.chakra = None
if "class" not in st.session_state:
    st.session_state.class_ = ""
if "seed" not in st.session_state:
    st.session_state.seed = ""
if "button_label" not in st.session_state:
    st.session_state.button_label = "🔮 抽卡"

# 標題文字
st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# 抽卡邏輯
def draw_card():
    # 若 data 是 list，就隨機挑一個 dict
    if isinstance(data, list):
        chosen = random.choice(data)
        chakra = chosen.get("chakra", "未知")
        card = chosen
    else:
        chakra = random.choice(list(data.keys()))
        card = random.choice(data[chakra])
    seed = chakra_info.get(chakra, {}).get("seed", "")
    chakra_class = chakra_info.get(chakra, {}).get("class", "")
    return chakra, card, seed, chakra_class

# 按鈕區
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    clicked = st.button(st.session_state.button_label, key="draw_button")

if clicked:
    chakra, card, seed, chakra_class = draw_card()
    st.session_state.chakra = chakra
    st.session_state.card = card
    st.session_state.seed = seed
    st.session_state.class_ = chakra_class
    st.session_state.drawn = True
    st.session_state.button_label = "🌙 再抽一張"
    st.rerun()

# 顯示抽卡結果
if st.session_state.drawn and st.session_state.card:
    chakra = st.session_state.chakra
    card = st.session_state.card
    chakra_class = st.session_state.class_
    seed = st.session_state.seed

    # 防呆：若 key 不存在就給預設值
    sentence = card.get("sentence", "💫 宇宙正在對你說話，請傾聽內心的聲音。")
    angel_num = card.get("angel_number", "1111")
    angel_mean = card.get("angel_meaning", "信任宇宙的完美時機。")

    st.markdown(
        f"""
        <div class="card-container {chakra_class}">
            <h3 style="color:#FFD6F6; margin-top:0.8rem;">
                🌈 {chakra.split('（')[0]} {seed}（{chakra.split('（')[1]}
            </h3>
            <div class='sentence'>{sentence}</div>
            <div class='angel'>🪽 天使數字：{angel_num}</div>
            <div class='meaning'>✨ {angel_mean}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<p style='text-align:center;color:#FFE6F7;'>🌙 點擊上方按鈕開始抽卡 🌙</p>",
        unsafe_allow_html=True,
    )

# 頁尾
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)