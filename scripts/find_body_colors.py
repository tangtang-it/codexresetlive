import re
from pathlib import Path

content = Path("_tpl_body_v2.html").read_text(encoding="utf-8")
colors = set(re.findall(r"#[0-9a-fA-F]{6}", content))
print("Hex colors in _tpl_body_v2.html:")
for c in sorted(colors):
    cnt = content.count(c)
    print(f"  {c}: {cnt} times")
