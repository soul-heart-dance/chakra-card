import os
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ===== Google Sheet 驗證與連線 =====
def get_gsheet():
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")

    if not creds_json or not sheet_id:
        raise Exception("❌ GOOGLE API 金鑰或試算表 ID 尚未設定！")

    creds = json.loads(creds_json)
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)
    client = gspread.authorize(credentials)
    return client.open_by_key(sheet_id).sheet1


# ===== 更新訪問計數 =====
def bump_counter():
    sheet = get_gsheet()
    today = datetime.now().strftime("%Y-%m-%d")

    # 讀取試算表資料
    records = sheet.get_all_records()
    today_row = None
    total_count = 0

    if records:
        total_count = sum(r.get("訪問數", 0) for r in records)
        for i, row in enumerate(records, start=2):
            if row["日期"] == today:
                today_row = i
                break

    # 更新今日數字
    if today_row:
        new_value = records[today_row - 2]["訪問數"] + 1
        sheet.update_cell(today_row, 2, new_value)
    else:
        new_value = 1
        sheet.append_row([today, new_value])

    total_count = total_count + 1
    return {"today": new_value, "total": total_count}