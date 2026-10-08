import re
from pathlib import Path

content = Path("scripts/build_studio.py").read_text(encoding="utf-8")

# 查找 pulse_svg
m = re.search(r"(pulse_svg = f?'''.*?''')", content, re.DOTALL)
if m:
    print("Found pulse_svg, lines:", len(m.group(1).splitlines()))
    print(m.group(1)[:500])

# 查找 p4_body_custom
m2 = re.search(r"(p4_body_custom = f?'''.*?''')", content, re.DOTALL)
if m2:
    print("\nFound p4_body_custom, lines:", len(m2.group(1).splitlines()))
    print(m2.group(1)[:500])
