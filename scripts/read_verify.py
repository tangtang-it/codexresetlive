from pathlib import Path
v = Path("scripts/verify_site.py").read_text(encoding="utf-8")
print("verify_site.py length:", len(v))
print(v[:1000])
