import json
from datetime import datetime
from collections import Counter

p = r"D:/ZySpace/zy_code/seo/codexlimit/data/tibo_reset_history.json"
with open(p, encoding="utf-8") as f:
    data = json.load(f)
recs = sorted(data["records"], key=lambda x: x["at"])

def pt(ts):
    return datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")

last = recs[-1]
now = datetime(2026, 10, 4, 12, 0, 0)
days_since = round((now - pt(last["at"])).total_seconds() / 86400, 1)

gaps = [(pt(recs[i]["at"]) - pt(recs[i-1]["at"])).total_seconds()/86400 for i in range(1, len(recs))]
recent_gaps = gaps[-14:]
avg_recent = round(sum(recent_gaps)/len(recent_gaps), 1)
avg_all = round(sum(gaps)/len(gaps), 1)

# Four-factor smooth probability model aligned with willcodexreset.com standard
# 1. Base baseline (preserves space for consecutive/double resets)
baseline = 12

# 2. Cooldown vs overdue factor
if days_since <= 2.0:
    cooldown_factor = -4  # Recent reset cooldown
elif days_since <= 4.0:
    cooldown_factor = +6  # Nearing typical cadence
else:
    cooldown_factor = min(40, round((days_since - 4) * 8.5))  # Overdue escalation

# 3. Product & social release signal hint (Tibo mentioned upcoming next week rollout)
signal_hint = 3

prob = max(10, min(85, round(baseline + cooldown_factor + signal_hint)))

months = Counter(r["at"][:7] for r in recs)
banked = sum(1 for r in recs if r["type"] == "banked")
regular = sum(1 for r in recs if r["type"] == "regular")

series = []
y, m = 2025, 9
while (y, m) <= (2026, 10):
    k = f"{y:04d}-{m:02d}"
    series.append({"month": k, "count": months.get(k, 0)})
    m += 1
    if m > 12:
        m = 1; y += 1

out = {
    "total": len(recs),
    "regular": regular,
    "banked": banked,
    "last_reset_at": last["at"],
    "last_reset_text": last["text"],
    "last_reset_url": last["url"],
    "first_reset_at": recs[0]["at"],
    "days_since_last_reset": days_since,
    "avg_gap_days_all": avg_all,
    "avg_gap_days_recent": avg_recent,
    "probability_48h": int(prob),
    "monthly_series": series,
    "monthly_max": max(s["count"] for s in series) or 1
}
print(json.dumps(out, ensure_ascii=False, indent=2))
with open(r"D:/ZySpace/zy_code/seo/codexlimit/data/radar_stats.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
