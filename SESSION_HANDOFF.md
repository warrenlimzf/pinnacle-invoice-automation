# Session handoff — read-tracking + NEEDS_REUPLOAD report added; README restyled

> Persistent resume file. Paste into a fresh session (or auto-load via a SessionStart hook).
> Delta only — project overview, roles, and decisions live in CLAUDE.md & docs (auto-loaded).

**Role:** Warren's agent maintaining the bank-NAV tool his non-technical colleague runs on
Windows. Two sibling repos exist: this one (V1, fully local, recommended) and
`../pinnacle-invoice-automation-api` (V2, Gemini-API OCR). This session's changes were made
to BOTH, separately (siblings, not linked) — Warren explicitly authorised editing V1 here.

## Status — updated 2026-07-08
- **Read tracking added** (see CLAUDE.md §Hard-constraints "Read tracking"): `shared/index.py`
  gained `mark_failed`/`clear_failed`/`collect_unread`/`write_reupload_report`; `mark_processed`
  now clears the failed record. `config.py` gained `FAILED_INDEX` + `NEEDS_REUPLOAD_REPORT`.
  `run_all_once.py` + `watcher.py` record the failure reason, regenerate
  `output/NEEDS_REUPLOAD.txt` every run, and print the not-read list. `.gitignore` adds
  `failed_index.json` + `output/NEEDS_REUPLOAD.txt`.
- What this solves: files are read one at a time (a bad file never blocks others — already the
  case) and now there's a persistent, human-readable record of which files were NOT read + a
  remove/re-upload protocol. Failed files still auto-retry.
- **Verified:** V1 5/5 failure-mode tests pass; all edited files compile.
- **README rewritten** in Warren's claude-web-design house style (emoji headers, linked shields
  badges, 30-sec table, TOC, is/isn't lists, tables). All facts preserved. See memory
  `readme-house-style`.
- Committed + pushed to public GitHub `warrenlimzf/pinnacle-invoice-automation`.

## Next actions
1. Nothing required from this session's work — shipped and verified.
2. Carry-over (unchanged): confirm the colleague's re-run on the latest ZIP (UBS first-table
   rule + LGT tab populated); if UBS still wrong she runs `diagnose.bat UBS` and sends the .txt.
   Fee rule still unset. See CLAUDE.md §Open.

## Running state
- Background processes: none
- Dev servers / ports: none
- Worktrees / branches: on `main`, clean, pushed

## Open items
- Colleague re-run confirmation + fee rule — carry-over, see CLAUDE.md §Open.

## Pick up here
Work is shipped and green. Await the colleague's re-run result, or Warren's next request.
Keep V1 and V2 in sync manually when touching shared logic (they are not linked).
