# Session handoff — real samples in, parsers rebuilt + validated, docs refreshed, pushed

> Persistent resume file. Paste into a fresh session (or auto-load via a SessionStart hook).
> Delta only — project overview, roles, and decisions live in CLAUDE.md & docs (auto-loaded).

**Role:** Solo — Claude assisting Warren. No multi-agent setup.

## Status — updated 2026-07-07 (session 3)
- Supervisor's real samples arrived (Warren's Downloads). Copied to `samples/`
  (raw + green-boxed guide + `pdf automation guide.xlsx`). **Gitignored — repo is
  public, client data never leaves the machine.** Originals still in ~/Downloads.
- Parsers REBUILT to the real layouts and **all 5 samples validate to the cent**
  (`python tests/validate_samples.py`): UBS portfolio-suffix table selection
  (Market value column), LGT add-backs + Liquidity, BoS parens-negatives +
  Overdrafts + check formula. New fields everywhere: Date, Account No, Currency,
  Liquidity. Column order (his spec): Date | Acct | Ccy | Gross | Net | Liquidity.
- LGT/UBS samples were IMAGE-ONLY PDFs → added optional local OCR fallback
  (RapidOCR, whitespace-insensitive label matching in `shared/extract.py`).
  Windows OCR wheels (py3.12) vendored; `setup.bat` installs them offline,
  optional + skippable. Core pipeline needs no OCR for born-digital statements.
- Docs refreshed: RULEBOOK (+ §7b mechanism-for-amateurs), EMAIL (copy A:F, account
  auto), HANDOFF, STATUS, CLAUDE.md; FOR_COLLEAGUE_AI marked SUPERSEDED.
- E2E run artifacts exist locally (output/nav_master.xlsx, verification docx,
  snapshots) from the sample run — all gitignored.

## Next actions
1. First live month: colleague drops her own fresh multi-page statements; watch Flags.
2. Multiple clients per PDF still unsupported (one account per PDF assumed).
3. `MGMT_FEE_RATE` still unset.

## Running state
- Background processes: none · Dev servers: none · Branch: main (pushed).

## Pick up here
- Any parser tweak → rerun `python tests/validate_samples.py` (needs local `samples/`).
- If Warren asks technical how/why questions → extend
  `second-brain/Personal/Dev/Learn - Pinnacle Invoice Automation.md` (global §14).
