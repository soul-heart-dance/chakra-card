import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, timedelta, timezone
from counter_utils import fetch_report


def render_admin_report():
    # ---- 全域樣式 ----
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

    # ---- 取數 ----
    data = fetch_report()
    rows = data["rows"]
    if not rows:
        st.info("目前尚無訪問資料")
        return

    # ---- 資料整理 ----
    df = pd.DataFrame(rows, columns=["日期", "當日訪問", "累積訪問"])
    df["日期"] = pd.to_datetime(df["日期"]).dt.strftime("%Y-%m-%d")
    df["年月"] = pd.to_datetime(df["日期"]).dt.to_period("M").astype(str)

    # ---- 台灣時間 ----
    taiwan_now = datetime.now(timezone(timedelta(hours=8)))
    today_str = taiwan_now.strftime("%Y-%m-%d")

    # ---- 今日訪問數 ----
    today_count = int(df.loc[df["日期"] == today_str, "當日訪問"].values[0]) if today_str in df["日期"].values else 0

    # ---- 月份清單 ----
    months = sorted(df["年月"].unique(), reverse=True)
    latest_month = months[0]
    month_df = df[df["年月"] == latest_month]

    # ---- 統計數字 ----
    st.markdown(
        f"""
        <div class='admin-sub' style='margin-top:0.8rem; font-size:1.05rem; color:#FFD6F6;'>
          🌸 今日訪問：{today_count}　
          🌕 累積訪問：{data['total']}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- 折線圖（當月）----
    if not month_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=month_df["日期"], y=month_df["當日訪問"],
            mode="lines+markers", name="當日訪問",
            line=dict(color="#f6a8ff", width=3, shape="spline"),
            marker=dict(size=8, color="#f6a8ff", line=dict(width=1, color="#fff")),
            hovertemplate="🌸 <b>%{x}</b><br>✨ 當日訪問：%{y}<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=month_df["日期"], y=month_df["累積訪問"],
            mode="lines+markers", name="累積訪問",
            line=dict(color="#8c52ff", width=3, shape="spline"),
            marker=dict(size=8, color="#8c52ff", line=dict(width=1, color="#fff")),
            hovertemplate="🌕 <b>%{x}</b><br>✨ 累積訪問：%{y}<extra></extra>"
        ))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#FFE6F7",
            hovermode="x unified",
            hoverlabel=dict(bgcolor="rgba(255,230,247,0.9)", font_color="#000", font_size=13),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=14)),
            margin=dict(t=50, b=40, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True,
                        config={"displaylogo": False, "modeBarButtonsToRemove": ["toImage"]})
    else:
        st.warning("🌙 本月尚無訪問紀錄")

    # ---- 折線圖與下載報表之間留一點距離 ----
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ---- 月份選擇（放在下載按鈕上方）----
    months = sorted(df["年月"].unique(), reverse=True)
    selected_month = st.selectbox("查詢時間", months, index=0)

    # ---- 下載報表 ----
    month_df = df[df["年月"] == selected_month]
    csv_filename = f"Soul_Heart_Dance_Report_{selected_month}_{taiwan_now.strftime('%H%M%S')}.csv"
    csv_data = month_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

    st.download_button(
        label=f"💾 下載 {selected_month} 報表（CSV）",
        data=BytesIO(csv_data),
        file_name=csv_filename,
        mime="text/csv",
        use_container_width=True
    )
    
    # ---- Hover 動態特效 ----
    st.markdown("""
        <style>
        div.stDownloadButton > button {
            border: 1.2px solid #f6a8ff !important;
            color: #FFD6F6 !important;
            border-radius: 0.6rem !important;
            transition: all 0.3s ease-in-out !important;
        }
        div.stDownloadButton > button:hover {
            box-shadow: 0 0 10px #f6a8ffaa !important;
            border-color: #ffbdfb !important;
            background-color: rgba(246, 168, 255, 0.08) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---- 更新時間放在下載按鈕下方、表格上方 ----
    st.markdown(f"""
    <div class='update-time'>🕓 更新時間：{taiwan_now.strftime('%Y-%m-%d %H:%M')}（台北時間）</div>

    <style>
      .update-time {{
          text-align: center !important;
          font-size: 0.9rem !important;
          color: #e8d4ff !important;
          opacity: 0.8 !important;
          text-shadow: 0 0 6px #cfa7ff !important;
          animation: glow 4s ease-in-out infinite alternate !important;
          margin: 0.5rem 0 0.8rem 0 !important;  /* 👈 上下留距讓版面呼吸 */
      }}
      @keyframes glow {{
          from {{ text-shadow: 0 0 6px #cfa7ff; opacity: 0.65; }}
          to {{ text-shadow: 0 0 12px #ffdbff; opacity: 0.95; }}
      }}
    </style>
    """, unsafe_allow_html=True)

    # ---- 表格 ----
    if not month_df.empty:
        st.dataframe(
            month_df[["日期", "當日訪問", "累積訪問"]],
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("🌸 該月份目前沒有訪問資料")

    # ---- Footer ----
    st.markdown("""
    <div class='footer'>© 2026 Soul Heart Dance · 與靈魂之心共舞</div>
    <style>
      .footer {
          text-align: center !important;
          color: #d8bfff !important;
          font-size: 0.92rem !important;
          margin-top: 1rem !important;
          padding-bottom: 0.8rem !important;
      }
    </style>
    """, unsafe_allow_html=True)