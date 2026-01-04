import streamlit as st
import json
import random
import uuid
from counter_utils import bump_counter

def render_chakra_card():
    # === 🌸 套用樣式 ===
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # === 🌟 Header ===
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

    # === 📈 計數功能 ===
    bump_counter()

    # === 📜 載入卡片資料 ===
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # === 🩵 初始化狀態 ===
    if "card" not in st.session_state:
        st.session_state.card = None

    # === 🔮 抽卡邏輯 ===
    def draw_card():
        chakra = random.choice(list(data.keys()))
        meta = data[chakra]
        card = random.choice(meta["cards"])
        st.session_state.card = {
            "chakra": chakra,
            "seed": meta["seed"],
            "color": meta["color"],
            "sentence": card["sentence"],
            "angel_number": card["angel_number"],
            "angel_meaning": card["angel_meaning"],
            "uid": str(uuid.uuid4())
        }

    # === 💖 小小提醒（輕盈版） ===
    st.markdown("""
    <div class="reminder-box fade-in">
      想著當下最想了解的問題再抽<br>
      或讓自己放鬆、隨心點選也可以<br>
      靈魂總會在此刻傳遞最適合你的指引🌙
    </div>
    """, unsafe_allow_html=True)

    # === ✨ 副標題 ===
    st.markdown("<div class='subtitle'>✨ 今日的靈魂訊息 ✨</div>", unsafe_allow_html=True)

    # === 🔘 抽卡按鈕（置中） ===
    btn_text = "🔮 抽卡" if not st.session_state.card else "🌙 再抽一張"
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    st.button(btn_text, on_click=draw_card, key="draw_card_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    # === 🌈 顯示卡片 ===
    if st.session_state.card:
        c = st.session_state.card
        st.markdown(f"""
        <div class="card-wrapper" id="{c['uid']}" style="--chakra-color: {c['color']}">
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

    # === 💫 Footer ===
    st.markdown("<div class='footer'>© 2026 Soul Heart Dance · 與靈魂之心共舞</div>", unsafe_allow_html=True)