import streamlit as st
import json, random

# ---------- 基本設定 ----------
st.set_page_config(page_title="七脈輪靈魂共振卡", page_icon="✨", layout="centered")

with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ---------- 樣式載入 ----------
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- 標題區 ----------
st.markdown("""
<div class="header">
  <div class="logo-container">
    <img src="https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png">
  </div>
  <div>
    <div class="title-line1">Soul Heart Dance</div>
    <div class="title-line2">七脈輪靈魂共振卡</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# ---------- 抽卡功能 ----------
if "current_card" not in st.session_state:
    st.session_state.current_card = None

col = st.columns([1, 2, 1])
with col[1]:
    if st.button("🔮 抽卡" if st.session_state.current_card is None else "🌙 再抽一張"):
        chakra = random.choice(list(data.keys()))
        card = random.choice(data[chakra])
        st.session_state.current_card = {
            "chakra": chakra,
            "card": card,
            "color": card.get("color", "#FFE6F7"),
            "seed": card.get("seed", "")
        }
        # 重新渲染頁面，讓柔光掃過動畫重新啟動
        st.rerun()

# ---------- 顯示卡片 ----------
if st.session_state.current_card:
    chakra = st.session_state.current_card["chakra"]
    card = st.session_state.current_card["card"]
    color = st.session_state.current_card["color"]
    seed = st.session_state.current_card["seed"]

    # 套入脈輪對應色的光暈類別
    chakra_class_map = {
        "海底輪": "root-glow",
        "臍輪": "sacral-glow",
        "太陽神經叢": "solar-glow",
        "心輪": "heart-glow",
        "喉輪": "throat-glow",
        "眉心輪": "third-glow",
        "頂輪": "crown-glow"
    }
    chakra_class = chakra_class_map.get(chakra, "root-glow")

    st.markdown(f"""
    <div class="card-container {chakra_class} shine-card">
      <h3 style="color:{color};">🌈 {card['name']}（{chakra}） {seed}</h3>
      <div class="sentence">{card['message']}</div>
      <div class="angel">🪽 天使數字：{card['angel_number']}</div>
      <div class="meaning">✨ {card['meaning']}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- 底部 ----------
st.markdown("""
<div class="footer">
  © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)