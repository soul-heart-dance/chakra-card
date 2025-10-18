import os
import json
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# ---- 讀 ENV ----
SHEET_ID   = os.environ.get("GOOGLE_SHEET_ID", "").strip()
CREDS_JSON = os.environ.get("GOOGLE_CREDENTIALS_JSON", "").strip()

# ---- 工具 ----
def _to_int(x):
    try:
        if x is None:
            return 0
        if isinstance(x, (int, float)):
            return int(x)
        s = str(x).strip()
        return int(s) if s else 0
    except:
        return 0

def _today():
    return datetime.now().strftime("%Y-%m-%d")

# ---- 取得工作表 ----
def get_gsheet():
    if not SHEET_ID or not CREDS_JSON:
        raise Exception("❌ GOOGLE API 金鑰或試算表 ID 尚未設定！")
    creds_info = json.loads(CREDS_JSON)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    try:
        ws = sh.worksheet("visits")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title="visits", rows=1000, cols=3)
        ws.update("A1:C1", [["日期", "訪問數", "累積訪問"]])
    # 確保有表頭
    headers = ws.row_values(1)
    if headers[:3] != ["日期", "訪問數", "累積訪問"]:
        ws.update("A1:C1", [["日期", "訪問數", "累積訪問"]])
    return ws

# ---- 寫入 + 回傳統計（每次載入抽卡頁時呼叫一次）----
def bump_counter():
    ws = get_gsheet()
    values = ws.get_all_values()  # 含表頭
    today = _today()

    # 只有表頭 -> 第一天
    if len(values) == 1:
        ws.append_row([today, 1, 1])
        return {"today": 1, "total": 1}

    last_row = values[-1]
    last_date = last_row[0] if len(last_row) > 0 else ""
    last_visit = _to_int(last_row[1] if len(last_row) > 1 else 0)
    last_total = _to_int(last_row[2] if len(last_row) > 2 else 0)

    # 取「前一天的累積」作為 today 的基底
    prev_total = 0
    if len(values) >= 3:
        prev_row = values[-2]
        prev_total = _to_int(prev_row[2] if len(prev_row) > 2 else 0)

    if last_date == today:
        # 同一天：更新當天行
        today_count = last_visit + 1
        # 當天累積＝「前一天累積」＋「當天累計訪問」
        total_count = prev_total + today_count
        ws.update(f"A{len(values)}:C{len(values)}", [[today, today_count, total_count]])
        return {"today": today_count, "total": total_count}
    else:
        # 新的一天：新增一行
        today_count = 1
        total_count = last_total + today_count
        ws.append_row([today, today_count, total_count])
        return {"today": today_count, "total": total_count}

# ---- 讀取完整資料（給管理者頁）----
def fetch_report():
    ws = get_gsheet()
    values = ws.get_all_values()
    # 沒資料只回表頭
    if len(values) <= 1:
        return {
            "rows": [],
            "today": 0,
            "total": 0
        }
    rows = []
    for r in values[1:]:
        date = r[0] if len(r) > 0 else ""
        day = _to_int(r[1] if len(r) > 1 else 0)
        total = _to_int(r[2] if len(r) > 2 else 0)
        rows.append((date, day, total))
    today = rows[-1][1]
    total = rows[-1][2]
    return {"rows": rows, "today": today, "total": total}