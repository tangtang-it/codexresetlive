import json
import os
import re
from datetime import datetime, timezone
import sys
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = DATA_DIR / "tibo_reset_history.json"

URL = "https://opentherank.com/codex-reset/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

def is_valid_tweet_id(tid: str) -> bool:
    if not tid or not isinstance(tid, str):
        return False
    if not re.fullmatch(r"[0-9]{18,20}", tid):
        return False
    if "123456789" in tid or "987654321" in tid:
        return False
    if any(digit * 6 in tid for digit in "0123456789"):
        return False
    return True

html = None
openers = [
    urllib.request.build_opener(),
]
if os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY"):
    openers.append(urllib.request.build_opener(urllib.request.ProxyHandler()))
else:
    openers.append(
        urllib.request.build_opener(
            urllib.request.ProxyHandler(
                {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
            )
        )
    )

for opener in openers:
    try:
        req = urllib.request.Request(URL, headers=headers)
        with opener.open(req, timeout=20) as r:
            content = r.read().decode("utf-8", errors="replace")
            if content and len(content) > 1000:
                html = content
                break
    except Exception:
        continue

if not html:
    if CACHE_FILE.exists():
        print("[WARN] Fetch failed or empty response. Falling back to existing cache.")
        sys.exit(0)
    else:
        print("[ERROR] Fetch failed and no existing cache.")
        sys.exit(1)

posts = []
post_pattern = r'<article class="cx-post" id="r-([0-9]+)"([^>]*)>(.*?)</article>'
for m in re.finditer(post_pattern, html, re.DOTALL):
    tid = m.group(1)
    if not is_valid_tweet_id(tid):
        print(f"[FILTER] Dropped invalid post tweet id: {tid}")
        continue

    attrs = m.group(2)
    inner = m.group(3)

    dtype = re.search(r'data-type="([^"]+)"', attrs)
    dtype = dtype.group(1) if dtype else "regular"

    status = re.search(r'data-status="([^"]+)"', attrs)
    status = status.group(1) if status else "confirmed"

    tmatch = re.search(r'<time[^>]*datetime="([^"]+)"', inner)
    ts = tmatch.group(1) if tmatch else None

    qmatch = re.search(r'<blockquote[^>]*>(.*?)</blockquote>', inner, re.DOTALL)
    quote = ""
    if qmatch:
        raw = re.sub(r'<[^>]+>', '', qmatch.group(1))
        quote = re.sub(r'\s+', ' ', raw).strip()

    posts.append({
        "id": tid,
        "at": ts,
        "type": dtype,
        "status": status,
        "text": quote,
        "url": "https://x.com/thsottiaux/status/" + tid,
    })

stamps = []
stamp_pattern = r'data-id="([0-9]+)"\s+data-at="([^"]+)"\s+data-type="([^"]+)"'
for m in re.finditer(stamp_pattern, html):
    tid = m.group(1)
    if not is_valid_tweet_id(tid):
        print(f"[FILTER] Dropped invalid stamp tweet id: {tid}")
        continue
    stamps.append({"id": tid, "at": m.group(2), "type": m.group(3)})

existing_records = []
if CACHE_FILE.exists():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            raw_records = existing_data.get("records", [])
            for r in raw_records:
                rid = r.get("id", "")
                if is_valid_tweet_id(rid):
                    existing_records.append(r)
                else:
                    print(f"[GUARD] Purged suspicious/mock tweet ID from cache: {rid}")
    except Exception:
        existing_records = []

merged = {r["id"]: r for r in existing_records}
for s in stamps:
    if s["id"] not in merged:
        merged[s["id"]] = {
            "id": s["id"],
            "at": s["at"],
            "type": s["type"],
            "status": "confirmed",
            "text": "",
            "url": "https://x.com/thsottiaux/status/" + s["id"],
        }
for p in posts:
    if p["id"] in merged:
        merged[p["id"]].update({
            "text": p["text"] or merged[p["id"]].get("text", ""),
            "type": p["type"],
            "status": p["status"],
            "at": p["at"] or merged[p["id"]]["at"],
        })
    else:
        merged[p["id"]] = p

valid_records = []
reset_keywords = ["reset", "quota", "limit", "refill", "banked", "cleared", "propagated", "bonus", "capacity", "day ", "chatgpt", "steering", "release", "announcing", "model"]
for r in merged.values():
    t = r.get("text", "").lower()
    if t:
        if any(k in t for k in reset_keywords):
            valid_records.append(r)
    else:
        valid_records.append(r)

records = sorted(valid_records, key=lambda x: x["at"])
print(f"Total merged records count: {len(records)}")

with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(
        {
            "source": URL,
            "scraped_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "author": {
                "name": 'Thibault "Tibo" Sottiaux',
                "handle": "@thsottiaux",
            },
            "total": len(records),
            "records": records,
        },
        f,
        ensure_ascii=False,
        indent=2,
    )
print(f"Saved verified cache: {CACHE_FILE}")
