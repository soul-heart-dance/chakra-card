import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import datetime, timedelta, timezone
from counter_utils import fetch_report

def render_admin_report():
    # ---- 套用全域樣式 ----
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # ---- Header ----
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

    # ---- 取得資料 ----
    data = fetch_report()
    rows = data["rows"]

    st.markdown(f"""
    <div class='admin-sub' style='margin-top:0.8rem; font-size:1.05rem; color:#FFD6F6;'>
      🌸 今日訪問：{data['today']}　🌕 累積訪問：{data['total']}
    </div>
    """, unsafe_allow_html=True)

    if not rows:
        st.info("目前尚無訪問資料")
        return

    # ---- 整理資料表 ----
    df = pd.DataFrame(rows, columns=["日期", "當日訪問", "累積訪問"])

    # ---- 台灣時間（UTC+8） ----
    taiwan_now = datetime.now(timezone(timedelta(hours=8)))
    csv_filename = f"Soul_Heart_Dance_Report_{taiwan_now.strftime('%Y%m%d_%H%M%S')}.csv"

    # ---- 柔光粉金＋紫色線條 ----
    fig = px.line(
        df,
        x="日期",
        y=["當日訪問", "累積訪問"],
        markers=True,
        color_discrete_sequence=["#f6a8ff", "#8c52ff"]
    )

    # ---- 愛心點與柔光線條設定 ----
    fig.update_traces(
        line=dict(width=4, shape="spline"),
        marker=dict(
            size=14,
            symbol="heart",  # 💖 讓點變成愛心
            opacity=1,
            line=dict(width=1, color="white")
        ),
        hovertemplate="<b>%{x}</b><br>✨ %{y}<extra></extra>"
    )

    # ---- 模擬 glow 效果的背景光暈 ----
    for i, color in enumerate(["#f6a8ff", "#8c52ff"]):
        fig.add_scatter(
            x=df["日期"],
            y=df[["當日訪問", "累積訪問"][i]],
            mode="lines",
            line=dict(width=18, color=color, opacity=0.08),
            hoverinfo="skip",
            showlegend=False
        )

    # ---- 柔光互動風格 ----
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#FFE6F7",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="rgba(255,230,247,0.9)",
            font_color="#000",
            font_size=13
        ),
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

    # ---- 顯示圖表（移除下載圖檔按鈕）----
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "modeBarButtonsToRemove": ["toImage", "editInChartStudio", "sendDataToCloud"],
            "responsive": True
        }
    )

    # ---- 自訂下載 CSV 按鈕 ----
    csv_data = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="💾 下載報表（CSV）",
        data=BytesIO(csv_data),
        file_name=csv_filename,
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("""
    <div style="color:#FFD6F6; font-size:0.9rem; margin-top:-0.3rem; text-align:center;">
      ✨ 檔名與時間皆已依台灣時區命名（UTF-8 編碼格式）
    </div>
    """, unsafe_allow_html=True)

    # ---- 表格 ----
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