import streamlit as st
import time
import json
import random
import uuid
from counter_utils import bump_counter

def render_chakra_card():
    # --- 加載 CSS ---
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- 載入動畫（靈魂連線中） ---
    st.markdown("""
    <div class="loader-wrapper" id="soul-loader">
        <div class="glow-circle"></div>
        <div class="loader-text">🌸 靈魂正在連線中...</div>
    </div>
    <script>
    setTimeout(function(){
        const loader = document.getElementById('soul-loader');
        if (loader){
            loader.style.opacity='0';
            setTimeout(()=>loader.remove(),1600);
        }
    }, 2200);
    </script>
    """, unsafe_allow_html=True)
    time.sleep(2.2)

    # --- 顯示 Header ---
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

    st.markdown("<div class='subtitle'>✨ 今日的靈魂訊息 ✨</div>", unsafe_allow_html=True)

    # --- 計數更新 ---
    bump_counter()

    # --- 抽卡邏輯 ---
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if "card" not in st.session_state:
        st.session_state.card = None

    def draw_card():
        chakra = random.choice(list(data.keys()))
        meta = data[chakra]
        card = random.choice(meta["cards"])
        st.session_state.card = {
            "chakra": chakra,
            "seed": meta["seed"],
            "color": meta["color"],
            "glow": meta["class"],
            "sentence": card["sentence"],
            "angel_number": card["angel_number"],
            "angel_meaning": card["angel_meaning"],
            "uid": str(uuid.uuid4())
        }

    btn_text = "🔮 抽卡" if not st.session_state.card else "🌙 再抽一張"
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    st.button(btn_text, on_click=draw_card, key="draw_card")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.card:
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