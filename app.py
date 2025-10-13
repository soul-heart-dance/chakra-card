import streamlit as st
import json, random

# ---------- 基本設定 ----------
st.set_page_config(page_title="七脈輪靈魂共振卡", page_icon="✨", layout="centered")

# ---------- 載入 JSON ----------
with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ---------- 載入樣式 ----------
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- 標題與 Logo ----------
st.markdown("""
<div class="header" style="margin-top:-1rem;">
  <div class="logo-container">
    <img src="shop_logo.png">
  </div>
  <div>
    <div class="title-line1">Soul Heart Dance</div>
    <div class="title-line2">七脈輪靈魂共振卡</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# ---------- 抽卡邏輯 ----------
if "current_card" not in st.session_state:
    st.session_state.current_card = None

if st.button("🔮 抽卡" if not st.session_state.current_card else "🌙 再抽一張"):
    chakra = random.choice(list(data.keys()))
    chakra_info = data[chakra]
    card = random.choice(chakra_info["cards"])

    st.session_state.current_card = {
        "name": chakra,
        "seed": chakra_info["seed"],
        "color": chakra_info["color"],
        "class": chakra_info["class"],
        "sentence": card["sentence"],
        "angel_number": card["angel_number"],
        "angel_meaning": card["angel_meaning"]
    }
    st.rerun()

# ---------- 顯示卡片 ----------
if st.session_state.current_card:
    c = st.session_state.current_card
    st.markdown(f"""
    <div class="card-container {c['class']} shine-card">
        <h3 style="color:{c['color']}">🌈 {c['name']} {c['seed']}</h3>
        <div class="sentence">{c['sentence']}</div>
        <div class="angel">🪽 天使數字：{c['angel_number']}</div>
        <div class="meaning">✨ {c['angel_meaning']}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- 底部 ----------
st.markdown("""
<div class="footer">
  © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)