import re
from pathlib import Path

body_path = Path("_tpl_body_v2.html")
content = body_path.read_text(encoding="utf-8")

# 1. 提取完整的 monitors section
monitors_pattern = r"(<section id=\"monitors\">.*?</section>)"
m = re.search(monitors_pattern, content, re.DOTALL)
if not m:
    print("ERROR: Could not find monitors section")
    exit(1)

monitors_block = m.group(1)

# 将 monitors 的编号从 05 改为 02
monitors_block = re.sub(r'<span class="sec-kick">05 [^<]+</span>', '<span class="sec-kick">02 — Authority & Proximity</span>', monitors_block)

# 2. 从原文本中删除 monitors section（连带紧随其后的空白或换行）
content = content.replace(m.group(0), "")

# 3. 找到 studio section 的结束位置 </section>
studio_pattern = r"(<section id=\"studio\">.*?</section>)"
s = re.search(studio_pattern, content, re.DOTALL)
if not s:
    print("ERROR: Could not find studio section")
    exit(1)

studio_block = s.group(1)

# 将 monitors_block 插入到 studio_block 紧随其后
replacement = studio_block + "\n\n" + monitors_block
content = content.replace(studio_block, replacement, 1)

# 4. 依次调整后续 section 的编号，保持自然递增连贯：
# calendar-grid 从 02 改为 03
content = re.sub(r'<span class="sec-kick">02 — Calendar Radar</span>', '<span class="sec-kick">03 — Calendar Radar</span>', content)
# calculator 从 03 改为 04
content = re.sub(r'<span class="sec-kick">03 — Personal Engine</span>', '<span class="sec-kick">04 — Personal Engine</span>', content)
# guides 从 04 改为 05
content = re.sub(r'<span class="sec-kick">04 — Deep Dive</span>', '<span class="sec-kick">05 — Deep Dive</span>', content)
# tools 保持 06，faq 保持 07

body_path.write_text(content, encoding="utf-8")
print("Successfully reordered sections in _tpl_body_v2.html!")
