import json
import random
import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)

# 載入資料
@st.cache_data
def load_data():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)
data = load_data()

# 套用 CSS
with open("style.css", "r", encoding="utf-8") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Logo URL
logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"

# 標題區塊
st.markdown(f"""
<div class="header">
  <div class="logo-container">
    <img src="{logo_url}" alt="Soul Heart Dance Logo">
  </div>
  <div class="title-text">
    <div class="title-line1">Soul Heart Dance</div>
    <div class="title-line2">七脈輪靈魂共振卡</div>
  </div>
</div>
""", unsafe_allow_html=True)

# 狀態管理
if "drawn" not in st.session_state:
    st.session_state.drawn = False
if "selected" not in st.session_state:
    st.session_state.selected = None
if "button_label" not in st.session_state:
    st.session_state.button_label = "🔮 抽卡"

# 抽卡標題
st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# 抽卡按鈕
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(st.session_state.button_label, use_container_width=True):
        chakra_name = random.choice(list(data.keys()))
        chakra_info = data[chakra_name]
        card = random.choice(chakra_info["cards"])

        st.session_state.drawn = True
        st.session_state.selected = {
            "name": chakra_name,
            "seed": chakra_info["seed"],
            "color": chakra_info["color"],
            "class": chakra_info["class"],
            "card": card,
            "shine_class": f"shine-{random.randint(1,10000)}"  # 強制刷新動畫
        }

        # 立即更新按鈕文字與畫面
        st.session_state.button_label = "🌙 再抽一張"
        st.rerun()

# 顯示抽卡結果
if st.session_state.drawn and st.session_state.selected:
    c = st.session_state.selected
    shine_class = c.get("shine_class", "")
    st.markdown(f"""
    <div class="card-container {c['class']} {shine_class}" style="--chakra-color:{c['color']}">
        <h3 style="color:{c['color']}">🌈 {c['name']}（{c['card']['chakra']}） {c['seed']}</h3>
        <div class="sentence">{c['card']['sentence']}</div>
        <div class="angel">🪽 天使數字：{c['card']['angel_number']}</div>
        <div class="meaning">✨ {c['card']['angel_meaning']}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p class='hint'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# 底部簽名
st.markdown("""
<div class="footer">
    © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)