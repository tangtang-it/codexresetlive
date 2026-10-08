import json
import urllib.request
from PIL import Image

# 我们可以直接写一个简短脚本，通过 headless chrome 用 script 打印出 rect
import subprocess

js_code = """
const el = document.querySelector("#studio .studio-col:nth-child(2) .col-header");
const r = el.getBoundingClientRect();
console.log("RECT:" + JSON.stringify({x: r.x, y: r.y, w: r.width, h: r.height}));
"""

# 用 Chrome 打印出位置
cmd = [
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "--headless=new",
    "--disable-gpu",
    "--window-size=1280,1800",
    "--run-all-compositor-stages-before-draw",
    "http://localhost:8080/"
]

# 直接检查完整截图中的 studio 区域
img = Image.open("tibo_avatar_full.png")
print("Image size:", img.size)

# 我们找一下头像和文字的大致像素范围并裁出几张预览
# Studio 标题栏大概在 y: 680~740
# 第一列 ~ 第三分之一
# 第二列 ~ x: 440 ~ 840
c1 = img.crop((440, 680, 840, 760))
c1.save("tibo_avatar_col2_header.png")
print("Saved tibo_avatar_col2_header.png with size:", c1.size)

# 整个 studio 区域三列概览
c2 = img.crop((40, 640, 1240, 1220))
c2.save("tibo_avatar_studio_3col.png")
print("Saved tibo_avatar_studio_3col.png with size:", c2.size)