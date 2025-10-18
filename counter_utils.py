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

    # 取得現有資料
    existing = sheet.get_all_records()
    existing_dates = {row["日期"]: row for row in existing if "日期" in row}

    if today in existing_dates:
        # 更新當日訪問次數
        cell = sheet.find(today)
        if cell:
            today_count = int(existing_dates[today]["訪問數"]) + 1
            total_count = int(existing_dates[today]["累積訪問"])
            sheet.update_cell(cell.row, 2, today_count)
    else:
        # 新增今日記錄
        total_count = 1 if not existing else existing[-1]["累積訪問"] + 1
        today_count = 1
        sheet.append_row([today, today_count, total_count])

    return {"today": today_count, "total": total_count}


def load_counter():
    """讀取試算表資料（用於報表）"""
    sheet = _get_gsheet()
    records = sheet.get_all_records()
    if not records:
        return {"dates": {}, "total": 0}

    dates = {r["日期"]: r["訪問數"] for r in records if "日期" in r}
    total = records[-1]["累積訪問"]
    return {"dates": dates, "total": total}