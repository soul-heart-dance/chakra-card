import json
import random
import streamlit as st
from PIL import Image
import os

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪共振卡",
    page_icon="🔮",
    layout="centered"
)

# 取得 logo 網址（直接從 Hugging Face repo 載入）
logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"

# 黑色柔光背景＋發光按鈕樣式
def set_background():
    st.markdown("""
        <style>
            .stApp {
                background: radial-gradient(circle at 30% 30%, #1b1b1b 0%, #000000 100%);
                text-align: center;
                font-family: "Noto Sans TC", sans-serif;
                color: #FFE6F7;
                background-size: 400% 400%;
                animation: gradientFlow 12s ease infinite;
            }

            @keyframes gradientFlow {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* --- 頁首 logo + 標題 --- */
            .header {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                margin-top: 1rem;
                margin-bottom: 1rem;
                animation: fadeIn 2s ease;
            }
            .header img {
                width: 70px;
                height: 70px;
                border-radius: 10px;
                margin-bottom: 0.5rem;
                animation: fadeIn 2s ease-in;
            }
            .header h1 {
                font-size: 1.5rem;
                font-weight: 600;
                color: #FFE6F7;
                letter-spacing: 0.05em;
                margin: 0;
            }

            /* --- 抽卡按鈕 --- */
            div.stButton > button:first-child {
                display: block;
                margin: 1.5rem auto;
                background-color: #FFE6F7 !important;
                color: #000 !important;
                font-size: 1.1rem !important;
                border-radius: 10px !important;
                border: none !important;
                box-shadow: 0 0 15px rgba(255, 192, 203, 0.4);
                transition: all 0.3s ease;
            }
            div.stButton > button:hover {
                transform: scale(1.05);
                box-shadow: 0 0 20px rgba(255, 192, 203, 0.7);
            }

            /* --- 文字動畫 --- */
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(10px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            /* --- 底部文字 --- */
            .footer {
                font-size: 0.95rem;
                color: #FFE6F7;
                margin-top: 2rem;
                padding-bottom: 1rem;
                letter-spacing: 0.02em;
                opacity: 0.9;
            }
        </style>
    """, unsafe_allow_html=True)

# 套用背景
set_background()

# 載入資料
with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 頁首（品牌 logo + 標題）
with st.container():
    st.markdown(f"""
    <div class="header">
        <img src="{logo_url}" alt="Soul Heart Dance Logo" width="70">
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