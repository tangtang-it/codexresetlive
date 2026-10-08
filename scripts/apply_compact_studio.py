from pathlib import Path

path = Path("_tpl_head_v2.html")
content = path.read_text(encoding="utf-8")

compact_studio_css = """
/* ---------- Studio 3-Column Compact Height & Pixel Alignment ---------- */
.studio-grid {
  display: grid !important;
  grid-template-columns: 1fr 1.35fr 1fr !important;
  gap: 18px !important;
  margin-bottom: 36px !important;
  align-items: stretch !important;
}
.studio-col {
  height: 520px !important;
  max-height: 520px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
  padding: 18px !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}
.studio-col > .col-header {
  flex-shrink: 0 !important;
  padding-bottom: 10px !important;
}
.studio-col > .move-list,
.studio-col > .stream-box {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  max-height: none !important;
  overflow-y: auto !important;
  padding-right: 4px !important;
}
.switch-user-card {
  padding: 10px 12px !important;
  gap: 2px !important;
  flex-shrink: 0 !important;
}
.switch-user-card .suc-num {
  font-size: 22px !important;
  line-height: 1.1 !important;
}
.switch-items {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 5px !important;
}
.switch-row {
  padding: 5px 10px !important;
  font-size: 11.5px !important;
}
@media(max-width:1020px){
  .studio-grid {
    grid-template-columns: 1fr !important;
  }
  .studio-col {
    height: auto !important;
    max-height: none !important;
  }
  .studio-col > .move-list,
  .studio-col > .stream-box {
    max-height: 420px !important;
  }
}
"""

content = content.replace("</style>", compact_studio_css + "\n</style>")
path.write_text(content, encoding="utf-8")
print("Successfully injected compact studio CSS into _tpl_head_v2.html")
