import streamlit as st
import pandas as pd
from datetime import datetime

def show_admin_report(counter_data):
    # --- 套用柔光主題 ---
    st.markdown("""
        <style>
        body, .stApp {
            background: radial-gradient(circle at 30% 30%, #2b1b27 0%, #000 100%) !important;
            color: #FFE6F7 !important;
            font-family: "Microsoft JhengHei", Verdana, sans-serif;
        }
        .report-box {
            background: rgba(255, 255, 255, 0.06);
            border-radius: 1.2rem;
            box-shadow: 0 0 18px rgba(255, 192, 230, 0.25);
            padding: 1.2rem 1.4rem;
            margin: 1.2rem auto;
            width: min(720px, 90%);
        }
        .report-title {
            font-size: 1.6rem;
            text-align: center;
            color: #FFD6F6;
            font-weight: 600;
            letter-spacing: 0.03em;
            margin-bottom: 1.2rem;
        }
        .stat {
            text-align: center;
            font-size: 1rem;
            color: #FFE6F7;
            margin-bottom: 0.8rem;
            line-height: 1.6;
        }
        .divider {
            height: 1px;
            background: rgba(255, 255, 255, 0.15);
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 主標題 ---
    st.markdown('<div class="report-title">📊 靈魂訪問統計儀表板</div>', unsafe_allow_html=True)

    today = datetime.now().strftime("%Y-%m-%d")
    today_count = counter_data["dates"].get(today, 0)
    total_count = counter_data["total"]

    # --- 概覽 ---
    st.markdown(f"""
    <div class="report-box">
        <div class="stat">
            ✨ 今日訪問：<b style="color:#FFD6F6;">{today_count}</b><br>
            💫 累積訪問：<b style="color:#FFD6F6;">{total_count}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 統計資料表 ---
    if counter_data["dates"]:
        rows = sorted(counter_data["dates"].items(), key=lambda x: x[0])
        df = pd.DataFrame(rows, columns=["日期", "訪問次數"])

        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown("🗓️ <b>每日訪問紀錄</b>", unsafe_allow_html=True)
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # --- 折線圖 ---
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown("📈 <b>訪問趨勢圖</b>", unsafe_allow_html=True)
        st.line_chart(
            df.set_index("日期"),
            height=240,
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # --- 匯出按鈕 ---
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 下載訪問紀錄 CSV",
            data=csv,
            file_name="visit_stats.csv",
            mime="text/csv",
        )
    else:
        st.info("🌙 目前尚無統計資料")

    # --- Footer ---
    st.markdown("""
    <hr style='border:none;height:1px;background:rgba(255,255,255,0.15);margin-top:1rem;margin-bottom:1rem;'>
    <p style='text-align:center;color:#999;font-size:0.9rem;'>✨ 管理者專用報表頁 ✨</p>
    """, unsafe_allow_html=True)