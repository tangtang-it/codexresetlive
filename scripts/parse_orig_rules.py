import re
from pathlib import Path

content = Path("_tpl_head.html").read_text(encoding="utf-8")
print("Total lines in _tpl_head.html:", len(content.splitlines()))

# 提取关键选择器
css = re.search(r"<style>(.*?)</style>", content, re.DOTALL).group(1)
rules = re.findall(r"([^{}]+){([^{}]+)}", css)
print("Total CSS rules in _tpl_head.html:", len(rules))

for sel, val in rules[:20]:
    print(f"{sel.strip()[:40]} -> {val.strip()[:60]}...")
