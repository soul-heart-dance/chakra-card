import streamlit as st
import pandas as pd
from datetime import datetime
import io

def show_admin_report(counter_data):
    st.markdown('<div class="subtitle">📊 靈魂訪問統計報表</div>', unsafe_allow_html=True)

    today = datetime.now().strftime("%Y-%m-%d")
    today_count = counter_data["dates"].get(today, 0)
    total_count = counter_data["total"]

    # 概覽
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

    # 若有資料 → 顯示表格與折線圖
    if counter_data["dates"]:
        rows = sorted(counter_data["dates"].items(), key=lambda x: x[0])
        df = pd.DataFrame(rows, columns=["日期", "訪問次數"])

        st.markdown("🗓️ 每日訪問統計")
        st.dataframe(df, hide_index=True, use_container_width=True)

        st.markdown("📈 訪問趨勢圖")
        st.line_chart(df.set_index("日期"), height=240, use_container_width=True)

        # 匯出 CSV
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 下載訪問紀錄 CSV",
            data=csv,
            file_name="visit_stats.csv",
            mime="text/csv",
        )
    else:
        st.info("目前尚無統計資料 🌙")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888;'>✨ 管理者專用報表頁 ✨</p>", unsafe_allow_html=True)