import json
import random
import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪共振卡",
    page_icon="🔮",
    layout="centered"
)

# 脈輪顏色設定
chakra_colors = {
    "菈莯（海底輪）": "#ff7b7b",
    "薇莯（臍輪）": "#ffa260",
    "蕊莯（太陽神經叢輪）": "#ffe066",
    "芽莯（心輪）": "#8bd17c",
    "哈莯（喉輪）": "#7ec8e3",
    "歐莯（眉心輪）": "#b48eff",
    "奧莯（頂輪）": "#e5b8ff"
}

# 載入 JSON 資料
@st.cache_data
def load_data():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# 套用外部 CSS
st.markdown(f"<style>{open('style.css').read()}</style>", unsafe_allow_html=True)

# Logo
logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"

# 標題區塊
st.markdown(f"""
<div class="header">
  <div class="logo-container"><img src="{logo_url}" alt="Soul Heart Dance Logo"></div>
  <div>
    <div class="title-line1">Soul Heart Dance</div>
    <div class="title-line2">七脈輪共振卡</div>
  </div>
</div>
""", unsafe_allow_html=True)

# 狀態管理
if "result" not in st.session_state:
    st.session_state.result = None
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

# 抽卡邏輯
def draw_card():
    chakra = random.choice(list(data.keys()))
    chakra_info = data[chakra]
    seed = chakra_info.get("seed", "")
    card = random.choice(chakra_info["cards"])
    return chakra, seed, card

# 按鈕文字切換
button_label = "🔮 抽卡" if not st.session_state.button_clicked else "🌙 再抽一張"

# 標題
st.markdown("<h4>✨ 抽一張今日的靈魂訊息 ✨</h4>", unsafe_allow_html=True)

# 抽卡按鈕置中
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(button_label, use_container_width=True):
        st.session_state.result = draw_card()
        st.session_state.button_clicked = True  # ✅ 修正：第一次按就更新狀態

# 顯示結果
if st.session_state.result:
    chakra, seed, card = st.session_state.result
    bg_color = chakra_colors.get(chakra, "#FFD6F6")

    # 顯示卡片
    st.markdown(f"""
        <div class="card-container animate-glow" style="--glow-color:{bg_color};">
            <h3 style='color:{bg_color}; margin-top:1.2rem;'>
                🌈 {chakra.split("（")[0]} {seed}（{chakra.split("（")[1]}
            </h3>
            <div class='sentence'>{card['sentence']}</div>
            <div class='angel'>🪽 天使數字：{card['angel_number']}</div>
            <div class='meaning'>✨ {card['angel_meaning']}</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<p>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# 頁尾
st.markdown("""
<div class="footer">
    © 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)