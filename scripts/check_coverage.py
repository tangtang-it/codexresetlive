import re
from pathlib import Path

content = Path("site/index.html").read_text(encoding="utf-8")

# 检查几个核心容器类名在 CSS 中是否有对应的样式定义
css = re.search(r"<style>(.*?)</style>", content, re.DOTALL).group(1)

test_classes = [
    "hdr", "brand", "brand-mark", "direct-ans-banner", "gauge-wrap",
    "chart-svg-wrap", "studio-grid", "col-card", "cal-table", "calc-card",
    "linear-slider", "guides-grid", "monitor-grid", "faq-card", "footer-dir",
    "move-item", "post-mini", "switch-item"
]

print("Class styling coverage check:")
for c in test_classes:
    has_css = ("." + c) in css
    has_html = ('class="' in content and c in content)
    print(f"  .{c:20s} -> in CSS: {str(has_css):5s} | in HTML: {has_html}")
