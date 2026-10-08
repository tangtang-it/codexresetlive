from pathlib import Path

path = Path("_tpl_head_v2.html")
content = path.read_text(encoding="utf-8")

# 1. 替换 studio-grid 与 studio-col 的高度与弹性拉伸规则
old_grid_def = ".studio-grid{display:grid;grid-template-columns:1fr 1.35fr 1fr;gap:18px;margin-bottom:48px}"
new_grid_def = ".studio-grid{display:grid;grid-template-columns:1fr 1.35fr 1fr;gap:18px;margin-bottom:48px;align-items:stretch}"

if old_grid_def in content:
    content = content.replace(old_grid_def, new_grid_def)
    print("Updated studio-grid align-items: stretch")
else:
    print("WARN: old_grid_def not found")

old_col_def = ".studio-col{background:var(--card);border:1px solid var(--hairline);border-radius:var(--r-xl);padding:20px;\ndisplay:flex;flex-direction:column;gap:16px}"
new_col_def = ".studio-col{background:var(--card);border:1px solid var(--hairline);border-radius:var(--r-xl);padding:20px;\ndisplay:flex;flex-direction:column;gap:16px;height:100%;box-sizing:border-box}"

if old_col_def in content:
    content = content.replace(old_col_def, new_col_def)
    print("Updated studio-col height: 100%")
else:
    print("WARN: old_col_def not found")

# 2. 移除写死的 max-height:460px，使用 flex: 1 1 0% 自动撑满高度，让前两列与最右侧在像素级严格等高
old_move = ".move-list{display:flex;flex-direction:column;gap:11px;max-height:460px;overflow-y:auto;padding-right:4px}"
new_move = ".move-list{display:flex;flex-direction:column;gap:11px;flex:1 1 0%;min-height:0;overflow-y:auto;padding-right:4px}"

if old_move in content:
    content = content.replace(old_move, new_move)
    print("Updated move-list to flex: 1 1 0%")
else:
    print("WARN: old_move not found")

old_stream = ".stream-box{display:flex;flex-direction:column;gap:12px;max-height:460px;overflow-y:auto;padding-right:4px}"
new_stream = ".stream-box{display:flex;flex-direction:column;gap:12px;flex:1 1 0%;min-height:0;overflow-y:auto;padding-right:4px}"

if old_stream in content:
    content = content.replace(old_stream, new_stream)
    print("Updated stream-box to flex: 1 1 0%")
else:
    print("WARN: old_stream not found")

# 另外，追加一条兜底 CSS，确保无论外部权重如何，3列 studio-col 及其内部滚动区域均绝对等高对齐
safety_studio_css = """
/* Studio 3-Column Strict Bottom Alignment Guarantee */
.studio-grid {
  display: grid !important;
  grid-template-columns: 1fr 1.35fr 1fr !important;
  align-items: stretch !important;
}
.studio-col {
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  box-sizing: border-box !important;
}
.studio-col > .col-header {
  flex-shrink: 0 !important;
}
.studio-col > .move-list,
.studio-col > .stream-box {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  max-height: none !important;
  overflow-y: auto !important;
}
@media(max-width:1020px){
  .studio-grid {
    grid-template-columns: 1fr !important;
  }
  .studio-col > .move-list,
  .studio-col > .stream-box {
    max-height: 480px !important;
  }
}
"""

content = content.replace("</style>", safety_studio_css + "\n</style>")
path.write_text(content, encoding="utf-8")
print("Saved _tpl_head_v2.html with strict equal-height alignment rules!")
