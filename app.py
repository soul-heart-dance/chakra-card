import json
import random
import streamlit as st
import uuid
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt

COUNTER_FILE = "counter.json"

# ---------- 計數器函式 ----------
def update_counter():
    """更新訪問計數"""
    if not os.path.exists(COUNTER_FILE):
        data = {"total": 0, "dates": {}}
    else:
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

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


# ---------- 標題文字 ----------
st.markdown("""
<div class="subtitle">
✨ 今日的靈魂訊息 ✨
</div>
""", unsafe_allow_html=True)


# ---------- 計數器 ----------
counter_data = update_counter()


# ---------- 隱藏版管理者檢視 ----------
query_params = st.query_params.to_dict()
if query_params.get("sara") == "1" or query_params.get("sara") == ["1"]:
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = counter_data["dates"].get(today, 0)
    total_count = counter_data["total"]

    # 總覽數字
    st.markdown(
        f"""
        <div style='text-align:right; font-size:0.9rem; color:#FFD6F6; opacity:0.85; margin-bottom:0.6rem;'>
        今日訪問：{today_count}　|　累積訪問：{total_count}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 每日統計表格
    if counter_data["dates"]:
        st.markdown(
            """
            <div style='font-size:1rem; color:#FFE6F7; margin-top:1.2rem; text-align:left;'>
            🗓️ <b>每日訪問統計</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        sorted_dates = sorted(counter_data["dates"].items(), reverse=True)
        table_html = "<table style='width:100%; font-size:0.95rem; color:#FFE6F7; border-collapse:collapse;'>"
        table_html += "<tr style='color:#FFD6F6; font-weight:bold;'><th align=\"left\">日期</th><th align=\"right\">訪問次數</th></tr>"
        for date, count in sorted_dates:
            table_html += f"<tr><td>{date}</td><td align='right'>{count}</td></tr>"
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)

        # 七日折線圖
        dates = []
        counts = []
        for i in range(6, -1, -1):  # 過去 7 天
            d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            dates.append(d)
            counts.append(counter_data["dates"].get(d, 0))

        fig, ax = plt.subplots(figsize=(6, 2.8))
        ax.plot(dates, counts, marker="o", color="#FFB6D9", linewidth=2.5)
        ax.fill_between(dates, counts, color="#FFB6D9", alpha=0.15)
        ax.set_title("最近 7 天訪問趨勢", color="#FFD6F6", fontsize=12, pad=10)
        ax.tick_params(axis="x", labelrotation=30, labelsize=9, colors="#FFD6F6")
        ax.tick_params(axis="y", labelsize=9, colors="#FFD6F6")
        ax.spines["bottom"].set_color("#FFD6F6")
        ax.spines["left"].set_color("#FFD6F6")
        ax.set_facecolor("#1E1E1E")
        fig.patch.set_facecolor("#1E1E1E")
        st.pyplot(fig)
    else:
        st.info("尚無訪問紀錄。")


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