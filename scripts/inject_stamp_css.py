from pathlib import Path

path = Path("_tpl_head_v2.html")
content = path.read_text(encoding="utf-8")

# 注入大印章与全新 Direct Answer Banner 样式
new_stamp_css = """
/* ---------- OpenTheRank-Inspired High-Impact Stamp Banner ---------- */
.direct-ans-banner {
  border-radius: 20px !important;
  background: radial-gradient(circle at 86% 50%, rgba(14, 203, 129, 0.16) 0%, rgba(20, 24, 30, 0.98) 60%), #12151b !important;
  border: 1px solid rgba(14, 203, 129, 0.28) !important;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
  padding: 24px 32px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 24px !important;
  margin-bottom: 24px !important;
  overflow: hidden !important;
  position: relative !important;
}

.dab-left {
  flex: 1 1 0% !important;
  min-width: 280px !important;
}

.dab-h {
  font-size: 26px !important;
  font-weight: 700 !important;
  color: #ffffff !important;
  letter-spacing: -0.02em !important;
  margin: 6px 0 8px !important;
  line-height: 1.25 !important;
}
.dab-h strong {
  color: #0ecb81 !important;
}

.dab-p {
  font-size: 14px !important;
  color: #a0a6b2 !important;
  line-height: 1.55 !important;
  margin-bottom: 12px !important;
}
.dab-p strong {
  color: #ffffff !important;
}

.dab-rec-line {
  font-size: 12.5px !important;
  color: #707a8a !important;
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  flex-wrap: wrap !important;
  margin-bottom: 6px !important;
}
.dab-rec-dt {
  color: #eaecef !important;
  font-weight: 600 !important;
}

.dab-right-wrap {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  gap: 12px !important;
  flex-shrink: 0 !important;
}

/* Eye-Catching SVG Circular Stamp */
.openthe-stamp-wrap {
  width: 170px !important;
  height: 170px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  transform: rotate(-4deg);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: default;
}
.openthe-stamp-wrap:hover {
  transform: rotate(0deg) scale(1.05);
}

.stamp-svg {
  width: 100% !important;
  height: 100% !important;
  overflow: visible !important;
}

/* Subtle Slow Rotation of Outer Orbit Track */
.stamp-spin-orbit {
  animation: stamp-orbit-spin 36s linear infinite;
  transform-origin: 110px 110px;
}
@keyframes stamp-orbit-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .stamp-spin-orbit {
    animation: none;
  }
}

.dab-btn {
  background: #1e2329 !important;
  border: 1px solid #2b3139 !important;
  color: #eaecef !important;
  padding: 6px 14px !important;
  border-radius: 9999px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  transition: all 0.15s ease !important;
  text-decoration: none !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
}
.dab-btn:hover {
  background: #2b3139 !important;
  border-color: #FCD535 !important;
  color: #FCD535 !important;
}

@media (max-width: 768px) {
  .direct-ans-banner {
    flex-direction: column !important;
    align-items: flex-start !important;
    padding: 20px 20px !important;
  }
  .dab-right-wrap {
    width: 100% !important;
    flex-direction: row !important;
    justify-content: space-between !important;
    margin-top: 14px !important;
  }
  .openthe-stamp-wrap {
    width: 120px !important;
    height: 120px !important;
  }
}
"""

content = content.replace("</style>", new_stamp_css + "\n</style>")
path.write_text(content, encoding="utf-8")
print("Injected High-Impact Stamp Banner CSS into _tpl_head_v2.html")
