import re
from pathlib import Path

orig = Path("_tpl_head_v2_orig.html").read_text(encoding="utf-8")
curr = Path("_tpl_head_v2.html").read_text(encoding="utf-8")

orig_selectors = set(re.findall(r"([.#][a-zA-Z0-9_-]+)s*{", orig))
curr_selectors = set(re.findall(r"([.#][a-zA-Z0-9_-]+)s*{", curr))

diff_lost = orig_selectors - curr_selectors
print("Selectors in orig but lost in curr:", len(diff_lost))
for s in sorted(list(diff_lost)):
    print(" -", s)
