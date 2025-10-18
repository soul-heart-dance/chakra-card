# pages/chakra_draw.py
import json, random, uuid
import streamlit as st
from counter_utils import bump_counter

def _load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def _load_cards():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)

def _header():
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
    st.markdown('<div class="subtitle">✨ 今日的靈魂訊息 ✨</div>', unsafe_allow_html=True)

def _draw_one(cards):
    chakra = random.choice(list(cards.keys()))
    meta = cards[chakra]
    c = random.choice(meta["cards"])
    return {
        "chakra": chakra,
        "seed": meta["seed"],
        "color": meta["color"],
        "glow": meta["class"],
        "sentence": c["sentence"],
        "angel_number": c["angel_number"],
        "angel_meaning": c["angel_meaning"],
        "uid": str(uuid.uuid4())
    }

def render():
    st.set_page_config(page_title="Soul Heart Dance｜七脈輪靈魂共振卡", page_icon="🔮", layout="centered")
    _load_css()
    bump_counter()  # 計數＋1（訪客不會看到數字）

    cards = _load_cards()
    if "card" not in st.session_state:
        st.session_state.card = None

    _header()

    # 按鈕
    btn_text = "🔮 抽卡" if st.session_state.card is None else "🌙 再抽一張"
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button(btn_text, key="draw_button"):
        st.session_state.card = _draw_one(cards)
    st.markdown('</div>', unsafe_allow_html=True)

    # 顯示
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

    st.markdown("""<div class="footer">© 2025 Soul Heart Dance · 與靈魂之心共舞</div>""", unsafe_allow_html=True)

# 讓 Streamlit 直接跑這頁時可顯示
if __name__ == "__main__":
    render()