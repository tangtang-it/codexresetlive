import re
from pathlib import Path

# 以具有完整 147+ 个 v2 类名的原始模板为基准进行黏土拟态化
orig = Path("_tpl_head_v2_orig.html").read_text(encoding="utf-8")

# 1. 替换 Typography
fonts_tag = """<!-- High-Trust Typography: Inter & JetBrains Mono -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
"""
if "fonts.googleapis.com" not in orig:
    orig = orig.replace("<style>", fonts_tag + "\n<style>")

# 2. 替换 :root 变量池为 Claymorphism 黏土拟态变量
old_root = re.search(r":root{([^}]+)}", orig)
clay_root = """:root{
/* Claymorphism Theme Tokens (https://spicytater.cn/terms/claymorphism) */
--canvas:#EEF2F6;
--surface-1:#FFFFFF;
--surface-2:#F8FAFC;
--surface-inset:#E2E8F0;

--card:#FFFFFF;
--elevated:#F8FAFC;
--hairline:rgba(255, 255, 255, 0.85);
--hairline-strong:rgba(203, 213, 225, 0.8);

/* Clay Shadows */
--clay-card-shadow: 0 16px 36px -8px rgba(100, 116, 139, 0.16), 0 4px 12px -2px rgba(100, 116, 139, 0.08), inset 0 3px 5px rgba(255, 255, 255, 0.95), inset 0 -4px 6px rgba(148, 163, 184, 0.15);
--clay-inset-shadow: inset 0 3px 6px rgba(100, 116, 139, 0.18), inset 0 -2px 4px rgba(255, 255, 255, 0.85);
--clay-btn-shadow: 0 10px 22px -4px rgba(99, 102, 241, 0.38), inset 0 3px 4px rgba(255, 255, 255, 0.45), inset 0 -3px 5px rgba(0, 0, 0, 0.18);

/* Primary Accent: Clay Lavender Indigo */
--primary:#6366F1;
--primary-active:#4F46E5;
--primary-hover:#4F46E5;
--primary-focus:#6366F1;
--primary-disabled:#CBD5E1;
--on-primary:#FFFFFF;

/* High-Contrast Charcoal Ink */
--ink:#0F172A;
--body:#334155;
--muted:#64748B;
--muted-strong:#475569;
--on-dark:#0F172A;

/* Vibrant Dopamine Semantic Status */
--up:#10B981;
--up-glow:rgba(16, 185, 129, 0.2);
--down:#EF4444;
--info:#6366F1;
--cyan:#0EA5E9;
--warning:#F59E0B;

/* Soft Clay Radii */
--r-sm:8px;--r-md:12px;--r-lg:18px;--r-xl:24px;--r-2xl:32px;--r-pill:9999px;

/* Fonts */
--font:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
--mono:"JetBrains Mono",ui-monospace,"SF Mono",Menlo,monospace;
}"""

if old_root:
    orig = orig.replace(old_root.group(0), clay_root)

# 3. 页面底色和字体全局调整
orig = orig.replace("body{background:var(--canvas);color:var(--body);font-family:var(--font);font-size:14px;line-height:1.5;", 
                    "body{background:var(--canvas);color:var(--body);font-family:var(--font);font-size:14px;line-height:1.55;letter-spacing:-0.005em;")

# 4. 顶栏导航改为柔和悬浮黏土栏
orig = orig.replace("background:rgba(11,14,17,.92)", "background:rgba(238,242,246,0.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.7);box-shadow:0 4px 24px rgba(100,116,139,0.08)")
orig = orig.replace("color:var(--muted);letter-spacing:.2px", "color:var(--muted);")

# 5. 替换卡片样式为黏土凸起浮雕 (Convex Clay Cards)
orig = orig.replace("border:1px solid var(--hairline);", "border:1px solid rgba(255,255,255,0.85);border-radius:24px;box-shadow:var(--clay-card-shadow);")
orig = orig.replace("border:1px solid var(--card);", "border:1px solid rgba(255,255,255,0.85);border-radius:24px;box-shadow:var(--clay-card-shadow);")
orig = orig.replace("background:var(--card);", "background:var(--surface-1);")

# 6. 直达答案条 (Direct Answer Banner) 变成柔和纯白微凸黏土大卡片
orig = orig.replace("background:linear-gradient(135deg,rgba(43,49,57,.65),rgba(24,26,32,.95));", "background:#ffffff;border:1px solid rgba(255,255,255,0.9);box-shadow:var(--clay-card-shadow);border-radius:26px;")
orig = orig.replace("border:1px solid rgba(252,213,53,.35);", "border:none;")

# 7. 内凹槽 (Concave Inset) 用于图表底板、输入框、进度条槽、日历单元格
orig = orig.replace("background:var(--elevated);", "background:#EEF2F6;box-shadow:var(--clay-inset-shadow);border:none;")
orig = orig.replace("background:var(--canvas);", "background:#EEF2F6;")

# 8. 胶囊黏土按钮
orig = orig.replace(".btn-primary{background:var(--primary);color:var(--on-primary);", 
                    ".btn-primary{background:linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);color:#ffffff;border-radius:var(--r-pill);box-shadow:var(--clay-btn-shadow);transition:all 0.15s ease;")

# 9. 绝对锁死所有 SVG 图标的宽度高度，绝不放大！
clay_guard_css = """
/* Claymorphism SVG Dimension Guardrails & Micro-Interactions */
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
.brand-mark {
  background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3), inset 0 2px 3px rgba(255,255,255,0.4) !important;
  border: none !important;
}
.brand-mark svg {
  width: 20px !important;
  height: 20px !important;
}
.channel-pills svg {
  width: 13px !important;
  height: 13px !important;
}

/* Clay Inset Components */
.chart-svg-wrap {
  background: #f1f5f9 !important;
  border-radius: 20px !important;
  box-shadow: inset 0 3px 6px rgba(100, 116, 139, 0.15), inset 0 -2px 4px rgba(255, 255, 255, 0.8) !important;
  padding: 14px !important;
}
.clock-c {
  background: #f1f5f9 !important;
  border-radius: 16px !important;
  box-shadow: inset 0 3px 6px rgba(100, 116, 139, 0.15), inset 0 -2px 4px rgba(255, 255, 255, 0.8) !important;
}
.cal-table td {
  background: #f8fafc !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 10px rgba(100, 116, 139, 0.06), inset 0 2px 3px rgba(255, 255, 255, 0.9) !important;
  border: 1px solid rgba(255, 255, 255, 0.8) !important;
}
.cal-table td:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(100, 116, 139, 0.12), inset 0 2px 3px rgba(255, 255, 255, 0.95) !important;
}
"""

orig = orig.replace("</style>", clay_guard_css + "\n</style>")

Path("_tpl_head_v2.html").write_text(orig, encoding="utf-8")
print("Compiled Claymorphism _tpl_head_v2.html successfully! Size:", len(orig))
