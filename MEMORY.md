# MEMORY.md - Project State & Architecture Log

## 1. Current Phase: Signal Studio Height Optimization & Compaction (Completed 2026-10-08)
- **Problem Solved**:
  - Addressed user feedback regarding `#studio` (01 — Signal Studio) being excessively tall (1200px+ vertical sprawl caused by unconstrained stream list expansion).
  - Unified all three columns into a crisp **520px fixed-height layout**:
    - Column 1 (Why The Number Moved): 520px container with internal smooth-scroll list.
    - Column 2 (Tibo Sottiaux Stream): 520px container with internal smooth-scroll tweets.
    - Column 3 (Signal Switchboard): tight 5px gap rows perfectly matching the 520px baseline without trailing voids.
  - Reduced section vertical footprint by over **55%**, dramatically improving reading rhythm and viewport density.
  - Recompiled all 40 multilingual pages; verified pixel-perfect top and bottom alignment.
- **Artifacts Delivered**:
  - `_tpl_head_v2.html`: Injected compact 520px studio layout and internal scrollbar rules.
  - Visual QA render: `compact_studio_crop.png`.

## 2. Architecture Decisions (ADRs)
- **ADR-009 [2026-10-08]**: Standardized `#studio` card height to a balanced 520px viewport budget, coupling internal scrollbars for unbounded data streams with dense status widgets for a true financial-terminal feel.

## 2. Relative Time Rounding Alignment (2026-10-08)
- Fixed updateAgo JS to Math.round(diffMin / 60) matching OpenTheRank and Python build.
- Added data-ago-utc to English dab-h header for synchronized live updating.
- Rebuilt all 40 pages.

## 3. Dynamic Days-Since Calculation & Cooldown Live Sync (2026-10-08)
- Replaced static 0.7d hardcoded numbers with live data-days-since-utc and data-cooldown-utc bindings in _tpl_body_v2.html.
- Aligned Python build to calculate days_since from latest verified reset (now accurately 0.8d) instead of stale JSON cache.
- Added client-side minute timer updating to fixed(1) + d.
- Rebuilt and verified all 40 pages.

## 4. Full-Site Real-Time Dynamic Data Audit & Upgrades (2026-10-08)
- Audited all static time-dependent fields across site.
- Upgraded SF work window in Signal Switchboard to calculate live US Pacific working hours/night/weekend with dynamic dot status.
- Added data-local-date-only binding to Gauge foot and Readout cards for seamless user-local calendar date mapping.
- Dynamicized direct answer banner no-reset fallback branches with data-days-since-utc and data-local-date-only.
- Recompiled and verified all 40 multilingual pages.
