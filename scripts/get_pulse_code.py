import re
from pathlib import Path

content = Path("scripts/build_studio.py").read_text(encoding="utf-8")
m = re.search(r"pulse_svg = f?'''(.*?)'''", content, re.DOTALL)
if m:
    print(m.group(0))
