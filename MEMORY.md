# MEMORY.md - Project State & Architecture Log

## 11. Phase: Oct 23 Day 18 Reset Event Sync & AdSense Pre-Audit Remediation (2026-10-23)
- Problem Solved & Root Causes Fixed:
  1. Classifier Rule Flaw (scripts/classifier.py): Day 18 tweet 2113492187770175603 was misclassified as chatter due to missing pattern for that's a reset. Added pattern and verified reset record.
  2. Cloudflare Edge Ingestion Gap (functions/api/radar.js & src/worker.js): Upstream data.events array was dropped. Now parses verified resets, extracts latestReset/lastResetAt, and removed fake fallback numbers.
  3. Stats Recalibration (scripts/compute_stats.py): Added follow-up tweet 2113492502355562875. Stats: 41 resets (11 in Oct), last reset 2026-10-23T04:46:19Z (0.3d ago), probability 99%.
  4. AdSense Compliance Pages (scripts/build_compliance_pages.py): Built dedicated /about/, /privacy/, /terms/, /contact/ pages with Google AdSense/DoubleClick cookie disclosures, edge logging facts, CCPA/GDPR clauses, and real contact channels.
  5. Harmonized Content & Removed Mock Email: Replaced fake email toast with real official source links and bookmark action. Harmonized FAQ text with active radar state.
  6. Sitemap & Verification: Updated sitemap.xml to 44 URLs and verified 100% pass via scripts/verify_site.py.

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

## 9. 48-Hour Forecast Pulse SVG Chart Oct 11 Desync Fix (Completed 2026-10-12)
- **Problem Root-Caused**:
  1. Direct answer stamp & cards correctly stated 'Latest reset 2026-10-11' (Day 6 hard reset confirmed on 2026-10-11 04:01 UTC).
  2. However, the SVG line chart ('48-Hour Forecast Pulse') retained static 10-09 layout: hardcoded 'Oct 8' event marker at x=425, missing Oct 11 event marker, and plotted a 4-day continuous drop directly from Oct 8 to Oct 12 Now (1%), contradicting the 11th reset.
  3. Client-side SWR hydration updated 'Now' anchor point coordinates to y=128.8 (1%) but did not update the SVG curve path endpoints, leaving a visual line disconnect.
- **Implemented Fixes**:
  1. **Dynamic SVG Generation (scripts/build_studio.py)**:
     - Dynamically formatted last_lbl (e.g. Oct 11) and time string from last_dt.
     - Updated Event Marker 4 at x=425 to last_lbl Confirmed Hard Reset (04:01 UTC) with Reset badge.
     - Updated X-axis date marker at x=425 to last_lbl (Oct 11).
     - Corrected Bezier curve trajectory (chartHistPath): from Oct 7 double event (330, 36), through Oct 8-10 lull (y=85), rising to Oct 11 hard reset peak (425, 40), then smoothly dropping down to Oct 12 Now cooldown level (515, y_now).
     - Added Day 6 reset to MOVES_DATA across English, Chinese, and Japanese.
  2. **Client-Side Live Hydration Coupling (_tpl_body_v2.html)**:
     - Bound chartHistPath and chartProjPath endpoints dynamically to yNow in updateLiveEngine(), eliminating line-to-dot disconnect.
     - Bound chartLastResetDate to lastReset date dynamically.
  3. **Hazard Cooldown Tuning (scripts/compute_stats.py)**:
     - Set initial post-reset cooldown (d <= 1.5d) to 1% baseline to match upstream radar signal.
- **Verification**: 40/40 multilingual pages recompiled; 100% passed verify_site.py integrity, schema, and section audit.

## 10. 48-Hour Forecast Pulse High Probability Clipping & Anchor Alignment Fix (2026-10-22)
- **Problem Root-Caused**:
  1. **Top Clipping Bug on High Probability**: When probability reached >= 80% (e.g. 99% in live window), the legacy linear formula `yNow = 130 - prob * 1.25` computed `yNow = 6.25`. Placing the badge at `yNow - 23` pushed `yBadgeRect = -16.75` and text to `y = -5.75` (negative coordinates). The SVG `viewBox="0 0 740 185"` and `.chart-svg-wrap { overflow: hidden; }` truncated the badge horizontally, leaving only a 0.2px sliver at the top boundary.
  2. **Anchor Coordinate & Path Desync**: In `_tpl_body_v2.html`, client-side SWR hydration previously hardcoded `cx="515"` and an obsolete 3-spike Bezier curve from October 11, whereas the compiled SVG in `build_studio.py` placed the 'Now' date and anchor at `x="525"` with 4 verified historical reset spikes (Oct 13, 15, 17, 20).
- **Implemented Fixes**:
  1. **Bounded Coordinate Mapping**:
     - Below 80%: Maps linearly from baseline `y = 130.0` (0%) to `y = 35.0` (80% grid line).
     - Above 80%: Smoothly compresses into the event crest zone from `y = 35.0` to `y = 30.0` (100%), matching confirmed reset levels (`y = 32`).
     - Hard Floor: Enforced `yBadgeRect = max(11.0, round(yNow - 20.0, 1))` and `yBadgeText = yBadgeRect + 11.5` in both Python (`scripts/build_studio.py`) and JS (`_tpl_body_v2.html`), ensuring the badge perfectly aligns on the horizontal row of RESET badges (`y = 11.0`, `y = 22.5`) with 11px headroom.
  2. **Synchronized SWR Hydration**:
     - Aligned all client-side anchor elements (`chartDot`, `chartRing`, `chartStem`, `chartProbTxt`) to `x = 525`, `chartBadgeRect` to `x = 498` (width 54, centered at 525).
     - Updated `chartHistPath`, `chartProjPath`, and added `chartAreaPath` dynamic endpoint coupling.
- **Verification**:
  - Recompiled all 40 multilingual and historical pages via `scripts/build_studio.py`.
  - 100% passed `scripts/verify_site.py` integrity, schema, and section audit.
  - Headless Chrome QA verified clean rendering and zero clipping under 99% probability.
- **Chart Reset vs Next Forecast UI**: When a reset occurred within 24h, the chart renders the current date as a green RESET event and places the next probability on the following date as yellow NEXT N%. The direct-answer timestamp renders both Tibo UTC and the visitor local timezone.

- **降低首页视觉模板感**: Commit 955b75d. Removed heavy gradients/shadows, reduced uniform rounded-card treatment, normalized label casing, reduced stamp emphasis, and clarified reset-versus-next-forecast hierarchy. Baseline rollback commit: f07cd1f.


- **编辑部观测站视觉方向 A**: Commit b45ad32. Switched the generated site to warm paper, charcoal, editorial red, serif display headings, restrained borders, and source/archive-oriented hierarchy while preserving all functions and URLs. Rollback tag: ui-before-editorial-a.


- **观测站圆顶品牌图标**: Commit e54d2c7. Replaced favicon and generated page brand marks with a unified observatory dome plus reset arc SVG. Preserved all runtime behavior and routes; QA screenshot: qa_observatory_icon.png.


- **月度日历图标与档案布局**: Commit 6ba03f5. Calendar now uses consistent linear reset/banked icons, editorial serif month title, clearer legend, paper-grid cells, and less pill-like event labels. Runtime calendar data and navigation remain unchanged.


- **信号统计卡与赞助横幅对比度**: Commit 3aaf753. Converted the remaining dark switchboard user-estimate card and sponsor banner to readable editorial paper surfaces with a primary-color edge marker; data and layout behavior unchanged.


- **顶部状态印章仪表盘与预测图表层级**: Commit c1b4758. Reduced the confirmed-reset stamp, simplified the 99% gauge, and normalized chart marker fills to editorial paper/green/red/amber colors so current reset and next forecast read as separate states.


- **公开信号证据卡**: Commit c83e78d. Added a source-first Latest Public Signal card showing the original post, thread context, interpretation, expected window, status, and source link; it distinguishes scheduled signals from confirmed effects without changing the event data model.


- **Tibo 头像与原文链接**: Commit b124a9a. Added the source author's avatar, handle, and direct original-post link to the confirmed reset summary in the hero area, with localized link labels and accessible image dimensions.


- **重置判定内联嵌入 Tibo 头像与链接**: Commit e4377dc. Fixed low-contrast white-on-cream text in direct answer banner by assigning var(--on-dark) to strong elements, and seamlessly embedded Tibo's avatar with direct link to the original X post into the primary verdict paragraph.

