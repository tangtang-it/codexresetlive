import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

url = "https://willcodexquotareset.com/api/forecast"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"})
)

with opener.open(req, timeout=15) as r:
    data = json.loads(r.read().decode("utf-8", errors="replace"))

posts = data.get("tiboPosts", [])
print(f"Total tiboPosts: {len(posts)}")
for i, p in enumerate(posts[:8]):
    print(f"[{i}] pubDate: {p.get('pubDate')}")
    print(f"    link: {p.get('link')}")
    print(f"    guid: {p.get('guid')}")
    print(f"    title: {p.get('title')}")
    print(f"    activityType: {p.get('activityType')}")
    print("-" * 50)
