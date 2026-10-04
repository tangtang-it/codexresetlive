import urllib.request
import re
import json
import os

URL = "https://opentherank.com/codex-reset/"
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
with urllib.request.urlopen(req, timeout=45) as r:
    html = r.read().decode("utf-8", errors="replace")

# 1. Parse all cx-post articles
posts = []
for m in re.finditer(r'<article class="cx-post" id="r-(\d+)"([^>]*)>(.*?)</article>', html, re.DOTALL):
    tid = m.group(1)
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
        "url": "https://x.com/thsottiaux/status/" + tid
    })

# 2. Calendar stamps (gives full set of dates even if post list truncated)
stamps = []
for m in re.finditer(r'data-id="(\d+)"\s+data-at="([^"]+)"\s+data-type="([^"]+)"', html):
    stamps.append({"id": m.group(1), "at": m.group(2), "type": m.group(3)})

# Merge unique by id, prefer post data (has text)
merged = {}
for s in stamps:
    merged[s["id"]] = {"id": s["id"], "at": s["at"], "type": s["type"], "status": "confirmed", "text": "", "url": "https://x.com/thsottiaux/status/" + s["id"]}
for p in posts:
    if p["id"] in merged:
        merged[p["id"]].update({"text": p["text"], "type": p["type"], "status": p["status"], "at": p["at"] or merged[p["id"]]["at"]})
    else:
        merged[p["id"]] = p

records = sorted(merged.values(), key=lambda x: x["at"])
print("TOTAL_RECORDS:", len(records))
print("WITH_TEXT:", sum(1 for r in records if r["text"]))
print("BANKED:", sum(1 for r in records if r["type"] == "banked"))
print("LATEST:", records[-1] if records else None)
print("OLDEST:", records[0] if records else None)

out_dir = r"D:/ZySpace/zy_code/seo/codexlimit/data"
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "tibo_reset_history.json"), "w", encoding="utf-8") as f:
    json.dump({
        "source": URL,
        "scraped_at_utc": "2026-10-04",
        "author": {"name": "Thibault \"Tibo\" Sottiaux", "handle": "@thsottiaux"},
        "total": len(records),
        "records": records
    }, f, ensure_ascii=False, indent=2)
print("WROTE:", os.path.join(out_dir, "tibo_reset_history.json"))
