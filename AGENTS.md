# AGENTS.md - CodexReset.live Engineering Guidelines

## 1. Project Overview & Scope
- **Domain**: [https://codexresetlive.com/](https://codexresetlive.com/)
- **Mission**: Source-first radar for public OpenAI Codex quota resets, verified developer signals (@thsottiaux), and personal 5-hour rolling limit recovery calculators.
- **Active Section Hierarchy**:
  1. `hero`: High-Impact Direct Answer Stamp Banner + Dual-Engine Radar
  2. `01 — Signal Studio` (`#studio`): Compact 520px unified equal-height 3-column studio grid
  3. `02 — Authority & Proximity` (`#monitors`): Verified leadership monitoring grid
  4. `03 — Calendar Radar` (`#calendar-grid`): Monthly visual reset archives
  5. `04 — Personal Engine` (`#calculator`): 5-hour rolling recovery calculator
  6. `05 — Deep Dive` (`#guides`): Technical deep-dive guides
  7. `06 — Alternatives` (`#tools`): Developer alternative tools
  8. `07 — Knowledge Base` (`#faq`): Algorithmic FAQ

## 2. Studio 3-Column Height & Density Guidelines
- **Unified Card Height**: `.studio-col` is locked to `height: 520px !important; max-height: 520px !important;` to prevent vertical bloat.
- **Inner Scroll Containers**: `.move-list` and `.stream-box` use `flex: 1 1 0% !important; min-height: 0; overflow-y: auto;` for smooth intra-card scrolling.
- **Switchboard Density**: Compact padding (`5px 10px`) on `.switch-row` ensures all 8 signals comfortably populate Column 3 without overflow or bottom voids.

## 3. Build & Verify Commands
```bash
# 1. Compile all 40 multilingual pages
python scripts/build_studio.py

# 2. Run integrity & schema audit
python scripts/verify_site.py

# 3. Preview locally (port 8080)
python -m http.server 8080 --directory site
```
