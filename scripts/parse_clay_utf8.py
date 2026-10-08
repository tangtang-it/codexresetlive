import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

# 读取之前脚本获取的文本
with open("scripts/fetch_clay.py", "r", encoding="utf-8") as f:
    pass

import urllib.request
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        d = data.strip()
        if d:
            self.text.append(d)

url = "https://spicytater.cn/terms/claymorphism"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
proxy = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"})
opener = urllib.request.build_opener(proxy)

try:
    with opener.open(req, timeout=15) as resp:
        html_content = resp.read().decode("utf-8")
    parser = TextExtractor()
    parser.feed(html_content)
    full = "\n".join(parser.text)
    # 提取正文内容
    for p in full.split("\n"):
        if len(p) > 15:
            print(p)
except Exception as e:
    print("Error:", e)
