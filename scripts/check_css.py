from pathlib import Path
import re

head = Path("_tpl_head_v2.html").read_text(encoding="utf-8")
body = Path("_tpl_body_v2.html").read_text(encoding="utf-8")

# 查看 CSS 中涉及颜色、卡片、按钮、导航的规则
css = re.search(r"<style>(.*?)</style>", head, re.DOTALL).group(1)

# 打印出主要选择器名称
selectors = re.findall(r"(.[a-zA-Z0-9_-]+)s*{", css)
print("Unique CSS classes defined:", len(set(selectors)))
print("Samples:", sorted(list(set(selectors)))[:40])
