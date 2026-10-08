from pathlib import Path

content = Path("site/index.html").read_text(encoding="utf-8")
for i, line in enumerate(content.splitlines(), 1):
    if "#FCD535" in line:
        print(f"Line {i}: {line.strip()[:120]}")
