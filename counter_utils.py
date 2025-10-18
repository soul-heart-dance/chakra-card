# counter_utils.py
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"
COUNTER_FILE = DATA_DIR / "counter.json"
DATA_DIR.mkdir(exist_ok=True)

def _load():
    if COUNTER_FILE.exists():
        return json.loads(COUNTER_FILE.read_text(encoding="utf-8"))
    return {"total": 0, "dates": {}}

def _save(data):
    COUNTER_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def bump_counter():
    """每次開頁＋1。回傳最新資料 dict。"""
    data = _load()
    today = datetime.now().strftime("%Y-%m-%d")
    data["total"] += 1
    data["dates"][today] = data["dates"].get(today, 0) + 1
    _save(data)
    return data

def read_counter():
    """只讀取計數（不+1）。"""
    return _load()