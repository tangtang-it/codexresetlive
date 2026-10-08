import urllib.request, re
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
    print("Found text lines:", len(parser.text))
    full = "\n".join(parser.text)
    # 查找关于黏土拟态的描述
    for part in full.split("\n"):
        if any(k in part for k in ["黏土", "拟态", "Clay", "阴影", "圆角", "风格", "特征", "色彩"]):
            print(part[:100])
except Exception as e:
    print("Error:", e)
