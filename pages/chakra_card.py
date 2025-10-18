import streamlit as st
import random
import uuid
import json
from counter_utils import bump_counter

def render_chakra_card():
    """主要抽卡頁面"""
    st.markdown("<h1 style='text-align:center;'>Soul Heart Dance</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>七脈輪靈魂共振卡 ✨</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>✨ 今日的靈魂訊息 ✨</p>", unsafe_allow_html=True)

    # 計數邏輯
    try:
        counter_data = bump_counter()
        st.markdown(
            f"<div style='text-align:center; color:#aaa;'>今日訪問：{counter_data['today']} ｜ 累積訪問：{counter_data['total']}</div>",
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"⚠️ 計數器錯誤：{e}")

    # 抽卡狀態初始化
    if "card" not in st.session_state:
        st.session_state.card = None

    # 抽卡按鈕
    button_text = "🔮 抽卡" if st.session_state.card is None else "🌙 再抽一張"
    if st.button(button_text):
        st.session_state.card = draw_card()

    # 顯示抽卡內容
    if st.session_state.card:
        c = st.session_state.card
        st.markdown(f"""
        <div style='border:1px solid #FFD6F6; border-radius:15px; padding:20px; margin-top:20px; text-align:center; color:{c['color']}; background-color:#111;'>
            <h3>🌈 {c['chakra']} {c['seed']}</h3>
            <div style='margin:10px 0;'>{c['sentence']}</div>
            <div>🪽 天使數字：{c['angel_number']}</div>
            <div>✨ {c['angel_meaning']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center;'>🌙 點擊上方按鈕開始抽卡 🌙</p>", unsafe_allow_html=True)


def draw_card():
    """抽卡邏輯"""
    with open("chakras_affirmations.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    chakra = random.choice(list(data.keys()))
    meta = data[chakra]
    card = random.choice(meta["cards"])
    return {
        "chakra": chakra,
        "seed": meta["seed"],
        "color": meta["color"],
        "sentence": card["sentence"],
        "angel_number": card["angel_number"],
        "angel_meaning": card["angel_meaning"],
        "uid": str(uuid.uuid4())
    }