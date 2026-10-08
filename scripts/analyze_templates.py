import re
from pathlib import Path

head = Path("_tpl_head_v2.html").read_text(encoding="utf-8")
body = Path("_tpl_body_v2.html").read_text(encoding="utf-8")
build = Path("scripts/build_studio.py").read_text(encoding="utf-8")

print(f"HEAD size: {len(head)}, lines: {len(head.splitlines())}")
print(f"BODY size: {len(body)}, lines: {len(body.splitlines())}")
print(f"BUILD size: {len(build)}, lines: {len(build.splitlines())}")

# 提取关键 CSS 变量
css_vars = re.findall(r"(--[a-zA-Z0-9-]+):([^;]+);", head)
print("CSS Variables:")
for k, v in css_vars:
    print(f"  {k}: {v.strip()}")
