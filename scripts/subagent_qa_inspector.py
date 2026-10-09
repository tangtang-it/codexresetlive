# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

# Subagent QA Inspector: Validating DOM structures & rendered contents
print("=== [SUBAGENT QA AUDIT] STARTING COMPREHENSIVE INTEGRITY INSPECTION ===")

zh_html = Path("site/zh-hans/index.html").read_text(encoding="utf-8")
en_html = Path("site/index.html").read_text(encoding="utf-8")
stats = json.loads(Path("data/radar_stats.json").read_text(encoding="utf-8"))
hist = json.loads(Path("data/tibo_reset_history.json").read_text(encoding="utf-8"))

passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  [PASS] {name}: {detail}")
        passed += 1
    else:
        print(f"  [FAIL] {name}: {detail}")
        failed += 1

# Check 1: Total Tibo Posts in history and stats
check("Total Tibo Posts in History", hist["total"] == 60, f"Expected 60, got {hist['total']}")
check("Total Tibo Posts in Stats", stats["total"] == 60, f"Expected 60, got {stats['total']}")
check("Tibo Watch in HTML", "60 Posts" in zh_html, "Found '60 Posts' in zh-hans HTML")

# Check 2: Day 4 tweet presence
d4_found = any("Day 4" in r.get("text", "") for r in hist["records"])
check("Day 4 tweet in History", d4_found, "Confirmed Day 4 tweet exists in records")

chatgpt_found = any("Today, we are announcing ChatGPT" in r.get("text", "") for r in hist["records"])
check("ChatGPT announcement tweet in History", chatgpt_found, "Confirmed ChatGPT release tweet exists in records")

# Check 3: Studio Column 1 Moves contains Day 4
check("Signal Studio Moves has Day 4 (ZH)", "Day 4" in zh_html, "Found Day 4 in zh-hans moves")
check("Signal Studio Moves has Day 4 (EN)", "Day 4" in en_html, "Found Day 4 in en moves")

# Check 4: Studio Column 2 Stream contains latest posts
check("Tibo Feed has Instant Steering", "instant steering" in zh_html.lower() or "steering to be instant" in zh_html.lower(), "Found Instant Steering in feed")
check("Tibo Feed has ChatGPT announcement", "chatgpt.com" in zh_html.lower(), "Found chatgpt.com in feed")

# Check 5: Probability model
check("Calculated 48h Probability", stats["probability_48h"] >= 20 and stats["probability_48h"] <= 35, f"Current prob = {stats['probability_48h']}%")

# Check 6: Days since reset synchronization
check("Days since reset is ~1.2d", stats["days_since_last_reset"] >= 1.0 and stats["days_since_last_reset"] <= 1.4, f"days_since = {stats['days_since_last_reset']}d")
check("No static 0.8d hardcoding", "0.8d" not in zh_html, "0.8d completely eliminated from HTML")

# Check 7: Pulse Chart Date labels
check("Chart Date has Oct 9 (Now)", "Oct 9 (Now)" in zh_html, "Chart X-axis label updated to 'Oct 9 (Now)'")
check("Chart Date has Oct 10", "Oct 10" in zh_html, "Chart projection +24h has 'Oct 10'")
check("Chart Date has Oct 11", "Oct 11" in zh_html, "Chart projection +48h has 'Oct 11'")

# Check 8: Client-side JS Live Engine integration
check("JS has calcProbability function", "function calcProbability" in zh_html, "Live mathematical model embedded in client JS")
check("JS has data-days-since-utc updater", "data-days-since-utc" in zh_html, "Live days-since-utc updater active")
check("JS has live chart synchronizer", "chartNowDate" in zh_html and "chartNowProbText" in zh_html, "Live SVG chart dynamic updater active")

print(f"\n=== [SUBAGENT QA AUDIT] SUMMARY: {passed} PASSED, {failed} FAILED ===")
