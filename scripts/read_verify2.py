from pathlib import Path
v = Path("scripts/verify_site.py").read_text(encoding="utf-8")
print(v[1000:])
