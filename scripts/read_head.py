import sys
from pathlib import Path

# 将输出设为 utf-8 避免 gbk 错误
sys.stdout.reconfigure(encoding="utf-8")

h = Path("_tpl_head_v2.html").read_text(encoding="utf-8")
print("Total head length:", len(h))
# 打印 head 的 meta 标签和结构
print("Head before <style>:")
print(h[:h.find("<style>")])
