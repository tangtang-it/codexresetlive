import re
from pathlib import Path

content = Path("site/index.html").read_text(encoding="utf-8")

# 检查是否包含关键 Linear 风格色彩
linear_checks = [
    "--canvas:#010102" in content,
    "--primary:#5e6ad2" in content,
    "--surface-1:#0f1011" in content,
    "--hairline:#23252a" in content,
    "fonts.googleapis.com" in content,
    "Inter" in content,
    "JetBrains Mono" in content,
    "#5e6ad2" in content, # SVG pulse
    "#27a644" in content, # SVG pulse
    "#FCD535" not in content # 无旧 Binance 黄色
]

print("Linear Theme Verification:")
labels = [
    "Canvas #010102 present",
    "Primary #5e6ad2 present",
    "Surface-1 #0f1011 present",
    "Hairline #23252a present",
    "Google Fonts connected",
    "Inter font configured",
    "JetBrains Mono configured",
    "Linear Lavender in SVG pulse",
    "Emerald in SVG pulse",
    "No legacy Binance #FCD535 in index.html"
]

for l, ok in zip(labels, linear_checks):
    print(f"  [{'PASS' if ok else 'FAIL'}] {l}")
