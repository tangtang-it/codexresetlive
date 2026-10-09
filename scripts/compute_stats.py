# -*- coding: utf-8 -*-
import json, math
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

p = DATA_DIR / "tibo_reset_history.json"
with open(p, encoding="utf-8") as f:
    data = json.load(f)
recs = sorted(data["records"], key=lambda x: x["at"])

def pt(ts):
    return datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")

# Only actual quota reset announcements (regular or banked)
reset_recs = [r for r in recs if r.get("type") in ["regular", "banked", "both"]]
last = reset_recs[-1] if reset_recs else recs[-1]
now = datetime.now(timezone.utc).replace(tzinfo=None)
days_since = round((now - pt(last["at"])).total_seconds() / 86400, 1)

gaps = [(pt(reset_recs[i]["at"]) - pt(reset_recs[i-1]["at"])).total_seconds()/86400 for i in range(1, len(reset_recs))]
recent_gaps = gaps[-14:] if len(gaps) >= 14 else gaps
avg_recent = round(sum(recent_gaps)/len(recent_gaps), 1) if recent_gaps else 3.4
avg_all = round(sum(gaps)/len(gaps), 1) if gaps else 6.8

# Continuous smooth hazard sigmoid model
def calc_probability(d):
    p_val = 11.0 + (74.0 / (1.0 + math.exp(-1.8 * (max(0.0, d) - 2.0))))
    return max(10, min(85, int(round(p_val))))

prob = calc_probability(days_since)

# Count months only for actual quota reset events
months = Counter(r["at"][:7] for r in reset_recs)
banked = sum(1 for r in reset_recs if r["type"] == "banked")
regular = sum(1 for r in reset_recs if r["type"] == "regular")

series = []
y, m = 2025, 9
while (y, m) <= (2026, 10):
    k = f"{y:04d}-{m:02d}"
    series.append({"month": k, "count": months.get(k, 0)})
    m += 1
    if m > 12:
        m = 1; y += 1

out = {
    "total": len(recs),  # Total monitored posts across all categories (60)
    "reset_count": len(reset_recs), # Total actual resets (58)
    "regular": regular,
    "banked": banked,
    "last_reset_at": last["at"],
    "last_reset_text": last["text"],
    "last_reset_url": last["url"],
    "first_reset_at": reset_recs[0]["at"] if reset_recs else recs[0]["at"],
    "days_since_last_reset": days_since,
    "avg_gap_days_all": avg_all,
    "avg_gap_days_recent": avg_recent,
    "probability_48h": int(prob),
    "monthly_series": series,
    "monthly_max": max(s["count"] for s in series) or 1
}

out_file = DATA_DIR / "radar_stats.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Computed stats: total={len(recs)}, resets={len(reset_recs)}, days_since={days_since}d, prob={prob}%")
