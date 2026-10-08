import re
from pathlib import Path

body = Path("_tpl_body_v2.html").read_text(encoding="utf-8")
head = Path("_tpl_head_v2.html").read_text(encoding="utf-8")

# 检查 verify_site.py 里要求的类名是否存在于 _tpl_body_v2.html
target_classes = [
    "direct-ans-banner", "gauge-wrap", "chart-svg-wrap", "studio-grid",
    "cal-table", "guides-grid", "monitor-grid", "tools", "faq", "footer-dir"
]

print("Target classes check in body:")
for tc in target_classes:
    print(f"  {tc}: {tc in body}")
