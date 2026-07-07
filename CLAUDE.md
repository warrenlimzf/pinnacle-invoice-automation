# Pinnacle Invoice / Fee Automation — router

Local-only tool: reads bank client-statement **PDFs** (multi-page), finds the overview
page, pulls **Date + Account No + Currency + Gross NAV + Net NAV + Liquidity**, writes
them to a master Excel (3 tabs, finance-formatted), and screenshots the exact PDF section
each number came from into a per-bank Word doc for human eyeball verification.

**VALIDATED against 5 real supervisor samples (2026-07-07)** — see `tests/validate_samples.py`.
Real samples + the supervisor's guide live in `samples/` (**gitignored — client data,
repo is public; never commit or upload**). Bank specifics (from her green-boxed guide):
- **UBS** multi-portfolio: portfolio-number suffix (`546-123456-03`) picks the
  "Portfolio 03" table; Gross/Net/Liquidity/Liabilities from the **Market value**
  column; SPACE (also apostrophe) thousands. Header "Total gross/net assets" = whole
  relationship, wrong. ALSO exports one PDF PER portfolio (colleague's real files):
  no "Portfolio NN" headings, client's own portfolio printed FIRST → read the FIRST
  table (cut at the first "Net assets" row; flag for eyeball when several tables).
- **BoS** Gross = "Investment Assets"; Net = "Total Net Asset Value"; parentheses =
  negative (Net can be negative); Overdrafts captured + check formula Gross+Liab−Net=0.
- **LGT** only Net ("Total" of allocation table); Gross = Excel formula adding back
  negative rows (Credit, Derivatives…); Liquidity row read too.
Excel columns A–F (her copy block): Date | Account No | Currency | Gross | Net | Liquidity.
Hardcoded = DARK BLUE font, formulas = BLACK.

## 🔒 Hard constraints (client banking data — non-negotiable)
- **Everything runs locally. Nothing is ever uploaded.** No cloud parsers (this is
  why we use local `PyMuPDF` + optional local RapidOCR, NOT MinerU — MinerU uploads
  to its cloud). `samples/` and inbox PDFs stay out of git (see `.gitignore`).
- **Never move/delete the colleague's statement PDFs.** Originals stay in `inbox/`.
  De-duplication is by content hash in `processed_index.json`, not by moving files.
  Re-do: a freshly (re)dropped PDF force-reprocesses (overwrites its row); startup
  catch-up still skips already-done files. `run_all_once.py --redo` rebuilds all.
- Builds on Mac, **runs on Windows**. Keep all code cross-platform (use `pathlib`,
  no hard-coded `/` or `\` paths). The `.bat` files are the Windows entry points.

## Layout (what each piece does)
- `config.py` — ALL paths + the fee setting (`MGMT_FEE_RATE`). One place to tweak.
- `watcher.py` — auto-trigger: watches the 3 inboxes, processes new PDFs.
- `run_all_once.py` — manual one-shot processing. `diagnose.py`/`.bat` — dumps the
  seen-text of inbox PDFs to `logs/diagnose/*.txt` (local) for layout debugging.
- Launchers: `*.command` (Mac) + `*.bat` (Windows): setup / run_watcher / run_once.
- `banks/<LGT|BoS|UBS>/parser.py` — the **3 distinct per-bank parsers** (real logic).
- `shared/extract.py` — line grouping, number parsing (commas, space thousands,
  parens negatives) + whitespace-insensitive label matching (OCR-safe).
- `shared/readers/pdf_reader.py` — PyMuPDF text layer; local OCR fallback (RapidOCR,
  optional) for image-only pages.
- `shared/fees.py` — LGT Gross-from-add-backs. `shared/process.py` — the glue.
- `shared/excel_writer.py` — master workbook; blue=hardcoded, black=formula; upsert by
  filename; BoS liabilities + check column; LGT add-backs from col N.
- `shared/docx_writer.py` — per-bank verification `.docx` (values + add-backs + snapshots).
- `shared/snapshot.py` — renders a PDF section to PNG.
- `tests/validate_samples.py` — run after ANY parser change; needs local `samples/`.
- `tests/test_failure_modes.py` — synthetic PDFs, runs anywhere: encrypted /
  OCR-crash / scan-without-OCR must each yield a visible **FAILED row** (flag says
  the fix), never a silently empty tab; failed files aren't marked processed → auto-retry.
- `output/nav_master.xlsx` — generated. `logs/` — run log + snapshot PNGs.
- `README.md` — the canonical GitHub-facing guide (colleague reads GitHub directly now:
  combined steps where Python install is step 1 one-time and every update starts from
  step 2, mechanism, troubleshooting of all known issues). Docs: `docs/RULEBOOK.md` —
  deep plain-English playbook; `docs/FOR_COLLEAGUE_AI.md` — AI orientation for the
  colleague's AI (reading order, hard rules, DEBUG JOURNAL of solved issues — append new
  fixes there + STATUS.md). EMAIL_TO_COLLEAGUE / STATEMENT_SPEC_TEMPLATE deleted
  2026-07-07 (superseded, Warren-authorized).

## Runtime / handoff facts
- Colleague runs on **Windows** → `.bat` launchers (`.command` are Mac, ignored).
- Deps pre-bundled in `vendor/` (Windows wheels; core = Py 3.11–3.13, OCR extras =
  Py 3.12) → `setup.bat` installs **offline** (`--no-index --find-links vendor`,
  online fallback; OCR is optional and skippable). Recommend Python 3.12.
- Outputs are a **DRAFT/staging** area, not her master file. Copy table = the A:F
  block (Date | Account No | Ccy | Gross | Net | Liquidity); paste as VALUES.
- `HANDOFF.md` (root) = AI-readable handoff for the colleague.
- **GitHub (deployment):** public repo `warrenlimzf/pinnacle-invoice-automation`.
  Colleague gets it via `git clone` or **Code → Download ZIP** (no account needed,
  no `.venv` carried). She then runs `setup.bat` to build a fresh Windows `.venv`.

## Open (see docs/STATUS.md)
- **V2 sibling exists (2026-07-07, mentor's request):** `../pinnacle-invoice-automation-api`
  (GitHub `warrenlimzf/pinnacle-invoice-automation-api`) — same tool, scanned pages read
  via the company's Gemini API instead of RapidOCR. THIS repo stays the recommended
  local-only version and stays as-is; shared-logic fixes must be applied to both repos
  separately (siblings, not linked).
- AWAITING colleague's re-run on the latest ZIP (`fa6a820`): confirm UBS values fill
  via the new first-table rule + LGT tab populated. If UBS still wrong → she runs
  `diagnose.bat UBS`, sends the .txt → fix parser from real wording, never guess.
- Multiple clients per PDF (parsers assume one account per PDF). Fee rule unset.

## Run (dev)
`python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(+ `pip install -r requirements-ocr.txt` for scanned PDFs)
then `python run_all_once.py` (after a PDF is in an inbox).
`python tests/validate_samples.py` = the regression check.
