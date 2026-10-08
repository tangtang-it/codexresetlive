import re
from pathlib import Path

body = Path("_tpl_body_v2.html").read_text(encoding="utf-8")
placeholders = re.findall(r"(__[A-Z0-9_]+__)", body)
print("Placeholders in _tpl_body_v2.html:", len(set(placeholders)))
print(sorted(list(set(placeholders))))
