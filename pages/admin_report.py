import streamlit as st
import pandas as pd
import plotly.express as px
from counter_utils import fetch_report
from datetime import datetime, timedelta, timezone

def render_admin_report():
    # ---- 套用全域樣式 ----
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # ---- Header：與抽卡頁相同的 Logo + 標題樣式 ----
    logo_url = "https://huggingface.co/spaces/soul-heart-dance/chakra-card/resolve/main/shop_logo.png"
    st.markdown(f"""
    <div class="header">
      <img src="{logo_url}" class="logo" alt="Soul Heart Dance Logo">
      <div class="title">
        <div class="title-line1">Soul Heart Dance</div>
        <div class="title-line2">七脈輪靈魂共振卡・管理報表</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- 取得訪問資料 ----
    data = fetch_report()
    rows = data["rows"]

    # ---- 統計數字區塊 ----
    st.markdown(f"""
    <div class='admin-sub' style='margin-top:0.8rem; font-size:1.05rem; color:#FFD6F6;'>
      🌸 今日訪問：{data['today']}　🌕 累積訪問：{data['total']}
    </div>
    """, unsafe_allow_html=True)

    # ---- 若無資料 ----
    if not rows:
        st.info("目前尚無訪問資料")
        return

    # ---- 整理資料表 ----
    df = pd.DataFrame(rows, columns=["日期", "當日訪問", "累積訪問"])

    # ---- 台灣時間（UTC+8）作為檔名基準 ----
    taiwan_now = datetime.now(timezone(timedelta(hours=8)))
    plot_filename = f"Soul_Heart_Dance_Report_{taiwan_now.strftime('%Y%m%d_%H%M%S')}"

    # ---- 柔光粉金＋紫色風格折線圖 ----
    fig = px.line(
        df,
        x="日期",
        y=["當日訪問", "累積訪問"],
        markers=True,
        color_discrete_sequence=["#f6a8ff", "#8c52ff"]  # 粉金 & 紫
    )

    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFE6F7",
        legend_title_text=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(t=50, b=40, l=20, r=20)
    )

    # ✅ 設定 Plotly 下載圖檔檔名（以台灣時間命名）
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "toImageButtonOptions": {
                "filename": plot_filename,
                "scale": 2
            }
        }
    )

    # ---- 表格顯示 ----
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
    )

    # ---- Footer ----
    st.markdown("""
    <div class='footer'>
      © 2025 Soul Heart Dance · 與靈魂之心共舞
    </div>
    """, unsafe_allow_html=True)