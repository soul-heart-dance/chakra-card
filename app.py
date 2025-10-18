import json
import random
import streamlit as st
import uuid
from datetime import datetime
import os
import pandas as pd

# ---------- 永久保存 ----------
DATA_DIR = "data"
COUNTER_FILE = os.path.join(DATA_DIR, "counter.json")
os.makedirs(DATA_DIR, exist_ok=True)

def update_counter():
    """更新訪問計數並回傳目前統計資料"""
    if not os.path.exists(COUNTER_FILE):
        data = {"total": 0, "dates": {}}
    else:
        try:
            with open(COUNTER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"total": 0, "dates": {}}

    today = datetime.now().strftime("%Y-%m-%d")
    data["total"] += 1
    data["dates"][today] = data["dates"].get(today, 0) + 1

    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


# ---------- Streamlit 設定 ----------
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

# ---------- 檢查是否為管理者 ----------
qp = st.query_params.to_dict()
is_admin = qp.get("sara") in ("1", ["1"])

# ---------- 訪問計數 ----------
counter_data = update_counter()

# ---------- 如果是管理者 → 顯示統計頁 ----------
if is_admin:
    st.markdown('<div class="subtitle">📊 靈魂訪問統計報表</div>', unsafe_allow_html=True)

    today = datetime.now().strftime("%Y-%m-%d")
    today_count = counter_data["dates"].get(today, 0)
    total_count = counter_data["total"]

    # 概覽數字
    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:1rem;
            color:#FFD6F6;
            opacity:0.95;
            margin: 0.2rem auto 1.0rem;
            background: rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 10px 14px;
            display: inline-block;
        ">
            今日訪問：{today_count}　｜　累積訪問：{total_count}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 每日統計表
    if counter_data["dates"]:
        rows = sorted(counter_data["dates"].items(), key=lambda x: x[0])
        df = pd.DataFrame(rows, columns=["日期", "訪問次數"])
        st.markdown("🗓️ 每日訪問統計")
        st.dataframe(df, hide_index=True, use_container_width=True)

        # 折線圖
        st.markdown("📈 訪問趨勢圖")
        df_chart = df.set_index("日期")
        st.line_chart(df_chart, height=240, use_container_width=True)
    else:
        st.info("目前尚無統計資料 🌙")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888;'>✨ 管理者專用報表頁 ✨</p>", unsafe_allow_html=True)

# ---------- 一般訪客（抽卡介面） ----------
else:
    st.markdown('<div class="subtitle">✨ 今日的靈魂訊息 ✨</div>', unsafe_allow_html=True)

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
            "uid": str(uuid.uuid4()),
        }

    # 抽卡按鈕
    btn_text = "🔮 抽卡" if st.session_state.card is None else "🌙 再抽一張"
    st.markdown('<div class="button-center">', unsafe_allow_html=True)
    st.button(btn_text, on_click=draw_card, key="draw_button")
    st.markdown("</div>", unsafe_allow_html=True)

    # 顯示卡片或提示文字
    if st.session_state.card:
        c = st.session_state.card
        st.markdown(
            f"""
            <div class="card-wrapper {c['glow']}" id="{c['uid']}">
                <div class="card-container animate">
                    <h3 style="color:{c['color']}">🌈 {c['chakra']} {c['seed']}</h3>
                    <div class="sentence">{c['sentence']}</div>
                    <div class="angel">🪽 天使數字：{c['angel_number']}</div>
                    <div class="meaning">✨ {c['angel_meaning']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<p class='hint'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<div class="footer">
© 2025 Soul Heart Dance · 與靈魂之心共舞
</div>
""", unsafe_allow_html=True)