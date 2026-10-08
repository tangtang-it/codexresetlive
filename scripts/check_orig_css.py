import re
from pathlib import Path

orig_head = Path("_tpl_head.html").read_text(encoding="utf-8")
print("Original _tpl_head.html size:", len(orig_head))
orig_css = re.search(r"<style>(.*?)</style>", orig_head, re.DOTALL).group(1)
orig_selectors = set(re.findall(r"(.[a-zA-Z0-9_-]+)", orig_css))
print("Original selectors count:", len(orig_selectors))
