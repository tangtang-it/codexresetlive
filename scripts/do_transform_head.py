import re
from pathlib import Path

content = Path("_tpl_head_v2_orig.html").read_text(encoding="utf-8")

# 1. 引入 Inter 和 JetBrains Mono
fonts_tag = """<!-- High-Trust Engineering Typography: Inter & JetBrains Mono -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
"""
if "fonts.googleapis.com" not in content:
    content = content.replace("<style>", fonts_tag + "\n<style>")

# 2. 替换 :root 变量池为完整的 Linear Design System
old_root = re.search(r":root{([^}]+)}", content)
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

if old_root:
    content = content.replace(old_root.group(0), linear_root)

# 3. 颜色与透明度精准转换
# 替换原有的 Binance 黄色透明度为 Linear Lavender 蓝紫透明度
content = re.sub(r"rgba(252,s*213,s*53,s*([0-9.]+))", r"rgba(94, 106, 210, \g<1>)", content)

# 替换绿色透明度为 Linear Emerald 翠绿
content = re.sub(r"rgba(14,s*203,s*129,s*([0-9.]+))", r"rgba(39, 166, 68, \g<1>)", content)

# 替换硬编码的 Binance 黄色与橙色
content = content.replace("#FCD535", "#5e6ad2")
content = content.replace("#f0b90b", "#4f5bb5")
content = content.replace("#0ecb81", "#27a644")
content = content.replace("#2b3139", "#23252a")
content = content.replace("#1e2329", "#0f1011")
content = content.replace("#0b0e11", "#010102")
content = content.replace("#707a8a", "#8a8f98")

# 4. 优化导航栏为深黑高斯模糊
content = content.replace("background:rgba(11,14,17,.92);", "background:rgba(1,1,2,.85);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);")
content = content.replace("background:rgba(11,14,17,.92)", "background:rgba(1,1,2,.85);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)")

# 5. 严格保护所有图标尺寸限制！绝不允许任何 SVG 无限放大！
# 确保 svg 尺寸全局防御性兜底
svg_safety_css = """
/* SVG Global Dimension Guardrails */
svg:not([width]):not([height]) {
  max-width: 100%;
}
.ico, .ico svg {
  width: 15px !important;
  height: 15px !important;
  display: inline-block;
  vertical-align: -2px;
}
.tool-ic svg {
  width: 18px !important;
  height: 18px !important;
}
.leg-item svg {
  width: 16px !important;
  height: 16px !important;
  flex-shrink: 0;
}
.dab-stamp {
  width: 86px !important;
  height: 86px !important;
  max-width: 86px !important;
  max-height: 86px !important;
  flex-shrink: 0;
}
.dab-stamp svg {
  width: 86px !important;
  height: 86px !important;
}
.brand-mark svg {
  width: 20px !important;
  height: 20px !important;
}
.channel-pills svg {
  width: 13px !important;
  height: 13px !important;
}
"""
content = content.replace("</style>", svg_safety_css + "\n</style>")

# 6. 为卡片增加 Linear 标志性的顶边微高光
content = content.replace("border:1px solid var(--hairline);", "border:1px solid var(--hairline);box-shadow:inset 0 1px 0 rgba(255,255,255,0.05);")

# 7. 全局负字距与排版
content = content.replace("body{background:var(--canvas);color:var(--body);font-family:var(--font);font-size:14px;line-height:1.5;",
                          "body{background:var(--canvas);color:var(--body);font-family:var(--font);font-size:14px;line-height:1.5;letter-spacing:-0.01em;")

Path("_tpl_head_v2.html").write_text(content, encoding="utf-8")
print("Transformed _tpl_head_v2.html with 100% v2 compatibility & Linear fidelity! Size:", len(content))
