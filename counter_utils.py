import json, os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

COUNTER_FILE = "data/counter.json"

def _load_local_counter():
    if not os.path.exists(COUNTER_FILE):
        return {"total": 0, "dates": {}}
    try:
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"total": 0, "dates": {}}

def _save_local_counter(data):
    os.makedirs(os.path.dirname(COUNTER_FILE), exist_ok=True)
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _get_gsheet():
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
    """更新訪問數據（含 Google Sheet 備份）"""
    data = _load_local_counter()
    today = datetime.now().strftime("%Y-%m-%d")
    data["total"] += 1
    data["dates"][today] = data["dates"].get(today, 0) + 1
    _save_local_counter(data)

    try:
        sheet = _get_gsheet()
        existing = sheet.get_all_records()
        existing_dates = {row["日期"]: row for row in existing if "日期" in row}
        if today in existing_dates:
            cell = sheet.find(today)
            if cell:
                sheet.update_cell(cell.row, 2, data["dates"][today])
        else:
            sheet.append_row([today, data["dates"][today], data["total"]])
    except Exception as e:
        print(f"[WARN] Google Sheet 更新失敗：{e}")

    return data

def load_counter():
    """僅讀取統計資料"""
    return _load_local_counter()