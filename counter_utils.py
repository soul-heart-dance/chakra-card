import json, os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def _get_gsheet():
    """連接 Google Sheet"""
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")

    if not creds_json or not sheet_id:
        raise Exception("❌ GOOGLE API 金鑰或試算表 ID 尚未設定！")

    creds_dict = json.loads(creds_json)
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    gc = gspread.authorize(creds)
    return gc.open_by_key(sheet_id).sheet1


def bump_counter():
    """更新訪問統計"""
    sheet = _get_gsheet()
    today = datetime.now().strftime("%Y-%m-%d")

    existing = sheet.get_all_records()
    existing_dates = {row["日期"]: row for row in existing if "日期" in row}

    # 取得當天與總訪問數
    if today in existing_dates:
        row = existing_dates[today]
        today_count = _safe_int(row.get("訪問數", 0)) + 1
        total_count = _safe_int(row.get("累積訪問", 0)) + 1
        cell = sheet.find(today)
        if cell:
            sheet.update_cell(cell.row, 2, today_count)
            sheet.update_cell(cell.row, 3, total_count)
    else:
        # 新增第一筆或下一天資料
        last_total = _safe_int(existing[-1].get("累積訪問", 0)) if existing else 0
        today_count, total_count = 1, last_total + 1
        sheet.append_row([today, today_count, total_count])

    return {"today": today_count, "total": total_count}


def _safe_int(value):
    """防呆轉換數字"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def load_counter():
    """讀取試算表資料（用於報表）"""
    sheet = _get_gsheet()
    records = sheet.get_all_records()
    if not records:
        return {"dates": {}, "total": 0}

    dates = {}
    for r in records:
        try:
            dates[r["日期"]] = _safe_int(r["訪問數"])
        except KeyError:
            pass

    total = _safe_int(records[-1].get("累積訪問", 0))
    return {"dates": dates, "total": total}