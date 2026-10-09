# -*- coding: utf-8 -*-
import json
import re
import sys
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
check("Total Monitored Posts Count Valid", hist["total"] == len(hist["records"]), f"Total count {hist['total']} matches records length")
check("No Mock Tweet IDs in Cache", all("123456789" not in r.get("id", "") for r in hist["records"]), "Confirmed no mock tweet IDs in records")

# 2. Check that latest legitimate tweets have valid X links
latest_rec = hist["records"][-1]
check("Latest Tweet Has Valid ID", re.fullmatch(r"[0-9]{18,20}", latest_rec["id"]) is not None, f"Latest ID: {latest_rec['id']}")

# 3. Check calendar JSON embedded in page
start_pos = zh_html.find("var resets = ")
check("Calendar JSON Marker Found", start_pos != -1, "Found 'var resets = ' marker in zh-hans index.html")
if start_pos != -1:
    end_pos = zh_html.find(";", start_pos)
    resets_str = zh_html[start_pos + len("var resets = "):end_pos].strip()
    try:
        resets_data = json.loads(resets_str)
        check("Calendar JSON Parsed Valid", isinstance(resets_data, list) and len(resets_data) > 0, f"Parsed {len(resets_data)} calendar entries")
        
        has_fake_oct9_reset = any(r.get("d") == "2026-10-09" for r in resets_data)
        check("No Fake Reset on Oct 9 (Today)", not has_fake_oct9_reset, "Confirmed Oct 9 has NO reset stamp on calendar")
        
        oct_resets = [r for r in resets_data if str(r.get("d", "")).startswith("2026-10")]
        check("October Resets Count Valid", len(oct_resets) >= 3, f"Oct legitimate resets: {len(oct_resets)}")
    except Exception as e:
        check("Calendar JSON Parsed Valid", False, f"JSON parse error: {e}")

print(f"\n=== [SUBAGENT QA AUDIT] RESULT: {passed} PASSED, {failed} FAILED ===")
if failed > 0:
    sys.exit(1)
