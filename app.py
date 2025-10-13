import json
import random
import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪共振卡",
    page_icon="🔮",
    layout="centered"
)

# 柔光背景與字體設定
def set_background():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Verdana&display=swap');

            .stApp {
                background: radial-gradient(circle at 30% 30%, #1b1b1b 0%, #000000 100%);
                text-align: center;
                font-family: "Microsoft JhengHei", Verdana, sans-serif;
                color: #FFE6F7;
            }

            /* Logo 柔光動畫 */
            .logo-container {
                width: 68px;
                height: 68px;
                border-radius: 50%;
                overflow: hidden;
                box-shadow: 0 0 18px rgba(255, 214, 246, 0.5);
                animation: glowPulse 4s ease-in-out infinite alternate;
            }

            .logo-container img {
                width: 100%;
                height: 100%;
                border-radius: 50%;
            }

            @keyframes glowPulse {
                0% { box-shadow: 0 0 10px rgba(255, 214, 246, 0.3); }
                100% { box-shadow: 0 0 20px rgba(255, 214, 246, 0.7); }
            }

            /* 標題 */
            .header {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                gap: 0.8rem;
                margin-top: 1.2rem;
                margin-bottom: 1.5rem;
            }

            .title-line1 {
                font-size: 1.6rem;
                font-weight: 600;
                color: #FFE6F7;
            }

            .title-line2 {
                font-size: 1.1rem;
                font-weight: 500;
                color: #FFD6F6;
            }

            /* 卡片外框容器（加流光） */
            .card-container {
                position: relative;
                margin-top: 2rem;
                background: rgba(255, 255, 255, 0.06);
                border-radius: 1.2rem;
                padding: 1.5rem;
                border: 1px solid rgba(255, 214, 246, 0.4);
                box-shadow: 0 0 20px rgba(255, 214, 246, 0.3);
                display: inline-block;
                overflow: hidden;
                animation: fadeInCard 1.2s ease-in-out;
            }

            /* 金粉能量流過動畫 */
            .card-container::before {
                content: "";
                position: absolute;
                top: 0;
                left: -75%;
                width: 50%;
                height: 100%;
                background: linear-gradient(120deg, rgba(255,255,255,0) 0%, rgba(255,220,250,0.6) 50%, rgba(255,255,255,0) 100%);
                animation: shimmer 3s ease-in-out forwards;
            }

            @keyframes shimmer {
                0% { left: -75%; opacity: 0; }
                20% { opacity: 1; }
                100% { left: 125%; opacity: 0; }
            }

            @keyframes fadeInCard {
                0% { opacity: 0; transform: translateY(20px) scale(0.95); }
                100% { opacity: 1; transform: translateY(0) scale(1); }
            }

            /* 內層訊息氣泡框 */
            .sentence {
                font-size: 1.2rem;
                background: rgba(255, 255, 255, 0.12);
                color: #fff;
                padding: 1rem 1.3rem;
                border-radius: 0.8rem;
                margin: 1rem auto;
                display: inline-block;
                box-shadow: 0 0 10px rgba(255, 192, 203, 0.2);
                backdrop-filter: blur(4px);
            }

            .angel, .meaning {
                font-size: 1.1rem;
                color: #FFE6F7;
                margin-top: 0.5rem;
            }

            /* 按鈕 */
            div.stButton > button {
                background-color: #FFD6F6 !important;
                color: #000 !important;
                font-size: 1.1rem !important;
                border-radius: 12px !important;
                border: none !important;
                box-shadow: 0 0 10px rgba(255, 214, 246, 0.5);
                transition: all 0.3s ease-in-out;
            }
            div.stButton > button:hover {
                transform: scale(1.05);
                box-shadow: 0 0 15px rgba(255, 214, 246, 0.8);
            }

            .footer {
                font-size: 0.9rem;
                color: #FFE6F7;
                margin-top: 2rem;
                padding-bottom: 1rem;
                opacity: 0.8;
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

# logo 圖片
logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"

# 標題
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
if "result" not in st.session_state:
    st.session_state.result = None

button_label = "🔮 抽卡" if not st.session_state.drawn else "🌙 再抽一張"

st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# 抽卡按鈕
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(button_label, use_container_width=True):
        chakra = random.choice(list(data.keys()))
        card = random.choice(data[chakra])
        st.session_state.result = (chakra, card)
        st.session_state.drawn = True

# 顯示抽卡結果
if st.session_state.result:
    chakra, card = st.session_state.result
    st.markdown(f"""
        <div class="card-container">
            <h3 style='color:#FFD6F6;'>🌈 {chakra}</h3>
            <div class='sentence'>💭 {card['sentence']}</div>
            <div class='angel'>🪽 天使數字：{card['angel_number']}</div>
            <div class='meaning'>✨ {card['angel_meaning']}</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align:center;color:#FFE6F7;'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# 底部簽名
st.markdown("""
<div class="footer">
    © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)