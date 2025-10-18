import streamlit as st
import random
import uuid
import json
import time
from counter_utils import bump_counter

def render_chakra_card():
    """訪客抽卡頁面（柔光載入動畫＋按鈕粉光特效）"""
    st.set_page_config(page_title="Soul Heart Dance｜七脈輪靈魂共振卡", page_icon="🔮", layout="centered")

    # 載入資料與樣式
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    try:
        bump_counter()
    except:
        pass

    if "card" not in st.session_state:
        st.session_state.card = None
    if "clicked" not in st.session_state:
        st.session_state.clicked = False
    if "show_loader" not in st.session_state:
        st.session_state.show_loader = True

    # 🌸 柔光載入動畫
    if st.session_state.show_loader:
        st.markdown('<div class="loader-wrapper"><div class="glow-circle"></div><div class="loader-text">🌸 靈魂正在連線中...</div></div>', unsafe_allow_html=True)
        time.sleep(1.8)
        st.session_state.show_loader = False
        st.rerun()
        return

    # Header
    logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"
    st.markdown(f"""
    <div class="header">
      <img src="{logo_url}" class="logo">
      <div class="title">
        <div class="title-line1">Soul Heart Dance</div>
        <div class="title-line2">七脈輪靈魂共振卡</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='subtitle'>✨ 今日的靈魂訊息 ✨</div>", unsafe_allow_html=True)

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

    button_text = "🔮 抽卡" if st.session_state.card is None else "🌙 再抽一張"
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button(button_text, key="draw_button"):
        st.session_state.card = draw_card()
        st.session_state.clicked = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

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

    st.markdown("<div class='footer'>© 2025 Soul Heart Dance · 與靈魂之心共舞</div>", unsafe_allow_html=True)