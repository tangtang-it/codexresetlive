import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

h = Path("_tpl_head_v2.html").read_text(encoding="utf-8")
style_match = re.search(r"<style>(.*?)</style>", h, re.DOTALL)
if style_match:
    style = style_match.group(1)
    # 分析主要 section 注释
    sections = re.findall(r"/* ---------- (.*?) ---------- */", style)
    print("CSS Major Sections:")
    for s in sections:
        print(" -", s)
