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

## 3. Dynamic Cadence Engine, Time Sync & Tibo Feed Update (Completed 2026-10-09)
- **Problem Solved**:
  - Probability stuck at 11%: Root-caused to flat step function in compute_stats.py (days_since <= 2.0 -> cooldown_factor = -4) and absence of client-side continuous hazard calculation. Implemented continuous logistic hazard curve calcProbability(daysSince) across both Python backend and client-side JavaScript (_tpl_body_v2.html). Live probability smoothly evolves over time (11% -> 25% at 1.2d -> 48% at 2d -> 74% at 3d).
  - Time desync ("0.8d" vs "1 天前" & "Oct 8 (Now)"): Replaced static 0.8d strings with live JavaScript synchronizers for [data-days-since-utc] and [data-cooldown-utc]. Synchronized relative time to 1.2d / 1.2d 前 without conflicting formats. Chart SVG date anchors now dynamically reflect current date (Oct 9 (Now), Oct 10, Oct 11).
  - Direct answer banner: Corrected Oct 9 status from outdated "今日已重置 (Yes.)" to accurate "今日暂无放水迹象 (25% 概率) / 最近一次官方放水发生在 1.2d 前 (2026-10-08)" with golden live radar stamp.
  - Tibo stream & monitoring update: Ingested Day 4 announcement (Instant Steering & GPT-6.1 Sol ultrafast) and ChatGPT launch tweet. Total verified posts updated from 58 to 60. Added Day 4 entry to Signal Studio Moves across all languages.
- **Verification & QA**:
  - Subagent automated audit (scripts/subagent_qa_inspector.py): 18/18 test assertions passed.
  - Multilingual build audit (scripts/verify_site.py): 40/40 pages passed integrity, schema, and section audits.
  - Headless browser visual QA: Captured clean renders for banner, radar, stats, and studio.
