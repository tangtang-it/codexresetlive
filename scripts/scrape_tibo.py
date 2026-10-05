import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = DATA_DIR / "tibo_reset_history.json"

URL = "https://opentherank.com/codex-reset/"
req = urllib.request.Request(
    URL,
    headers={
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    },
)

html = None
try:
  with urllib.request.urlopen(req, timeout=30) as r:
    html = r.read().decode("utf-8", errors="replace")
except Exception as e:
  print(f"[WARN] Fetch failed: {e}. Gracefully falling back to existing cache.")
  sys.exit(0)

if not html:
  print("[WARN] Empty response received. Keeping existing cache.")
  sys.exit(0)

# Parse all cx-post articles
posts = []
for m in re.finditer(
    r'<article class="cx-post" id="r-(d+)"([^>]*)>(.*?)</article>',
    html,
    re.DOTALL,
):
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
    quote = re.sub(r's+', ' ', raw).strip()

  posts.append({
      "id": tid,
      "at": ts,
      "type": dtype,
      "status": status,
      "text": quote,
      "url": "https://x.com/thsottiaux/status/" + tid,
  })

# Calendar stamps
stamps = []
for m in re.finditer(
    r'data-id="(d+)"s+data-at="([^"]+)"s+data-type="([^"]+)"', html
):
  stamps.append({"id": m.group(1), "at": m.group(2), "type": m.group(3)})

# Merge with existing cache if available
existing_records = []
if CACHE_FILE.exists():
  try:
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
      existing_data = json.load(f)
      existing_records = existing_data.get("records", [])
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

records = sorted(merged.values(), key=lambda x: x["at"])
print(f"Total merged records count: {len(records)}")

with open(CACHE_FILE, "w", encoding="utf-8") as f:
  json.dump(
      {
          "source": URL,
          "scraped_at_utc": "2026-10-05",
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
print(f"Saved: {CACHE_FILE}")
