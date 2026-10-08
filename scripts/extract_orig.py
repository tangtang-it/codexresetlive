import subprocess
from pathlib import Path

orig = subprocess.check_output(["git", "show", "HEAD:_tpl_head_v2.html"], encoding="utf-8")
Path("_tpl_head_v2_orig.html").write_text(orig, encoding="utf-8")
print("Saved _tpl_head_v2_orig.html, size:", len(orig))
