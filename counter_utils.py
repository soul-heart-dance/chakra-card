import json
import os
from datetime import datetime

DATA_DIR = "data"
COUNTER_FILE = os.path.join(DATA_DIR, "counter.json")
os.makedirs(DATA_DIR, exist_ok=True)

def update_counter():
    """更新訪問計數並回傳目前統計資料"""
    if not os.path.exists(COUNTER_FILE):
        data = {"total": 0, "dates": {}}
    else:
        try:
            with open(COUNTER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"total": 0, "dates": {}}

    today = datetime.now().strftime("%Y-%m-%d")
    data["total"] += 1
    data["dates"][today] = data["dates"].get(today, 0) + 1

    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data