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
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    gc = gspread.authorize(creds)
    return gc.open_by_key(sheet_id).sheet1


def _safe_int(value):
    """防呆轉換數字"""
    try:
        return int(str(value).strip())
    except Exception:
        return 0


def bump_counter():
    """更新訪問統計，確保欄位正確"""
    sheet = _get_gsheet()
    today = datetime.now().strftime("%Y-%m-%d")
    records = sheet.get_all_records()

    # 檢查欄位結構
    if not records:
        sheet.append_row(["日期", "訪問數", "累積訪問"])
        sheet.append_row([today, 1, 1])
        return {"today": 1, "total": 1}

    # 現有資料
    existing_dates = {r["日期"]: r for r in records if "日期" in r}
    last_total = _safe_int(records[-1].get("累積訪問", 0))

    if today in existing_dates:
        row = existing_dates[today]
        today_count = _safe_int(row.get("訪問數", 0)) + 1
        total_count = last_total  # 不重複加總訪問
        cell = sheet.find(today)
        if cell:
            sheet.update_cell(cell.row, 2, today_count)
    else:
        today_count, total_count = 1, last_total + 1
        sheet.append_row([today, today_count, total_count])

    return {"today": today_count, "total": total_count}


def load_counter():
    """讀取報表資料"""
    sheet = _get_gsheet()
    records = sheet.get_all_records()
    if not records:
        return {"dates": {}, "total": 0}

    dates = {}
    for r in records:
        date = r.get("日期")
        count = _safe_int(r.get("訪問數", 0))
        if date:
            dates[date] = count

    total = _safe_int(records[-1].get("累積訪問", 0))
    return {"dates": dates, "total": total}