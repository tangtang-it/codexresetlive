# CodexReset.live Data Credibility Remediation Plan

> Supersedes the previous SEO and multilingual-expansion plan on 2026-11-01.
> The product KPI is evidence integrity, not page count.

## P0 — Block publication of incorrect reset facts

1. **Canonical event ledger**
   - Use one immutable event record per source post and a separate derived claim record only when it has explicit evidence.
   - Require: source URL, source author, publishedAt, claim type, scope, evidence excerpt, verification state, and reviewer/source provenance.
   - Do not count a post as a reset merely because it contains `reset`, `banked`, or a future-tense promise.

2. **Scope and state vocabulary**
   - `public_global_reset`: evidence of an automatic public quota reset; account coverage remains explicitly bounded by the source.
   - `banked_credit`: a discretionary credit which must be claimed/applied; never presented as an immediate quota reset.
   - `personal_rolling_window`: user-specific recovery estimate; never inferred from public announcements.
   - `notice_only`, `claim_unverified`, and `unknown`: do not drive hero status, calendar reset markers, or reset counts.

3. **Publication rules**
   - The hero and calendar consume only `effective_confirmed` records.
   - The ledger exposes every observed record, with its raw source and state; it must not silently promote a notice to a reset.
   - API failure is visibly unavailable and preserves only last known, source-linked static history. No numeric or status fallback may be invented.

## P1 — Make the forecast falsifiable

1. Replace “1% probability” with a clearly named heuristic signal until a documented, versioned model has a backtest, calibration window, sample size, and scorecard.
2. Publish a versioned history API with stable IDs, timestamps, scope, state, source URLs, corrections, and `generatedAt` freshness metadata.
3. Generate structured data only from published, source-linked facts. Do not put forecasts, unverified scope, or synthetic counts into JSON-LD.

## Acceptance gates

- A fixture suite proves: duplicate source posts are deduplicated; a future promise remains `notice_only`; banked credit never increments public-reset count; personal recovery never changes public-reset status; and an unavailable upstream cannot fabricate a result.
- Browser QA verifies ledger count, row state, inspector source, hero, calendar, API response, and JSON-LD all agree for the same stable event ID.
- Every displayed reset must be traceable from UI to API to a source URL and evidence excerpt in one hop.

## Explicitly stopped

- No new locales, page families, page-count targets, or cosmetic forecast upgrades before P0 is closed.
- Existing locales remain maintained only for correctness regressions; they are not an expansion program.
