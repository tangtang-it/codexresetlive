import re
from pathlib import Path

orig = Path("_tpl_head.html").read_text(encoding="utf-8")

# 1. 替换 Typography 和 Google Fonts
fonts_tag = """<!-- High-Trust Engineering Typography: Inter & JetBrains Mono -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
"""

if "fonts.googleapis.com" not in orig:
    orig = orig.replace("<style>", fonts_tag + "\n<style>")

# 2. 替换 :root 变量
old_root_match = re.search(r":root{([^}]+)}", orig)
if old_root_match:
    linear_root = """:root{
/* Linear Surface Ladder (VoltAgent/awesome-design-md) */
--canvas:#010102;
--surface-1:#0f1011;
--surface-2:#141516;
--surface-3:#18191a;
--surface-4:#1c1d1f;

/* Surface Aliases */
--card:#0f1011;
--elevated:#141516;
--hairline:#23252a;
--hairline-strong:#34343a;
--hairline-tertiary:#3e3e44;
--edge-highlight:inset 0 1px 0 rgba(255,255,255,0.06);

/* Linear Signature Brand Accent: Lavender-Blue */
--primary:#5e6ad2;
--primary-active:#4f5bb5;
--primary-hover:#828fff;
--primary-focus:#5e69d1;
--primary-disabled:#222438;
--primary-glow:rgba(94,106,210,0.18);
--on-primary:#ffffff;

/* Ink & Typography */
--ink:#f7f8f8;
--body:#d0d6e0;
--muted:#8a8f98;
--muted-strong:#a0a6b2;
--on-dark:#f7f8f8;

/* Semantic Status */
--up:#27a644;
--up-glow:rgba(39,166,68,0.18);
--down:#ef4444;
--info:#5e6ad2;
--cyan:#38bdf8;
--warning:#f59e0b;

/* Radii Scale */
--r-sm:4px;--r-md:6px;--r-lg:8px;--r-xl:12px;--r-2xl:16px;--r-pill:9999px;

/* High-Trust Font Stacks */
--font:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
--mono:"JetBrains Mono",ui-monospace,"SF Mono","Cascadia Mono",Menlo,Consolas,monospace;
}"""
    orig = orig.replace(old_root_match.group(0), linear_root)

# 3. 替换颜色与质感
# 替换原有的 Binance 黄色透明度为 Linear Lavender 蓝紫透明度
orig = re.sub(r"rgba(252,s*213,s*53,s*([0-9.]+))", r"rgba(94, 106, 210, \g<1>)", orig)

# 替换绿色透明度
orig = re.sub(r"rgba(14,s*203,s*129,s*([0-9.]+))", r"rgba(39, 166, 68, \g<1>)", orig)

# 替换顶部导航背景
orig = orig.replace("background:rgba(11,14,17,.92)", "background:rgba(1,1,2,.85);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)")

# 替换硬编码的 Binance 滚动条
orig = orig.replace("rgba(252, 213, 53, 0.7)", "rgba(94, 106, 210, 0.7)")
orig = orig.replace("rgba(252, 213, 53, 0.4)", "rgba(94, 106, 210, 0.4)")

# 给所有的卡片增加 Linear 标志性的内嵌顶边微高光
orig = orig.replace("border:1px solid var(--hairline);", "border:1px solid var(--hairline);box-shadow:inset 0 1px 0 rgba(255,255,255,0.05);")
orig = orig.replace("border:1px solid var(--card);", "border:1px solid var(--hairline);box-shadow:inset 0 1px 0 rgba(255,255,255,0.05);")

# 增加全局负字距与更佳字体表现
orig = orig.replace("body{background:var(--canvas);color:var(--body);font-family:var(--font);font-size:14px;line-height:1.5;", 
                    "body{background:var(--canvas);color:var(--body);font-family:var(--font);font-size:14px;line-height:1.5;letter-spacing:-0.01em;")

# 给大标题增加 Linear Negative Tracking
orig = orig.replace("h1{", "h1{letter-spacing:-0.035em;")
orig = orig.replace("h2{", "h2{letter-spacing:-0.025em;")
orig = orig.replace("h3{", "h3{letter-spacing:-0.015em;")

Path("_tpl_head_v2.html").write_text(orig, encoding="utf-8")
print("Successfully generated full-fidelity Linear _tpl_head_v2.html! Size:", len(orig))
