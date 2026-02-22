# Technical Changes and Implementation Notes

## Overview
- Introduced explicit HTTP contract, hardened scraper pipeline, improved concurrency and observability, stabilized runner/CLI, and added dev automation. Validated REST execution end-to-end with enrollment and statistics.

## HTTP Contract
- Added `Result[T,E]` and `HttpRequestFailed` with `retryable`.
- `http_get(url, headers=None, timeout=15) -> Result[bytes, HttpRequestFailed]`.
- Retryable rules: timeouts/5xx → true; 403/404 → false; other 4xx → false.
- References: `udemy_enroller/types.py:1`, `udemy_enroller/http_utils.py:9`.

## Scraper Updates
- All scrapers now consume `Result` and gate parsing on `res.ok`.
- References:
  - `udemy_enroller/scrapers/tutorialbar.py:85,101`
  - `udemy_enroller/scrapers/discudemy.py:49,72`
  - `udemy_enroller/scrapers/freebiesglobal.py:49,77`
  - `udemy_enroller/scrapers/idownloadcoupon.py:68`
  - `udemy_enroller/scrapers/coursevania.py:69,104,127`

## Concurrency & Fuzz
- `FuzzManager` enforces `HARD_MAX_CONCURRENCY=20` clamp with warning.
- Aggregated counters: total/success/error/timeout and total `duration`.
- Single-line summary `fuzz_summary total=... duration=...s urls=...`.
- References: `udemy_enroller/scrapers/fuzz_manager.py:12,40`.

## Runner & CLI Stabilization
- `RunConfig` dataclass introduced for stable API across CLI/Runner.
- CLI accepts `--email` and `--password`, setting env before `Settings`.
- Runner initializes `asyncio` event loop if missing (Python 3.12+).
- UI runner falls back to REST on failure, ensures browser quit.
- References: `udemy_enroller/run_config.py:1`, `udemy_enroller/cli.py:240`, `udemy_enroller/runner.py:36,145,250`.

## Settings & Credentials
- Removed `distutils`; implemented `_strtobool` compatible with 3.12+.
- Credential collection:
  - Use `UDEMY_EMAIL`/`UDEMY_PASSWORD` if set.
  - Fallback to `getpass`; on failure, non-hidden `input`.
- References: `udemy_enroller/settings.py:32,97,119`.

## UI Login Hardening
- Attempt cookie-based login (inject `access_token/client_id/csrftoken`).
- Fallback to interactive login:
  - Multiple selectors and iframe traversal for email/password fields.
  - Submit via `auth-submit-button` or `//button[@type='submit']`.
- References: `udemy_enroller/udemy_ui.py:97,100,114`.

## Developer Experience
- Scripts (PowerShell):
  - `scripts/setup.ps1`: venv + install + dev deps
  - `scripts/run-ui.ps1`: activates venv and runs UI
  - `scripts/run-rest.ps1`: activates venv and runs REST
  - `scripts/test.ps1`: ensures dev deps then runs `pytest`
  - `scripts/build.ps1`: build artifacts
- CI Workflow:
  - `.github/workflows/ci.yml`: Windows/Ubuntu/macOS with Python 3.12

## Tests Added
- BaseScraper `time_run` marks COMPLETE on exceptions.
- FuzzManager clamp and run path produce at least one URL and clamp active.
- References: `tests/test_base_scraper_time_run.py:1`, `tests/test_fuzz_manager.py:1`.

## Observability & Logging
- Debug mode raises stream and file handlers to DEBUG.
- `fuzz_summary` logs single-line execution metrics.
- `RunStatistics.table` emits consolidated stats.
- References: `udemy_enroller/logger.py:17`, `udemy_enroller/scrapers/fuzz_manager.py:40`, `udemy_enroller/udemy_rest.py:58`.

## Security & Safety
- No secrets printed; credentials via env/flags; cookies persisted to app dir.
- HTTP `retryable` enables safer backoff decisions in future work.

## Usage Summary
- REST:
  - `python run_enroller.py --debug --email <EMAIL> --password <PASSWORD>`
- UI with REST fallback:
  - `python run_enroller.py --browser chrome --debug --email <EMAIL> --password <PASSWORD>`
- Scripts:
  - `.\scripts\setup.ps1`, `.\scripts\run-ui.ps1 -Browser chrome -Debug`, `.\scripts\run-rest.ps1 -Debug`.

## Validation Outcome
- Verified REST flow end-to-end with successful enrollment and stats.
- UI remains guarded by site anti-automation; runner falls back to REST automatically and completes.
