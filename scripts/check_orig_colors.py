import re
from pathlib import Path

content = Path("_tpl_head.html").read_text(encoding="utf-8")
colors = set(re.findall(r"#[0-9a-fA-F]{6}|rgba?([^)]+)", content))
print("Colors found in original _tpl_head.html:")
for c in sorted(colors):
    cnt = content.count(c)
    print(f"  {c:28s}: {cnt} times")
