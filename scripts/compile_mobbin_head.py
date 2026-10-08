import re
from pathlib import Path

# 同样以包含完整 147+ 个 v2 类名的原始模板为基准进行 Mobbin 化改造
orig = Path("_tpl_head_v2_orig.html").read_text(encoding="utf-8")

# 1. 引入 Inter Variable 与 JetBrains Mono 字体
fonts_tag = """<!-- Mobbin High-Craft Typography: Inter (Saans variable equivalent) & JetBrains Mono -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;450;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
"""
if "fonts.googleapis.com" not in orig:
    orig = orig.replace("<style>", fonts_tag + "\n<style>")

# 2. 替换 :root 变量池为 Mobbin Design System 规范
old_root = re.search(r":root\{([^}]+)\}", orig)
mobbin_root = """:root{
/* Mobbin Design System Tokens (DESIGN-mobbin.md) */
--canvas: #ffffff;
--canvas-soft: #f3f3f3;
--field: #f0f0f0;
--hairline-soft: #f0f0f0;
--hairline: #e0e0e0;
--accent: #0066ff;

/* Surface Aliases */
--card: #ffffff;
--elevated: #f3f3f3;
--surface-1: #ffffff;
--surface-2: #f3f3f3;

/* Ink Hierarchy */
--primary: #141414;
--on-primary: #ffffff;
--ink: #141414;
--ink-soft: #262626;
--body: #141414;
--muted: #707070;
--muted-strong: #262626;
--on-dark: #141414;
--text-muted: #707070;
--text-faint: #adadad;

/* Status Colors within Mobbin Restraint */
--up: #10b981;
--warning: #f59e0b;
--down: #ef4444;
--info: #0066ff;
--cyan: #0066ff;

/* Mobbin Radius Scale */
--r-none: 0px;
--r-sm: 16px;
--r-md: 24px;
--r-pill: 9999px;
--r-lg: 24px;
--r-xl: 24px;
--r-2xl: 24px;

/* Typography */
--font: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
--mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}"""

if old_root:
    orig = orig.replace(old_root.group(0), mobbin_root)

# 3. 页面全局基础样式（纯白画廊画布，墨水黑文字，无字距调整）
orig = orig.replace("body{background:var(--canvas);color:var(--body);font-family:var(--font);font-size:14px;line-height:1.5;", 
                    "body{background:#ffffff;color:#141414;font-family:var(--font);font-size:15px;line-height:1.45;letter-spacing:0;-webkit-font-smoothing:antialiased;")

# 标题紧密行高与 650 粗度
orig = orig.replace("h1{", "h1{font-weight:700;line-height:1.05;letter-spacing:0;color:#141414;")
orig = orig.replace("h2{", "h2{font-weight:700;line-height:1.13;letter-spacing:0;color:#141414;")
orig = orig.replace("h3{", "h3{font-weight:600;line-height:1.25;letter-spacing:0;color:#141414;")

# 4. Mobbin 标志性悬浮 Stadium Pill 导航栏 (nav-pill)
mobbin_hdr_css = """
.hdr {
  position: sticky;
  top: 14px;
  z-index: 60;
  background: transparent;
  border-bottom: none;
  padding: 0 20px;
  margin-bottom: 24px;
}
.hdr-in {
  max-width: 980px;
  margin: 0 auto;
  background: rgba(243, 243, 243, 0.94);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 9999px;
  border: 1px solid #e0e0e0;
  padding: 8px 18px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: none;
}
.brand-mark {
  width: 32px;
  height: 32px;
  border-radius: 30% !important; /* iOS squircle */
  background: #141414 !important;
  color: #ffffff !important;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none !important;
  box-shadow: none !important;
}
.brand-mark svg {
  width: 18px !important;
  height: 18px !important;
  stroke: #ffffff !important;
}
.brand-name {
  color: #141414 !important;
  font-weight: 700;
  font-size: 15px;
}
.nav-a {
  color: #141414 !important;
  font-weight: 500;
  border-radius: 9999px !important;
  padding: 6px 14px;
  font-size: 14px;
  transition: background 0.15s ease;
}
.nav-a:hover {
  background: #ffffff;
}
.nav-a.active {
  background: #ffffff;
  border: 1px solid #e0e0e0;
}
.live-pill {
  background: #ffffff !important;
  border: 1px solid #e0e0e0 !important;
  border-radius: 9999px !important;
  color: #141414 !important;
  font-size: 12px;
  padding: 4px 10px;
}
.dot-live, .dot {
  background: #0066ff !important; /* Mobbin electric blue */
  box-shadow: none !important;
}
"""

orig = orig.replace(".hdr{position:sticky;top:0;z-index:60;background:rgba(11,14,17,.92);backdrop-filter:blur(12px);", mobbin_hdr_css + "\n.hdr-old{")

# 5. Mobbin 卡片体系：Shadow-free, 24px 圆角, 纯白与软灰色差层级
card_mobbin_css = """
/* Mobbin Shadow-Free Card Geometry */
.card-box, .gauge-wrap, .chart-svg-wrap, .studio-col, .calc, .cal-grid-card, .hist-table-card, .guide-card, .monitor-card {
  background: #ffffff !important;
  border: 1px solid #f0f0f0 !important;
  border-radius: 24px !important;
  box-shadow: none !important;
  padding: 24px !important;
  transition: border-color 0.15s ease;
}
.card-box:hover, .guide-card:hover, .monitor-card:hover {
  border-color: #e0e0e0 !important;
  transform: none !important;
  box-shadow: none !important;
}

/* Featured / Emphasized Containers */
.direct-ans-banner {
  background: #f3f3f3 !important; /* canvas-soft */
  border: 1px solid #e0e0e0 !important;
  border-radius: 24px !important;
  box-shadow: none !important;
  padding: 24px 28px !important;
}

/* 4-item quick readout strip */
.ro-item, .readout-item {
  background: #f3f3f3 !important;
  border: 1px solid #f0f0f0 !important;
  border-radius: 20px !important;
  box-shadow: none !important;
}

/* Inputs & Form Fields (Mobbin Field Tint) */
.alert-input, input, textarea {
  background: #f0f0f0 !important;
  border: none !important;
  border-radius: 16px !important;
  color: #141414 !important;
  box-shadow: none !important;
  padding: 10px 16px !important;
}
.alert-input:focus, input:focus {
  outline: 2px solid #141414 !important;
}

/* Mobbin Buttons: Stadium Pill */
.btn, .btn-primary, button.btn-primary {
  background: #141414 !important;
  color: #ffffff !important;
  border-radius: 9999px !important;
  font-weight: 600 !important;
  padding: 10px 22px !important;
  border: none !important;
  box-shadow: none !important;
  transition: opacity 0.15s ease !important;
}
.btn-primary:hover {
  opacity: 0.88;
}
.btn-ghost, .btn-outline {
  background: #ffffff !important;
  color: #141414 !important;
  border: 1px solid #e0e0e0 !important;
  border-radius: 9999px !important;
  box-shadow: none !important;
}

/* Preset Buttons (Pills) */
.p1, .p2, .p3, .p4, .preset-btn {
  border-radius: 9999px !important;
  background: #f3f3f3 !important;
  color: #141414 !important;
  border: 1px solid #e0e0e0 !important;
  box-shadow: none !important;
}
.p1:hover, .p2:hover, .p3:hover, .p4:hover, .preset-btn:hover {
  background: #141414 !important;
  color: #ffffff !important;
  border-color: #141414 !important;
}

/* Badges & Chips: Stadium Pill */
.badge, .sub-badge, .col-badge, .dab-badge {
  border-radius: 9999px !important;
  box-shadow: none !important;
  font-weight: 600 !important;
}
.badge-popular, .badge-electric {
  background: #0066ff !important;
  color: #ffffff !important;
}

/* Polarity Inversion Footer (Near-black with 24px top radius) */
.ftr, footer {
  background: #141414 !important;
  color: #ffffff !important;
  border-radius: 24px 24px 0 0 !important;
  margin-top: 80px !important;
  padding: 64px 20px 48px !important;
  border-top: none !important;
}
.ftr a, footer a {
  color: #adadad !important;
}
.ftr a:hover, footer a:hover {
  color: #ffffff !important;
}
.ftr-col-t, .dir-title, .lang-grid-t {
  color: #ffffff !important;
  font-weight: 600;
}
.lang-chip {
  background: #262626 !important;
  color: #ffffff !important;
  border-radius: 9999px !important;
  border: 1px solid #333333 !important;
}
.lang-chip:hover {
  background: #333333 !important;
}
.lang-chip.on {
  background: #0066ff !important;
  border-color: #0066ff !important;
}

/* Mobbin Strict SVG Dimension Boundaries */
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
.channel-pills svg {
  width: 13px !important;
  height: 13px !important;
}

/* Calendar styling in Mobbin style */
.cal-table td {
  background: #ffffff !important;
  border-radius: 16px !important;
  border: 1px solid #f0f0f0 !important;
  box-shadow: none !important;
}
.cal-table td:hover {
  border-color: #141414 !important;
}
.cal-event-pill {
  border-radius: 9999px !important;
  font-weight: 600 !important;
}
"""

orig = orig.replace("</style>", card_mobbin_css + "\n</style>")

Path("_tpl_head_v2.html").write_text(orig, encoding="utf-8")
print("Compiled Mobbin _tpl_head_v2.html successfully! Size:", len(orig))
