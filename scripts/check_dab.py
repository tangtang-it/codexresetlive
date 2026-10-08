import re
from pathlib import Path

orig = Path("_tpl_head_v2_orig.html").read_text(encoding="utf-8")

# 检查 dab-stamp 和 direct-ans-banner 的定义
for line in orig.splitlines():
    if any(k in line for k in [".dab-stamp", ".direct-ans-banner", ".dab-right", ".leg-item svg", ".dual-cards"]):
        print(line[:120])
