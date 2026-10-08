import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

h = Path("_tpl_head_v2.html").read_text(encoding="utf-8")
style = h[h.find("<style>")+7:h.find("</style>")]

# 找到所有的注释
comments = re.findall(r"/\*+([^*]+(?:\*+[^/*][^*]*)*)\*+/", style)
print(f"Total comments: {len(comments)}")
for c in comments[:25]:
    c_clean = c.strip()
    if len(c_clean) < 80:
        print("/* " + c_clean + " */")
