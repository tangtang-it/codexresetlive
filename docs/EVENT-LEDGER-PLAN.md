# Event Ledger Implementation Plan — 2026-10-25

## Specify
- Replace the homepage and reset-today forecast chart/gauge block with Concept C: chronological event ledger, source inspector and compact independent 48-hour indicator.
- Preserve existing routes, branding, themes, calculator, source stream and calendar. Reuse existing CSS tokens and vanilla JS/Python static build.
- Dates are normal document-flow headings, never SVG coordinates. Desktop uses approximately 2:1 ledger/inspector columns; <=760px uses expandable inline detail. Minimum touch target 44px, visible focus, keyboard-operable controls, no horizontal document overflow.

## Data contract and invariants
- One canonical client event store seeded by all local history records (stable id, UTC at, category, text, source URL, source provenance). Invalid timestamps cannot become current timestamps. No event removed just because it is not today.
- Preserve multiple events per day and distinct IDs. Merge repeated IDs deterministically; do not merge separate events merely because they share a source link. Sort by actual timestamp descending.
- Categories: reset, banked, pending/notice and other signals; classifier output is a recorded interpretation, not independent verification. Never promote a future promise or ordinary post to a completed reset just because it contains the word reset.
- Live hydration merges available event arrays/posts and latestReset into the store. Select latest reset by timestamp, not array order. Keep lastResetAt and latestReset provenance consistent. If upstream only supplies a partial history, merge it into static history instead of replacing history.
- Hero/latest-reset/date groups/calendar consume the canonical store. Local dates use one timezone policy; inspector exposes local timezone plus UTC. Fallback retains static records and visibly reports live unavailability.
- Historical probabilities are not fabricated. Forecast is a compact current heuristic value with available freshness metadata, separate from historical event facts.

## Plan and tasks
1. Add reusable event normalization/store/ledger rendering code using existing project conventions; safely serialize inline JSON and insert user/upstream text via textContent, validate outgoing http(s) links.
2. Replace chart/gauge markup and obsolete chart update code. Keep compatibility for unrelated consumers and explicitly remove unused SVG generation.
3. Add desktop list, date headings, category filters, text search, accessible selection, source inspector and mobile disclosure. Default latest reset selected; show Today empty state without asserting there are no account resets.
4. Show recent records initially and Load earlier events until every record is accessible. Show filter counts/empty states. No arbitrary hidden date cutoff.
5. Update both live endpoint implementations consistently if needed for canonical events, sorted latest reset and provenance. Do not invent sources or timestamps.
6. Share canonical reset store with calendar updates and hero summary, including after live fetch and midnight changes.
7. Localize new visible labels for all 10 existing locales, using existing i18n conventions. Do not translate original post quotations.

## Verify
- Meaningful deterministic regression fixtures: Oct 23 17:41 UTC becomes Oct 24 01:41 Shanghai; Oct 25 retains that event while today is empty; UTC and Los Angeles group correctly; same-day multiple records retained; midnight changes headings; old records remain loadable; filters/search/selection work; live new event updates hero/ledger/calendar; repeated hydration deduplicates; out-of-order upstream chooses latest correctly; malformed data and unavailable API preserve static history; source relation remains explicit.
- Run uv run python scripts/build_studio.py and uv run python scripts/verify_site.py; inspect generated routes for placeholders, script errors and old hardcoded chart remnants.
- ego-browser QA at desktop and 390px mobile, light/dark, English and Chinese; screenshot actual rendered ledger; exercise filters, detail selection and history loading; verify no document horizontal overflow or overlapping date headings.
- Update MEMORY.md with final behavior, exact commands, evidence and known limitations. Do not claim production deployment from local QA. No commit/push/deploy requested in this task.

## Execution
Implementation assigned to Gemini/gemini-3.8-flash-high at the user's explicit request. Parent agent reviews code and performs final acceptance. Existing dirty changes belong to this task and must be preserved or superseded intentionally, never reset wholesale.