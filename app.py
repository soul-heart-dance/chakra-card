import json, random, streamlit as st

st.set_page_config(page_title="Soul Heart Dance｜七脈輪共振卡", page_icon="🔮", layout="centered")

@st.cache_data
def load_data():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

def draw_card():
    chakra = random.choice(list(data.keys()))
    card = random.choice(data[chakra])
    return chakra, card

st.markdown(open("style.css").read(), unsafe_allow_html=True)

logo = "shop_logo.png"
st.markdown(f"""
<div class="header">
  <div class="logo-container"><img src="{logo}"></div>
  <div>
    <div class="title-line1">Soul Heart Dance</div>
    <div class="title-line2">七脈輪共振卡</div>
  </div>
</div>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    btn = st.button("🌙 再抽一張" if st.session_state.result else "🔮 抽卡", use_container_width=True)
if btn:
    st.session_state.result = draw_card()

if st.session_state.result:
    chakra, card = st.session_state.result
    st.markdown(f"""
        <div class="card-container active">
            <h3>🌈 {chakra}</h3>
            <div class='sentence'>💭 {card['sentence']}</div>
            <div class='angel'>🪽 天使數字：{card['angel_number']}</div>
            <div class='meaning'>✨ {card['angel_meaning']}</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

st.markdown("<div class='footer'>© 2025 Soul Heart Dance · 與靈魂之心共舞</div>", unsafe_allow_html=True)