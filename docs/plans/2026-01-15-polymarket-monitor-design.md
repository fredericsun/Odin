Title: Polymarket Monitor v1 Design
Date: 2026-01-15
Status: Draft (validated)

## Summary
Build a local-first web app that monitors Polymarket for unusual odds and liquidity moves, explains them using public sources, and maps high-confidence events to tradable instruments with clear risk checks and ranked opportunities. The system is alert-driven (email) with a daily 7am local report, plus a minimal dashboard for review and configuration.

## Goals
- Detect unusual moves using hybrid thresholds (absolute, relative, and statistical).
- Produce cited explanations using public sources and an LLM.
- Map events to tradable instruments across Polymarket, crypto, and equities.
- Rank opportunities with transparent component scoring.
- Run locally with minimal infra and simple, reliable operations.

## Non-Goals (v1)
- Automated trade execution.
- Paid data APIs or vendor-specific premium feeds.
- Full-featured analytics UI or advanced charting.
- Long-term data warehousing beyond 7 days.

## Constraints and Requirements
- Markets: Polymarket only (official public APIs only).
- Default market scope: top 50 by liquidity; user can change later.
- Alerts: email only (Gmail SMTP), near-real-time via polling.
- Report: daily at 7am local time.
- Storage: local Postgres, derived data only.
- Retention: 7 days of derived events and report history.
- LLM: OpenAI `gpt-4o-mini`.
- Market data (free sources): Alpha Vantage + Stooq (equities), Binance + Coinbase public endpoints (crypto).
- Hosting: local machine only; dashboard bound to 127.0.0.1.

## Architecture Overview
- Single local service running:
  - Polymarket collector (polling).
  - Signal engine (hybrid anomaly detection).
  - Decision engine (risk checks + scoring).
  - Explanation engine (public sources + LLM).
  - Instrument mapper (rules + entity matching).
  - Ranker (weighted score).
  - Alerting and report scheduler.
  - FastAPI backend + minimal Next.js dashboard.

## Data Flow
1. Poll Polymarket public API every 60 to 120 seconds for top 50 markets.
2. Update in-memory ring buffer (recent snapshots) per market.
3. Compute deltas and rolling stats; emit a `MarketEvent` on threshold breach.
4. Score the event and apply position-size risk check.
5. If above score threshold, enrich with public sources and LLM explanation.
6. Map the event to instruments and fetch optional free price context.
7. Rank and store the opportunity, then send an email alert.
8. Daily report compiles the last 24 hours into a single email.

## Hybrid Anomaly Detection
Trigger an event if any of these fire:
- Absolute odds jump over configured percent in a short window.
- Relative move above percentile vs last 7 days.
- Volume spike above absolute and relative thresholds.
- Liquidity spike above absolute and relative thresholds.
- Z-score anomaly using recent in-memory window.

## Explanation Engine
- Inputs: event context + public sources.
- Sources: official announcements, public RSS/news feeds, and reputable public web sources.
- Output: short, cited narrative with confidence score.
- Fail-closed: missing sources reduce confidence; alerts still sent with warning.

## Instrument Mapping
- Rule-based mapping with entity extraction from market question and sources.
- Maps to:
  - Polymarket related markets.
  - Crypto pairs (Binance/Coinbase).
  - Equities/ETFs (Alpha Vantage/Stooq symbols).
- Adds rationale and optional price context from free APIs.

## Ranking Model (v1)
Weighted score = odds move + volume spike + liquidity spike + LLM confidence + source count.
- Transparent component weights, configurable in settings.
- Used for both alerts and daily report ordering.

## Risk Checks (v1)
- Single max position size limit applied to recommendations.
- Advisory-only output; no execution or account access.

## Dashboard and UX
Minimal local dashboard with:
- Recent alerts list and detail view (explanation + citations).
- Top opportunities table.
- Daily report history.
- Settings: thresholds, cooldown, report time, market scope, position cap.
- API key inputs and test email action.

## Storage Model (Postgres)
Derived-only tables:
- `markets`: metadata and status.
- `baselines`: rolling stats (mean/std) per market.
- `events`: anomalies with component scores and timestamps.
- `explanations`: summaries, confidence, citations.
- `instrument_mappings`: instrument links and rationale.
- `alerts`: send status and timestamps.
- `reports`: daily report summary and top events.
- `settings`: single-row configuration.

In-memory ring buffer:
- Per-market recent snapshots (odds, volume, liquidity).
- Rebuilt on restart from recent stored stats to avoid cold starts.

## Error Handling and Reliability
- Short timeouts and capped retries for external sources.
- Cycle-level isolation (a single failed poll does not crash the service).
- Alert dedupe window and rate limits to avoid flooding.
- Missing explanation sources downgrade confidence rather than blocking.
- Health endpoint and run-once debug endpoint for inspection.

## Testing Strategy
- Unit tests for anomaly detection and ranking.
- Integration tests for alerting and dedupe rules using mocked APIs.
- Mocked LLM tests to validate citation requirements and confidence handling.
- Dry-run mode and test email function for operational validation.

## Open Questions
- Exact Polymarket API endpoints and rate limits to use.
- Preferred set of public news sources (initial RSS list).
- Final threshold defaults for odds, volume, and liquidity spikes.
