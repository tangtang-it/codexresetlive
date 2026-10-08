from pathlib import Path
content = Path("scripts/banked_tooltips.py").read_text(encoding="utf-8")
print("banked_tooltips.py length:", len(content))
print("First 40 lines:")
for l in content.splitlines()[:40]:
    print(l)
