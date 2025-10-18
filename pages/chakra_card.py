import streamlit as st
import random
import uuid
import json
import time
from counter_utils import bump_counter

def render_chakra_card():
    """訪客抽卡頁面（含柔光載入動畫與粉光按鈕特效）"""
    st.set_page_config(page_title="Soul Heart Dance｜七脈輪靈魂共振卡", page_icon="🔮", layout="centered")

    # 載入資料與樣式
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("style.css", "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # 背景統計
    try:
        bump_counter()
    except:
        pass

    # Session 初始化
    if "card" not in st.session_state:
        st.session_state.card = None
    if "clicked" not in st.session_state:
        st.session_state.clicked = False
    if "show_loader" not in st.session_state:
        st.session_state.show_loader = True

    # 🌸 柔光載入動畫
    if st.session_state.show_loader:
        loader_html = """
        <div class="loader-wrapper">
          <div class="glow-circle"></div>
          <div class="loader-text">🌸 靈魂正在連線中...</div>
        </div>
        <style>
          .loader-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 85vh;
            animation: fadeout 1.8s ease-in-out forwards;
            animation-delay: 1.8s;
          }
          .glow-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: radial-gradient(circle at center, rgba(255,192,203,0.9), rgba(255,182,193,0.1));
            box-shadow: 0 0 60px 25px rgba(255,192,203,0.5);
            animation: pulse 1.5s infinite ease-in-out;
          }
          .loader-text {
            color: #ffd9ec;
            font-size: 20px;
            margin-top: 30px;
            font-family: "Noto Sans TC", sans-serif;
            text-shadow: 0 0 10px #ffb6c1;
          }
          @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
          }
          @keyframes fadeout {
            100% { opacity: 0; visibility: hidden; }
          }
        </style>
        """
        st.markdown(loader_html, unsafe_allow_html=True)
        time.sleep(1.8)
        st.session_state.show_loader = False
        st.rerun()
        return

    # Header
    logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"
    st.markdown(f"""
    <div class="header">
      <img src="{logo_url}" class="logo" alt="Soul Heart Dance Logo">
      <div class="title">
        <div class="title-line1">Soul Heart Dance</div>
        <div class="title-line2">七脈輪靈魂共振卡</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 副標題
    st.markdown("<div class='subtitle'>✨ 今日的靈魂訊息 ✨</div>", unsafe_allow_html=True)

    # 抽卡邏輯
    def draw_card():
        chakra = random.choice(list(data.keys()))
        meta = data[chakra]
        card = random.choice(meta["cards"])
        return {
            "chakra": chakra,
            "seed": meta["seed"],
            "color": meta["color"],
            "glow": meta["class"],
            "sentence": card["sentence"],
            "angel_number": card["angel_number"],
            "angel_meaning": card["angel_meaning"],
            "uid": str(uuid.uuid4())
        }

    # 🌸 抽卡按鈕（粉光閃爍特效）
    button_text = "🔮 抽卡" if st.session_state.card is None else "🌙 再抽一張"
    st.markdown("""
    <style>
      .button-center {
        display: flex;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 30px;
      }
      div[data-testid="stButton"] button {
        background: linear-gradient(145deg, #ffc1e3, #ffb6c1);
        color: #2e2e2e;
        font-size: 20px;
        border-radius: 50px;
        border: none;
        padding: 0.6em 1.6em;
        font-weight: 600;
        box-shadow: 0 0 20px rgba(255,182,193,0.5);
        transition: all 0.25s ease-in-out;
      }
      div[data-testid="stButton"] button:hover {
        transform: scale(1.08);
        box-shadow: 0 0 35px rgba(255,182,193,0.8);
        background: linear-gradient(145deg, #ffd6e9, #ffc1e3);
      }
      div[data-testid="stButton"] button:active {
        transform: scale(0.95);
        box-shadow: 0 0 25px rgba(255,105,180,0.7);
      }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button(button_text, key="draw_button"):
        st.session_state.card = draw_card()
        st.session_state.clicked = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 顯示卡片
    if st.session_state.card and st.session_state.clicked:
        c = st.session_state.card
        st.markdown(f"""
        <div class="card-wrapper {c['glow']}" id="{c['uid']}">
            <div class="card-container animate">
                <h3 style="color:{c['color']}">🌈 {c['chakra']} {c['seed']}</h3>
                <div class="sentence">{c['sentence']}</div>
                <div class="angel">🪽 天使數字：{c['angel_number']}</div>
                <div class="meaning">✨ {c['angel_meaning']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p class='hint'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer'>© 2025 Soul Heart Dance · 與靈魂之心共舞</div>", unsafe_allow_html=True)