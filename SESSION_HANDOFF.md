# Session handoff — first live-run debugging (empty tabs → FAILED rows, UBS first-table rule, docs overhaul)

> Persistent resume file. Paste into a fresh session (or auto-load via a SessionStart hook).
> Delta only — project overview, roles, and decisions live in CLAUDE.md & docs (auto-loaded).

**Role:** Warren's agent maintaining the local-only bank-NAV tool his non-technical
colleague runs on Windows (she downloads ZIPs from the public GitHub repo; Warren relays
her screenshots/logs here).

## Status — updated 2026-07-07 (session 4, evening)
- Colleague's first live run debugged end-to-end. Root causes found and fixed, all
  pushed through commit `fa6a820`. Full chronicle: docs/STATUS.md (session-4 block) and
  the debug journal in docs/FOR_COLLEAGUE_AI.md — don't re-derive from chat.
- Shipped this session (each with regression tests in tests/test_failure_modes.py,
  runnable anywhere, no client data): FAILED-row visibility (no silently empty tabs,
  failed files auto-retry), encrypted-PDF + OCR-crash + scan-without-OCR handling,
  "NOT stuck" OCR notice, UBS one-PDF-per-portfolio support (no heading → read FIRST
  table, cut at its "Net assets" row; Warren's rule), UBS Liabilities + Check column,
  apostrophe thousands, diagnose.py/.bat text-dump tool.
- Docs overhauled: README = colleague's canonical GitHub guide (steps: Python once,
  updates start from "Download ZIP"); FOR_COLLEAGUE_AI.md = AI orientation + debug
  journal; EMAIL_TO_COLLEAGUE.md + STATEMENT_SPEC_TEMPLATE.md deleted (authorized).
- Global CLAUDE.md gained §8.7: solved issues get logged in the project's docs.
- Learn note grown 3 sections (second-brain/Personal/Dev/Learn - Pinnacle Invoice
  Automation.md): text-layer vs scan + OCR, parser signposts + ordered fallbacks,
  where rules live + diagnose as the visible pdf-as-text stage.
- Validation state: 5 real samples pass to the cent; 5 synthetic failure-mode/UBS
  tests pass. Her REAL UBS files not yet confirmed — she was told to download the
  latest ZIP and re-run.

## Next actions
1. When Warren reports her re-run: confirm UBS tab fills C–H (incl. new Liabilities +
   Check) and LGT tab has values. If UBS still wrong: she runs `diagnose.bat UBS`,
   Warren pastes the .txt → fix banks/UBS/parser.py against real wording, add the fix
   to the debug journal (global CLAUDE.md §8.7), run both test scripts, push.
2. If all good: consider updating samples/expected.json equivalents only if Warren
   supplies her real figures (samples/ stays local, never committed).

## Running state
- Background processes: none
- Dev servers / ports: none
- Worktrees / branches: main only, clean, pushed (`fa6a820`)

## Open items
- Colleague's confirmation of the UBS first-table fix on her real files — everything
  else this session is verified by tests.
- Fee rule (`MGMT_FEE_RATE`) still unset; multiple-clients-per-PDF still unsupported
  (queue, per CLAUDE.md §Open — don't start unasked).

## Pick up here
Ask Warren whether the colleague re-ran with the latest ZIP; judge her UBS/LGT tabs
(or her diagnose .txt) and iterate on banks/UBS/parser.py if needed.
