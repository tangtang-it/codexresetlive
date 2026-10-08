import re
from pathlib import Path

body_path = Path("_tpl_body_v2.html")
c = body_path.read_text(encoding="utf-8")

# 查看 #FCD535 出现的行和上下文
for i, line in enumerate(c.splitlines(), 1):
    if "#FCD535" in line or "#0ecb81" in line or "#f6465d" in line:
        print(f"Line {i}: {line.strip()[:100]}")
