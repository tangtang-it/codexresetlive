# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

print("=== [SUBAGENT QA AUDIT] CALENDAR & RADAR VERIFICATION ===")

zh_html = Path("site/zh-hans/index.html").read_text(encoding="utf-8")
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

# 1. Total monitored posts vs actual resets
check("Total Monitored Posts", hist["total"] == 60, f"Expected 60, got {hist['total']}")
check("Tibo Watch in HTML", "60 Posts" in zh_html, "Found '60 Posts' in zh-hans HTML")

# 2. Check that announcements are typed as release/announcement and NOT on the reset calendar
d4_rec = next(r for r in hist["records"] if r["id"] == "2108476123456789012")
check("Day 4 Tweet Type is 'release'", d4_rec["type"] == "release", f"Type is {d4_rec['type']}")

chatgpt_rec = next(r for r in hist["records"] if r["id"] == "2108548123456789013")
check("ChatGPT Tweet Type is 'announcement'", chatgpt_rec["type"] == "announcement", f"Type is {chatgpt_rec['type']}")

# 3. Check calendar JSON embedded in page
resets_match = re.search(r'var resets = ([.*?]);', zh_html)
check("Calendar JSON Present", bool(resets_match), "Found embedded calendar JSON")
if resets_match:
    resets_data = json.loads(resets_match.group(1))
    has_fake_oct9_reset = any(r["d"] == "2026-10-09" for r in resets_data)
    check("No Fake Reset on Oct 9 (Today)", not has_fake_oct9_reset, "Confirmed Oct 9 has NO reset stamp on calendar")
    
    has_fake_day4_reset = any(r["d"] == "2026-10-08" and "19:24" in r.get("l", "") for r in resets_data)
    check("No Fake Reset for Day 4 on Oct 8", not has_fake_day4_reset, "Confirmed Day 4 release is not labeled as a Hard Reset")
    
    oct_resets = [r for r in resets_data if r["d"].startswith("2026-10")]
    check("October Total Resets Count", len(oct_resets) == 4, f"Expected 4 true resets in Oct, got {len(oct_resets)}")

print(f"\n=== [SUBAGENT QA AUDIT] RESULT: {passed} PASSED, {failed} FAILED ===")
