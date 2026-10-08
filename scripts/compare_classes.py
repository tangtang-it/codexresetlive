import re
from pathlib import Path

content = Path("site/index.html").read_text(encoding="utf-8")

# 提取 HTML 中的所有 class
classes = set(re.findall(r'class="([^"]+)"', content))
all_classes = set()
for c in classes:
    for item in c.split():
        all_classes.add(item)

# 提取 CSS 中的所有选择器
css = re.search(r"<style>(.*?)</style>", content, re.DOTALL).group(1)
css_classes = set(re.findall(r'\.([a-zA-Z0-9_\-]+)', css))

missing = all_classes - css_classes
print(f"Total HTML classes: {len(all_classes)}")
print(f"Total CSS classes: {len(css_classes)}")
print(f"HTML classes without CSS rules: {len(missing)}")
print("Sample missing classes:")
for m in sorted(list(missing))[:35]:
    print(" -", m)
