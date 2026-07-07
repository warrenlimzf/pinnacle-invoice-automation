# Session handoff — V2 (API edition) built as sibling repo; V1 untouched

> Persistent resume file. Paste into a fresh session (or auto-load via a SessionStart hook).
> Delta only — project overview, roles, and decisions live in CLAUDE.md & docs (auto-loaded).

**Role:** Warren's agent maintaining the bank-NAV tool his non-technical colleague runs
on Windows. As of this session there are TWO sibling repos: this one (V1, fully local,
recommended) and `../pinnacle-invoice-automation-api` (V2, Gemini-API OCR for scans).

## Status — updated 2026-07-07 (V2 build session)
- **V2 shipped:** mentor asked for a Gemini-API variant (company subscription pays).
  Built at `../pinnacle-invoice-automation-api`, pushed to public GitHub
  `warrenlimzf/pinnacle-invoice-automation-api` (commit `51cceba`). One functional
  change vs V1: image-only pages → `shared/readers/gemini_ocr.py` (stdlib urllib, key
  in gitignored `api_key.txt`, `check_api.bat` self-test). Stress-tested 8/8 failure
  modes (API mocked) + 5/5 real samples incl. all 3 scanned pages (V1 RapidOCR
  transcripts replayed as mock Gemini responses). Details: V2's CLAUDE.md +
  docs/STATUS.md + SESSION_HANDOFF.md over there.
- **This repo (V1): zero code changes.** Only edits: CLAUDE.md Open section got a
  one-line V2 pointer, and this handoff. V1 code stays exactly as validated at `fa6a820`.

## Next actions
1. (V1, unchanged from last session) Await colleague's re-run on the latest ZIP:
   confirm UBS fills via the first-table rule + LGT tab populated. If UBS still wrong →
   `diagnose.bat UBS`, she sends the .txt, fix parser from real wording, log in the
   debug journal, run both test scripts, push.
2. (V2) When the company key is available: `check_api.bat` → SUCCESS, then one scanned
   LGT statement end-to-end; eyeball the docx. The live Gemini call has never been made.

## Running state
- Background processes: none
- Dev servers / ports: none
- Worktrees / branches: both repos on `main`, clean, pushed

## Open items
- V1: colleague re-run pending (above); multi-client-per-PDF unsupported; fee rule
  (`MGMT_FEE_RATE`) unset — queue, don't start unasked.
- V2: live API shakedown pending (needs company key); `config.GEMINI_MODEL` may need
  updating if the company standardises on another model.
- Rule to keep: never edit V1 from a V2 session or vice versa; shared-logic fixes go to
  BOTH repos separately (siblings, not linked).

## Pick up here
If Warren brings colleague feedback about UBS/LGT values → work in V1 (diagnose flow).
If he brings the company Gemini key or V2 feedback → work in
`../pinnacle-invoice-automation-api`.
