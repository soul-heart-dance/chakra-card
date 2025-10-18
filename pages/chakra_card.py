import json, random, uuid
import streamlit as st
from counter_utils import bump_counter

# 讀卡片資料與 CSS
@st.cache_data
def load_data():
    with open("chakras_affirmations.json","r",encoding="utf-8") as f:
        return json.load(f)
@st.cache_data
def load_css():
    with open("style.css","r",encoding="utf-8") as f:
        return f.read()

def render_chakra_card():
    st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

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

    # 抬頭
    st.markdown('<div class="subtitle">✨ 今日的靈魂訊息 ✨</div>', unsafe_allow_html=True)

    # 進入頁面 → 計數（訪客版只做計數，不顯示數字）
    try:
        bump_counter()
    except Exception as e:
        # 即使寫入失敗，也不要讓畫面黑掉
        st.toast("計數寫入暫時失敗，但不影響抽卡使用 💖", icon="⚠️")

    # Session 初始化
    if "card" not in st.session_state:
        st.session_state.card = None

    data = load_data()

    # 抽卡邏輯
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

    # 按鈕
    btn_text = "🔮 抽卡" if st.session_state.card is None else "🌙 再抽一張"
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    if st.button(btn_text, use_container_width=False):
        draw_card()
        st.rerun()   # 立即更新按鈕文字
    st.markdown('</div>', unsafe_allow_html=True)

    # 卡片
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

    # Footer
    st.markdown("<div class='footer'>© 2025 Soul Heart Dance · 與靈魂之心共舞</div>", unsafe_allow_html=True)