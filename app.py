import json
import random
import streamlit as st
import uuid
from datetime import datetime
import os

# ---------- 永久保存設定 ----------
DATA_DIR = "data"
COUNTER_FILE = os.path.join(DATA_DIR, "counter.json")
os.makedirs(DATA_DIR, exist_ok=True)  # 確保目錄存在


# ---------- 計數器 ----------
def update_counter():
    """更新訪問計數並回傳統計資料"""
    if not os.path.exists(COUNTER_FILE):
        data = {"total": 0, "dates": {}}
    else:
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"total": 0, "dates": {}}

    today = datetime.now().strftime("%Y-%m-%d")
    data["total"] += 1
    data["dates"][today] = data["dates"].get(today, 0) + 1

    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


# ---------- Streamlit 頁面設定 ----------
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)


# ---------- 載入資料與樣式 ----------
@st.cache_data
def load_data():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        return f.read()

data = load_data()
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)


# ---------- 初始化 ----------
if "card" not in st.session_state:
    st.session_state.card = None


# ---------- Header ----------
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


# ---------- 標題 ----------
st.markdown("""
<div class="subtitle">
✨ 今日的靈魂訊息 ✨
</div>
""", unsafe_allow_html=True)


# ---------- 更新訪問計數 ----------
counter_data = update_counter()


# ---------- Sara 專用模式 ----------
query_params = st.query_params.to_dict()
if query_params.get("sara") == "1" or query_params.get("sara") == ["1"]:
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = counter_data["dates"].get(today, 0)
    total_count = counter_data["total"]

    # 只顯示簡潔數字（品牌色系）
    st.markdown(
        f"""
        <div style="
            text-align:right;
            font-size:0.9rem;
            color:#FFD6F6;
            opacity:0.9;
            margin-bottom:0.8rem;
            background:rgba(255,255,255,0.05);
            border-radius:12px;
            padding:8px 12px;
            display:inline-block;
        ">
        今日訪問：{today_count}　|　累積訪問：{total_count}
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- 抽卡邏輯 ----------
def draw_card():
    chakra = random.choice(list(data.keys()))
    meta = data[chakra]
    card = random.choice(meta["cards"])
    uid = str(uuid.uuid4())
    st.session_state.card = {
        "chakra": chakra,
        "seed": meta["seed"],
        "color": meta["color"],
        "glow": meta["class"],
        "sentence": card["sentence"],
        "angel_number": card["angel_number"],
        "angel_meaning": card["angel_meaning"],
        "uid": uid
    }


# ---------- 按鈕 ----------
button_text = "🔮 抽卡" if st.session_state.card is None else "🌙 再抽一張"
st.markdown('<div class="button-center">', unsafe_allow_html=True)
st.button(button_text, on_click=draw_card, key="draw_button")
st.markdown('</div>', unsafe_allow_html=True)


# ---------- 顯示卡片 ----------
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


# ---------- Footer ----------
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)import json
import random
import streamlit as st
import uuid
from datetime import datetime
import os

# ---------- 永久保存設定 ----------
DATA_DIR = "data"
COUNTER_FILE = os.path.join(DATA_DIR, "counter.json")
os.makedirs(DATA_DIR, exist_ok=True)  # 確保目錄存在


# ---------- 計數器 ----------
def update_counter():
    """更新訪問計數並回傳統計資料"""
    if not os.path.exists(COUNTER_FILE):
        data = {"total": 0, "dates": {}}
    else:
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"total": 0, "dates": {}}

    today = datetime.now().strftime("%Y-%m-%d")
    data["total"] += 1
    data["dates"][today] = data["dates"].get(today, 0) + 1

    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


# ---------- Streamlit 頁面設定 ----------
st.set_page_config(
    page_title="Soul Heart Dance｜七脈輪靈魂共振卡",
    page_icon="🔮",
    layout="centered"
)


# ---------- 載入資料與樣式 ----------
@st.cache_data
def load_data():
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        return f.read()

data = load_data()
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)


# ---------- 初始化 ----------
if "card" not in st.session_state:
    st.session_state.card = None


# ---------- Header ----------
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


# ---------- 標題 ----------
st.markdown("""
<div class="subtitle">
✨ 今日的靈魂訊息 ✨
</div>
""", unsafe_allow_html=True)


# ---------- 更新訪問計數 ----------
counter_data = update_counter()


# ---------- Sara 專用模式 ----------
query_params = st.query_params.to_dict()
if query_params.get("sara") == "1" or query_params.get("sara") == ["1"]:
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = counter_data["dates"].get(today, 0)
    total_count = counter_data["total"]

    # 只顯示簡潔數字（品牌色系）
    st.markdown(
        f"""
        <div style="
            text-align:right;
            font-size:0.9rem;
            color:#FFD6F6;
            opacity:0.9;
            margin-bottom:0.8rem;
            background:rgba(255,255,255,0.05);
            border-radius:12px;
            padding:8px 12px;
            display:inline-block;
        ">
        今日訪問：{today_count}　|　累積訪問：{total_count}
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- 抽卡邏輯 ----------
def draw_card():
    chakra = random.choice(list(data.keys()))
    meta = data[chakra]
    card = random.choice(meta["cards"])
    uid = str(uuid.uuid4())
    st.session_state.card = {
        "chakra": chakra,
        "seed": meta["seed"],
        "color": meta["color"],
        "glow": meta["class"],
        "sentence": card["sentence"],
        "angel_number": card["angel_number"],
        "angel_meaning": card["angel_meaning"],
        "uid": uid
    }


# ---------- 按鈕 ----------
button_text = "🔮 抽卡" if st.session_state.card is None else "🌙 再抽一張"
st.markdown('<div class="button-center">', unsafe_allow_html=True)
st.button(button_text, on_click=draw_card, key="draw_button")
st.markdown('</div>', unsafe_allow_html=True)


# ---------- 顯示卡片 ----------
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


# ---------- Footer ----------
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)