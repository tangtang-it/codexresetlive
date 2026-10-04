import os

head_path = r"D:/ZySpace/zy_code/seo/codexlimit/_tpl_head.html"
with open(head_path, "r", encoding="utf-8") as f:
    css = f.read()

# Add CSS for 3D Agnes assets and functional SVG icons
extra_css = """
/* ---------- 3D Agnes Decorative Icons & Functional SVG System ---------- */
.deco-3d-badge {
  width: 48px;
  height: 48px;
  border-radius: var(--r-xl);
  object-fit: cover;
  filter: drop-shadow(0 8px 16px rgba(0,0,0,.6)) drop-shadow(0 0 12px rgba(252,213,53,.25));
  border: 1px solid rgba(252,213,53,.35);
  background: var(--canvas);
  transition: transform .3s cubic-bezier(.16,1,.3,1), filter .3s ease;
}
.gauge-card:hover .deco-3d-badge {
  transform: rotate(6deg) scale(1.06);
  filter: drop-shadow(0 10px 20px rgba(0,0,0,.7)) drop-shadow(0 0 18px rgba(252,213,53,.45));
}
.section-deco-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}
.deco-satellite {
  width: 56px;
  height: 56px;
  border-radius: var(--r-xl);
  object-fit: cover;
  border: 1px solid rgba(252,213,53,.28);
  background: var(--card);
  filter: drop-shadow(0 6px 16px rgba(0,0,0,.5)) drop-shadow(0 0 10px rgba(252,213,53,.18));
}
.icon-svg {
  display: inline-block;
  vertical-align: -0.15em;
  stroke-width: 2.2;
}
.btn .icon-svg {
  margin-right: 2px;
}
"""

if "/* ---------- 3D Agnes Decorative Icons" not in css:
    css = css.replace("</style>", extra_css + "\n</style>")
    with open(head_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("Added 3D Agnes & Functional Icon CSS successfully!")
else:
    print("CSS already present.")
