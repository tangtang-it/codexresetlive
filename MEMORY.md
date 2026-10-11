# MEMORY.md - Project State & Architecture Log

## 10. Phase: Day 6 Global Reset Pipeline Sync & Cooldown State Transition (2026-10-11)
- **Problem Solved & Root Causes Fixed**:
  - Investigated user report comparing competitor WillCodexReset.com against CodexReset.live.
  - Repaired 4 root cause blockers across data pipeline and render engine:
    1. Classifier Rule Collision (scripts/classifier.py): Promoted Day 6/ Reset to confirmed_reset.
    2. Scraper Type Assignment (scripts/scrape_tibo.py): Ensured reset posts are classified as regular.
    3. Hazard Engine Transition (scripts/compute_stats.py): Completed resets within 24h transition to 11% cooldown.
    4. Direct Answer Banner & Calendar Sync (scripts/build_studio.py): 24h is_today_reset window, green YES stamp.
    5. Restored Cloudflare Edge Hydration (_tpl_body_v2.html): Re-injected missing hydrateLiveSignals() calling /api/radar (functions/api/radar.js & src/worker.js). Now fetches real-time signals from edge with 30s cache, perfectly linking Cloudflare Function live data to the UI.
- **Verification & QA**:
  - Recomputed stats: 61 verified resets, latest reset 2026-10-10T22:16:20.000Z (0.7d ago), probability 11%.
  - Recompiled all 40 multilingual pages via scripts/build_studio.py.
  - Passed scripts/verify_site.py 100% across all 40 pages with zero errors.

## 9. Viral Forecast Share Modal & Share Button Integration (2026-10-11)
- **Problem Solved & Feature Delivered**:
  - In response to user request and competitor reference (WillCodexReset.com), added a sleek, unobtrusive circular viral share button (.dab-share-btn, 38x38px, SVG connected-nodes share icon) in the top-right corner of .direct-ans-banner (Direct Answer Stamp Banner).
  - Engineered a full viral sharing modal dialog (#shareModalOverlay / .share-modal) in our Binance/Linear obsidian dark design system:
    - **High-Definition Card Preview**: Displays live dynamic probability (synced with window.CODEX_RADAR.probability), verdict status, brand header, and watermark.
    - **3 Primary Action Controls**: Copy link (copies current page URL with toast notification), Copy card (HTML5 Canvas 2x Retina PNG directly into clipboard via ClipboardItem, or viral text fallback), and Download (one-click instant PNG export codex-reset-forecast.png).
    - **9 Global & Domestic Social Channels**: X (Twitter), Facebook, LinkedIn, WhatsApp, Telegram, Reddit, 微信 / WeChat (interactive QR code popup + clipboard copy guidance), 微博 / Weibo, and Email.
    - **Full 10-Locale Internationalization**: Complete native translation across n, zh-hans, zh-hant, ja, ko, s, de, r, pt-br, and 
u.
- **Verification**:
  - Recompiled all 40 multilingual and historical pages (scripts/build_studio.py).
  - Verified 100% pass on schema, placeholder, link, and section integrity (scripts/verify_site.py).
  - Visual QA verified on headless browser screenshots (qa_share_crop_banner.png, qa_share_modal_crop.png, qa_share_modal_zh_crop.png).

## 4. Phase: Circular Gauge Caption Typography & Layout Optimization (2026-10-11)
- Problem Solved:
  - Repositioned gauge caption (`.gauge-cap`, e.g. "Elevated — Approaching average reset gap") from inside the narrow circle chord to sit cleanly below `.gauge-wrap`, completely eliminating visual overlap and occlusion from the circular arc and stroke glow.
  - Upgraded caption into a high-visibility telemetry pill badge (`#f0f6fc` on frosted-glass badge with glowing status dot `::before`, dynamic color states: `.high` gold `#FCD535`, `.mod` blue `#60a5fa`, `.low` green `#0ecb81`).
  - Removed accidental square card border (`border: 1px solid #23272e !important`) from `.gauge-wrap` so the circular gauge renders borderless and clean against the card.
  - Extended dynamic client-side translations across all 10 site locales (zh-hans, zh-hant, ja, ko, es, de, fr, pt-br, ru, en).
- Verification: All 40 multilingual pages compiled via `scripts/build_studio.py` and passed `scripts/verify_site.py` 100%.

## 3. Phase: Global Variable Unification, Single Native Pulse Wave & Mobile Optimization (2026-10-11)
- Problem Solved:
  - Global probability divergence fixed: Resolved inconsistency where Direct Answer Banner & Stamp displayed 99% while the circular gauge displayed 79% (due to unaligned client formula clamp). Unified probability authoritative state via window.CODEX_RADAR.probability.
  - Chart duplicate line eliminated: Completely purged redundant ECharts injection and duplicate X-axis labels, restoring the single, clean, custom native SVG pulse wave with historical badges and 48-hour projection.
  - Mobile responsiveness perfected: Added fluid aspect-ratio scaling for chart SVG, wrapped legend badges and alert email inputs, and fine-tuned card paddings for viewports under 640px and 420px.
- Verification: All 40 multilingual pages recompiled and passed verify_site.py 100%.

## 2. Phase: Intelligent Tweet Classifier & Reset Banner Guard (2026-10-11)
- Problem Solved: Fixed False Positive where Direct Answer Banner reported reset completed due to substring match on humorous community reply.
- Architecture Delivered: Implemented scripts/classifier.py (Open-Source LLM + Heuristics + Cache).
- Aligned direct answer banner with verified confirmed reset events.
- Rebuilt all 40 pages and verified 100% integrity.

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

## 4. X (Twitter) Link Integrity & Mock Data Immunity (Completed 2026-10-09)
- **Problem Solved**:
  - Investigated user-reported 404 dead link on /reset-today/ pointing to https://x.com/thsottiaux/status/2108548123456789013.
  - Root-caused to manual mock records with placeholder IDs (123456789012, 123456789013) ingested in prior development turns that persisted through cache merges.
- **Implemented Fixes & Immunity Shields**:
  - **Data Cleansing**: Completely purged fake records from data/tibo_reset_history.json and aligned with legitimate remote upstream records (56 verified records).
  - **Scraper Ingestion Guard** (scripts/scrape_tibo.py): Added is_valid_tweet_id validator that rejects non-Snowflake IDs and mock patterns (e.g. 123456789, repeated sequences) both at parsing and cache merge stages.
  - **CI & Build Pipeline Guard** (scripts/verify_site.py): Added mandatory integrity assertion scanning all generated HTML files for external X status links; any mock/invalid ID immediately aborts build with exit code 1.
  - **Full Regeneration & QA**: Recomputed radar statistics, regenerated all 40 multilingual pages, and verified 100% test pass on both verify_site.py and subagent_qa_inspector.py.

## 5. Dual-Engine Realtime Ingestion & Day 4 Sync (Completed 2026-10-09)
- **Problem Solved**:
  - Addressed discrepancy where competitor (willcodexquotareset.com) displayed the Day 4 tweet (2026-10-08 19:15 UTC) and ChatGPT announcement while codexresetlive.com was missing it due to upstream delay in opentherank.com.
- **Implemented Upgrades**:
  - **Dual-Source Ingestion Engine** (scripts/scrape_tibo.py): Upgraded scraper with Source 1 (competitor fast stream willcodexquotareset.com/api/forecast) + Source 2 (OpenTheRank backlog archive) + validated real Snowflake ID fallback.
  - **Verified Real Links Synchronized**:
    - Day 4 Release: https://x.com/thsottiaux/status/2108275041276420573
    - ChatGPT Announcement: https://x.com/thsottiaux/status/2108349826727588000
    - Day 3 Encore: https://x.com/thsottiaux/status/2108084615349170480
  - Recompiled all 40 multilingual pages; passed 100% QA and link validity audit.


## 6. SEO Audit Clean-up & Production Hardening (Completed 2026-10-09)
- **External Redirects & Broken Links Fixed**:
  - Replaced Windsurf redirect chain (`https://codeium.com/windsurf?ref=codexreset` -> `https://codeium.com/windsurf`).
  - Replaced Claude 403 route (`https://claude.ai/code?ref=codexreset` -> `https://claude.ai/`).
  - Verified zero placeholder / mock tweet links across all compiled HTML pages.
- **llms.txt Markdown Links**:
  - Enriched `site/llms.txt` with standard markdown hyperlinks to Radar, Calculator, FAQ, and GitHub signal repository.
- **AI Crawler Allowances in robots.txt**:
  - Explicitly allowed OAI-SearchBot, ChatGPT-User, GPTBot, PerplexityBot, Claude-Web, ClaudeBot, and Applebot-Extended.
- **Edge Security Headers Configured**:
  - Created `site/_headers` and `_headers` for Cloudflare Pages (HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy).
- **H1 Keyword Consistency**:
  - Added spacing around line breaks in `<h1>__H1_A__ <br><em>__H1_B__</em></h1>` so stripped-text parsers extract "Will Codex Reset Today?" cleanly.
- **Verification**:
  - Recompiled all 40 multilingual pages (`scripts/build_studio.py`).
  - 100% passed `scripts/verify_site.py` integrity, schema, and link audit.


## 7. Tibo Feed Stagnation Root-Cause Analysis & Day 5 Real-Time Pipeline (Completed 2026-10-10)
- **Problem Diagnosed**: Tibo signal feed repeatedly appeared stale across versions, failing to show Day 5 tweets (Composer predictions & mobile Dots).
- **4 Fatal Root Causes Discovered**:
  1. **Upstream Proxy Failure**: `scripts/scrape_tibo.py` was never a direct X scraper; it was scraping competitor `willcodexquotareset.com/api/forecast`. The competitor API threw `sourceErrors: {'tibo': 'Tibo timeline returned 404'}` and returned empty `tiboPosts: []`.
  2. **CI/CD Silent No-op**: GitHub Actions `update_radar.yml` used `python scripts/scrape_tibo.py || true`. When scraper ingested 0 tweets, no diff was produced, and `git-auto-commit-action` silently skipped pushing.
  3. **Static Generation Lag**: The site is a 100% pre-rendered SSG (40 multilingual pages) without runtime browser live-polling. Without a successful GitHub Actions commit + Cloudflare Pages deployment, client HTML remained permanently frozen.
  4. **Data Layer Desync**: Column 1 (`MOVES_DATA` in `build_studio.py`) was hardcoded Python tuples, meaning even if Column 2 got new tweets, Column 1 would stay frozen on Day 4.
- **Implemented Fixes & Tooling**:
  - **Ingested Verified Day 5 Signals**:
    - Tweet 1: `2108842183749873664` (Composer predictions in desktop app without consuming usage, Pro plans).
    - Tweet 2: `2108845192084729856` (Day 5 dots edition: create and text dot from ChatGPT mobile app).
  - **Data Synchronization**: Updated `data/tibo_reset_history.json` (61 verified records), recomputed stats (days_since=1.8d, prob=41%).
  - **Signal Studio Updates**: Updated `MOVES_DATA` in `scripts/build_studio.py` across English, Chinese, and Japanese with Day 5 Catalyst (+30 pts).
  - **Single-Command Developer Pipeline (`scripts/add_signal.py`)**: Added CLI to instantly ingest any tweet/signal, validate snowflake ID, recompute stats, compile all 40 pages, and run audit in one command.
- **Verification**: 40/40 multilingual pages recompiled; 100% passed `verify_site.py` integrity, schema, and section audit.

## 8. Cloudflare Edge Function & Client Hydration Architecture Upgrade (Completed 2026-10-11)
- **Problem Root-Caused**: User noticed significant data latency compared to competitor (willcodexreset.com showing Day 6 / 99% probability while site remained stuck). Inspection of Cloudflare dashboard revealed Cloudflare Pages was skipping deployments entirely ('已跳过 0s') due to '[skip ci]' tags in Git commit messages.
- **Architecture Upgrade (Static SSG -> SWR Edge Hybrid)**:
  1. **Cloudflare Pages Function (/api/radar)**: Created functions/api/radar.js to directly query upstream real-time radar payload with 30s Edge caching and CORS support.
  2. **Client-Side SWR Hydration**: Injected hydrateLiveSignals() into _tpl_body_v2.html. Pages load instantly with pre-rendered SEO HTML and asynchronously fetch /api/radar to dynamically update probability stamps (e.g. 51% -> 99%) and prepend latest tweets without page refresh.
  3. **CI/CD Build Unblocking**: Removed '[skip ci]' from .github/workflows/update_radar.yml so Cloudflare Pages automatically detects changes and triggers deployments.
- **Verification**: 40/40 multilingual pages recompiled; 100% passed verify_site.py integrity and schema audit.

## 5. Monetag Monetization Integration (2026-10-11)
- **Format 1 - In-Page Push (Banner)**:
  - Injected Monetag zone `12002461` (`https://nap5k.com/tag.min.js`) into `_tpl_head_v2.html` after `<head>` / `<meta charset="UTF-8">`.
  - Recompiled all 40 multilingual and historical pages via `scripts/build_studio.py`.
  - Audited via `scripts/verify_site.py` (100% pass across all 40 pages).
- **Format 2 - Direct Link (Completed 2026-10-11)**:
  - Integrated Monetag Direct Link (`https://uplcm.com/4/12002462`) into `_tpl_body_v2.html` and `scripts/build_studio.py`.
  - Native Placement 1: Multilingual responsive `.sponsor-banner` positioned between `#calculator` and `#guides` with `rel="noopener nofollow sponsored"`.
  - Native Placement 2: Global `foot-links` partner anchor (`Partner Deals ↗`).
  - Recompiled all 40 multilingual and historical pages; verified 100% pass via `scripts/verify_site.py`.
