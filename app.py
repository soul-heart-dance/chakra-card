import json
import random
import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪共振卡",
    page_icon="🔮",
    layout="centered"
)

# 固定黑色柔光背景
def set_background():
    st.markdown("""
        <style>
            .stApp {
                background: radial-gradient(circle at 30% 30%, #1b1b1b 0%, #000000 100%);
                color: #FFE6F7;
                font-family: "Noto Sans TC", sans-serif;
                text-align: center;
            }
            .header {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 0.8rem;
                margin-top: 1rem;
                margin-bottom: 1.5rem;
            }
            .header img {
                width: 60px;
                height: 60px;
                object-fit: contain;
                filter: brightness(1.2);
            }
            .header h1 {
                font-size: 1.6rem;
                font-weight: 600;
                color: #FFE6F7;
                letter-spacing: 0.03em;
            }
            .sentence {
                font-size: 1.3rem;
                background: rgba(255, 255, 255, 0.1);
                color: #fff;
                padding: 1rem 1.5rem;
                border-radius: 0.8rem;
                margin: 1.2rem auto;
                display: inline-block;
                font-weight: 500;
                box-shadow: 0 0 15px rgba(255, 192, 203, 0.3);
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
                letter-spacing: 0.02em;
                opacity: 0.9;
            }
            div[data-testid="stButton"] {
                display: flex;
                justify-content: center;
            }
            button[kind="primary"] {
                background-color: #FFD6F6 !important;
                color: #000 !important;
                font-size: 1.1rem !important;
                border-radius: 8px !important;
                border: none !important;
                padding: 0.4rem 1.2rem !important;
            }
            h4 {
                color: #FFE6F7;
            }
        </style>
    """, unsafe_allow_html=True)

# 套用背景
set_background()

# 載入資料
with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 頁首（品牌 logo + 標題）
st.markdown("""
<div class="header">
    <img src="shop_logo.png" alt="Soul Heart Dance Logo">
    <h1>Soul Heart Dance｜七脈輪共振卡</h1>
</div>
""", unsafe_allow_html=True)

# 抽卡按鈕
st.markdown("<h4>✨ 抽一張今日共振能量 ✨</h4>", unsafe_allow_html=True)

if st.button("🔮 抽卡"):
    chakra = random.choice(list(data.keys()))
    card = random.choice(data[chakra])

    st.markdown(f"<div class='sentence'>💭 {card['sentence']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='angel'>🪽 天使數字：{card['angel_number']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='meaning'>✨ {card['angel_meaning']}</div>", unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align:center;color:#FFE6F7;'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# 底部簽名
st.markdown("""
<div class="footer">
    © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)