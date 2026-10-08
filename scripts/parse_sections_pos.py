import re
from pathlib import Path

body = Path("_tpl_body_v2.html").read_text(encoding="utf-8")

# 寻找所有 section 块的开始和结束
sections = re.findall(r"(<section[^>]*id=\"([^\"]+)\"[^>]*>.*?</section>)", body, re.DOTALL)
print(f"Total id sections found: {len(sections)}")
for s, sid in sections:
    print(f"Section id: {sid}, length: {len(s)}")
