import json
import random
import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪共振卡",
    page_icon="🔮",
    layout="centered"
)

# 黑色柔光背景 CSS
def set_background():
    st.markdown("""
        <style>
            .stApp {
                background: radial-gradient(circle at 30% 30%, #1b1b1b 0%, #000000 100%);
                text-align: center;
                font-family: "Noto Sans TC", sans-serif;
                color: #FFE6F7;
            }
            .header {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 0.8rem;
                margin-top: 1rem;
                margin-bottom: 1.5rem;
                animation: fadeIn 2s ease-in;
            }
            .header img {
                width: 60px;
                height: 60px;
                border-radius: 12px;
                box-shadow: 0 0 10px rgba(255, 214, 246, 0.3);
            }
            .header h1 {
                font-size: 1.5rem;
                font-weight: 600;
                color: #FFE6F7;
                letter-spacing: 0.03em;
            }
            .sentence {
                font-size: 1.2rem;
                background: rgba(255, 255, 255, 0.08);
                color: #fff;
                padding: 1rem 1.2rem;
                border-radius: 1rem;
                margin: 1.5rem auto;
                display: inline-block;
                box-shadow: 0 0 15px rgba(255, 192, 203, 0.25);
                backdrop-filter: blur(4px);
                animation: fadeIn 1.5s ease-in;
            }
            .angel, .meaning {
                font-size: 1.1rem;
                color: #FFE6F7;
                margin-top: 0.6rem;
                animation: fadeIn 2s ease-in;
            }
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(10px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            .footer {
                font-size: 0.95rem;
                color: #FFE6F7;
                margin-top: 2rem;
                padding-bottom: 1rem;
                opacity: 0.8;
                letter-spacing: 0.02em;
            }
            h4 {
                color: #FFE6F7;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

# 載入資料
with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

set_background()

# ✅ 使用 Hugging Face 圖片 URL
logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"

st.markdown(f"""
<div class="header">
    <img src="{logo_url}" alt="Soul Heart Dance Logo">
    <h1>Soul Heart Dance｜七脈輪共振卡</h1>
</div>
""", unsafe_allow_html=True)

# 狀態管理
if "drawn" not in st.session_state:
    st.session_state.drawn = False

button_label = "🔮 抽卡" if not st.session_state.drawn else "🌙 再抽一張"

st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(button_label, use_container_width=True):
        chakra = random.choice(list(data.keys()))
        card = random.choice(data[chakra])
        st.session_state.drawn = True

        st.markdown(f"<h3 style='color:#FFD6F6; margin-top:1.2rem;'>🌈 {chakra}</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='sentence'>💭 {card['sentence']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='angel'>🪽 天使數字：{card['angel_number']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='meaning'>✨ {card['angel_meaning']}</div>", unsafe_allow_html=True)

if not st.session_state.drawn:
    st.markdown("<p style='text-align:center;color:#FFE6F7;'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)