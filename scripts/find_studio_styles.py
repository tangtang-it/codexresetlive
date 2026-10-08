import re
from pathlib import Path

head = Path("_tpl_head_v2.html").read_text(encoding="utf-8")
matches = re.findall(r"([^{}]+studio-[^{}]+{[^{}]+})", head)
for m in matches:
    print(m.strip())
