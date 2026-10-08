from pathlib import Path

path = Path("_tpl_head_v2.html")
content = path.read_text(encoding="utf-8")

# 1. 引入 Inter 和 JetBrains Mono 字体
fonts_tag = """<!-- High-Craft Typography: Inter & JetBrains Mono -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
"""
if "fonts.googleapis.com" not in content:
    content = content.replace("<style>", fonts_tag + "\n<style>")

# 2. 注入专业遥测微卡片 (Telemetry Badge) 与去 AI 味精密样式
promax_css = """
/* ---------- UI/UX Pro Max: De-AI & Precision Telemetry ---------- */
.dab-telemetry-badge {
  background: #14171d;
  border: 1px solid #282f38;
  border-radius: 12px;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
  min-width: 170px;
}
.dab-telemetry-badge.standby {
  border-color: #383120;
}
.dt-top {
  display: flex;
  align-items: center;
  gap: 6px;
}
.dt-label {
  font-size: 10px;
  font-weight: 700;
  color: #707a8a;
  letter-spacing: 0.06em;
  font-family: var(--mono);
  text-transform: uppercase;
}
.dt-source {
  font-size: 11.5px;
  color: #eaecef;
}
.dt-source strong {
  color: #FCD535;
}
.dt-time {
  font-size: 11px;
  color: #707a8a;
  font-family: var(--mono);
}
.dt-prob-pill {
  margin-top: 4px;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 10.5px;
  font-weight: 700;
  font-family: var(--mono);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  width: fit-content;
}
.dt-prob-pill.yes {
  background: rgba(14, 203, 129, 0.14);
  color: #0ecb81;
  border: 1px solid rgba(14, 203, 129, 0.3);
}
.dt-prob-pill.yellow {
  background: rgba(252, 213, 53, 0.14);
  color: #FCD535;
  border: 1px solid rgba(252, 213, 53, 0.3);
}

.dot-live {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #0ecb81;
  box-shadow: 0 0 8px #0ecb81;
  animation: dt-pulse 2s infinite ease-in-out;
}
.dot-amber {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #FCD535;
  box-shadow: 0 0 8px #FCD535;
  animation: dt-pulse 2s infinite ease-in-out;
}
@keyframes dt-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.25); opacity: 0.6; }
}

/* De-AI Precision Font Stacks */
body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  letter-spacing: -0.01em;
}
.num, [data-ago-utc], [data-local-dt], .dt-time, .ro-v, .gauge-num, .dial-num {
  font-family: "JetBrains Mono", ui-monospace, "SF Mono", monospace !important;
  font-variant-numeric: tabular-nums;
}
h1, h2, h3, .h1, .h2, .h3 {
  letter-spacing: -0.025em !important;
}

/* Card Clean Hairlines (No cheap heavy glow) */
.card-box, .gauge-wrap, .chart-svg-wrap, .studio-col, .calc, .cal-grid-card, .direct-ans-banner {
  border: 1px solid #23272e !important;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
  transition: border-color 0.2s ease;
}
.card-box:hover, .studio-col:hover, .calc:hover {
  border-color: #353c48 !important;
}

/* Strict Sizing Guardrails */
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
.brand-mark svg {
  width: 20px !important;
  height: 20px !important;
}
"""

content = content.replace("</style>", promax_css + "\n</style>")
path.write_text(content, encoding="utf-8")
print("Updated _tpl_head_v2.html with UI/UX Pro Max rules successfully!")
