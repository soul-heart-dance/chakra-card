import json
import random
import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪共振卡",
    page_icon="🔮",
    layout="centered"
)

# 黑色柔光背景 + 星光動態 logo + 優雅字體
def set_background():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Noto+Sans+TC:wght@400;500&display=swap');

            body {
                margin: 0;
                overflow-x: hidden;
                background-color: #000;
            }

            .stApp {
                background: radial-gradient(circle at 30% 30%, #1b1b1b 0%, #000000 100%);
                text-align: center;
                font-family: 'Noto Sans TC', sans-serif;
                color: #FFE6F7;
                animation: fadeIn 2.5s ease-in forwards;
            }

            /* Logo 星光緩慢亮起 */
            .logo-container {
                position: relative;
                width: 70px;
                height: 70px;
                border-radius: 50%;
                overflow: hidden;
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0 0 20px rgba(255, 214, 246, 0.2);
                animation: glowIn 3s ease-in-out forwards;
            }

            .logo-container img {
                width: 100%;
                height: 100%;
                border-radius: 50%;
                opacity: 0;
                animation: logoFade 4s ease-in-out forwards;
            }

            @keyframes logoFade {
                0% { opacity: 0; filter: brightness(0.5) blur(3px); }
                60% { opacity: 0.8; filter: brightness(1.2) blur(1px); }
                100% { opacity: 1; filter: brightness(1) blur(0); }
            }

            @keyframes glowIn {
                0% { box-shadow: 0 0 0px rgba(255, 214, 246, 0.1); }
                100% { box-shadow: 0 0 18px rgba(255, 214, 246, 0.6); }
            }

            /* 標題漸入與分行設計 */
            .header {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 0.8rem;
                flex-wrap: wrap;
                margin-top: 1.2rem;
                margin-bottom: 2rem;
                animation: fadeInUp 3s ease-in;
            }

            .title-line1 {
                font-family: 'Cormorant Garamond', serif;
                font-size: 1.7rem;
                font-weight: 600;
                color: #FFE6F7;
                letter-spacing: 0.05em;
                opacity: 0;
                animation: textGlow 3s ease-in-out 1s forwards;
            }

            .title-line2 {
                font-family: 'Noto Sans TC', sans-serif;
                font-size: 1.2rem;
                font-weight: 500;
                color: #FFD6F6;
                letter-spacing: 0.05em;
                opacity: 0;
                animation: textGlow 3s ease-in-out 1.5s forwards;
            }

            @keyframes textGlow {
                0% { opacity: 0; text-shadow: none; }
                100% { opacity: 1; text-shadow: 0 0 12px rgba(255, 214, 246, 0.5); }
            }

            @keyframes fadeInUp {
                0% { opacity: 0; transform: translateY(20px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            /* 卡片與內容 */
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

            /* 按鈕樣式 */
            div.stButton > button {
                background-color: #1c1c1e !important;
                color: #FFD6F6 !important;
                border: 1px solid #FFD6F6 !important;
                border-radius: 10px !important;
                font-size: 1.1rem !important;
                padding: 0.6rem 1.2rem !important;
                box-shadow: 0 0 10px rgba(255, 214, 246, 0.3);
                transition: all 0.3s ease-in-out;
            }

            div.stButton > button:hover {
                background-color: #FFD6F6 !important;
                color: #000 !important;
                transform: scale(1.03);
                box-shadow: 0 0 15px rgba(255, 214, 246, 0.6);
            }

            .footer {
                font-size: 0.9rem;
                color: #FFE6F7;
                margin-top: 2rem;
                padding-bottom: 1rem;
                opacity: 0.8;
                letter-spacing: 0.03em;
                animation: fadeIn 4s ease-in;
            }

            h4 {
                color: #FFE6F7;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

# 套用背景
set_background()

# 載入靈魂訊息資料
with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# logo 網址
logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"

# 頁首 - 星光 logo + 標題
st.markdown(f"""
<div class="header">
    <div class="logo-container">
        <img src="{logo_url}" alt="Soul Heart Dance Logo">
    </div>
    <div>
        <div class="title-line1">Soul Heart Dance</div>
        <div class="title-line2">七脈輪共振卡</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 狀態管理
if "drawn" not in st.session_state:
    st.session_state.drawn = False

button_label = "🔮 抽卡" if not st.session_state.drawn else "🌙 再抽一張"

st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# 抽卡按鈕
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

# 初始提示
if not st.session_state.drawn:
    st.markdown("<p style='text-align:center;color:#FFE6F7;'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# 底部簽名
st.markdown("""
<div class="footer">
    © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)