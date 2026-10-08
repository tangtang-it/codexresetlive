import re
from pathlib import Path

b = Path("scripts/build_studio.py").read_text(encoding="utf-8")
funcs = re.findall(r"def (render_[a-zA-Z0-9_]+|get_[a-zA-Z0-9_]+|build_[a-zA-Z0-9_]+)", b)
print("Rendering functions in build_studio.py:")
for f in set(funcs):
    print(" -", f)

# 检查 pulse_svg 定义
m_pulse = re.search(r"pulse_svg = f?'''(.*?)'''", b, re.DOTALL)
if m_pulse:
    print("\nFound pulse_svg definition, length:", len(m_pulse.group(1)))
