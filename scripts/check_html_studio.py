import subprocess, json

# 我们可以用 edge 截屏，也可以用 python 写一个简单的测量脚本
# 检查 site/zh-hans/index.html 里面的实际 CSS
content = open("site/zh-hans/index.html", encoding="utf-8").read()
import re
print("Checking studio-grid in generated HTML:")
for line in content.splitlines():
    if "studio-grid" in line or "studio-col" in line:
        print("  ", line[:100])
