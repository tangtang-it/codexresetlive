import re
from pathlib import Path

content = Path("scripts/build_studio.py").read_text(encoding="utf-8")
colors = set(re.findall(r"#[0-9a-fA-F]{6}", content))
print("Hex colors in build_studio.py:")
for c in sorted(colors):
    cnt = content.count(c)
    print(f"  {c}: {cnt} times")
