import re
from pathlib import Path

body = Path("_tpl_body_v2.html").read_text(encoding="utf-8")

# 打印 monitors section 的完整内容
m_match = re.search(r"<section id=\"monitors\".*?</section>", body, re.DOTALL)
if m_match:
    print("=== MONITORS SECTION ===")
    print(m_match.group(0))

# 打印 studio section 及其后的几行
s_match = re.search(r"<section id=\"studio\".*?</section>", body, re.DOTALL)
if s_match:
    print("\n=== STUDIO SECTION TAIL ===")
    lines = s_match.group(0).splitlines()
    print("\n".join(lines[-8:]))
