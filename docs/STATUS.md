# STATUS

## First live run on colleague's PC (2026-07-07, session 4) — fix shipped, awaiting her re-run
- Her first real run: BoS wrote 6 rows fine; UBS and LGT tabs came out COMPLETELY empty
  (not even flagged rows). Root cause class confirmed locally: any per-file exception in
  the parser (proven triggers: password-protected PDF → PyMuPDF `ValueError: document
  closed or encrypted`; OCR engine crash; full-scan PDF) was logged but wrote NO Excel row.
- Fix (commit `a5ffceb`): encrypted PDFs detected with a plain-English error; OCR call
  guarded; any parse failure now writes a visible **FAILED row** with the fix in Flags;
  failed files are not marked processed → auto-retry next run.
  `tests/test_failure_modes.py` (synthetic PDFs) locks all three modes in.
- CONFIRMED from her re-run (same day): OCR IS installed and working on her PC. Her LGT
  files are full scans (20+ pages, ~10s OCR per page → 3–4 min per file); BoS has a text
  layer → instant. The original empty tabs were almost certainly the window being closed
  mid-OCR. Commit `56c8b4e` adds a "scanned statement, ~10s/page, NOT stuck — leave the
  window open" log notice. She just lets a full run finish once; done files are hash-skipped
  forever after.

## Done & VERIFIED against 5 REAL statements (2026-07-07, session 3)
- 3 banks (LGT, BoS, UBS), each with `inbox/` + its own real `parser.py`.
- Folder-watch trigger (`watcher.py`) + manual run (`run_all_once.py`).
- Launchers for BOTH OSes: `*.command` (Mac) and `*.bat` (Windows).
- Pipeline: PDF → date/account/ccy/Gross/Net/Liquidity → master Excel (3 tabs) →
  section screenshot → per-bank `.docx`.
- Local-only extraction via PyMuPDF + optional local OCR (RapidOCR) fallback for
  image-only pages (NOT MinerU — MinerU uploads to cloud; forbidden here).
- File-safety: originals never moved/deleted; de-dupe by content hash.
- `tests/validate_samples.py`: all 5 supervisor samples pass to the cent
  (expected values transcribed from her green-boxed guide copies).

## Extraction logic (validated on the real layouts)
- **UBS** — multi-portfolio statements; the portfolio number suffix (`546-123456-03`)
  selects the "Portfolio 03" table; reads Gross assets / Net assets / Liquidity from
  the **Market value** column (space thousands). Header "Total gross/net assets" =
  whole relationship = deliberately NOT used (kept only as single-portfolio fallback).
- **BoS** — Gross = "Investment Assets", Net = "Total Net Asset Value"; parentheses =
  negative (an overdrawn client has negative Net); Liabilities (Overdrafts) captured
  with an Excel check formula Gross+Liab−Net=0.
- **LGT** — Net = allocation "Total"; negative rows (Credit, Derivatives…) added back;
  Gross = live Excel formula `=Net-SUM(addbacks)`; Liquidity from its own row.
- All banks: Account No / Currency / Statement Date read off the header. Multi-page
  PDFs: the engine finds the overview page by its text fingerprint first.
- Columns A–F (the copy block): Statement Date | Account No | Currency | Gross NAV |
  Net NAV | Liquidity. Hardcoded = DARK BLUE, formulas = BLACK.

## Samples policy (important)
- Real client samples + supervisor's guide live in `samples/` (raw + green-boxed guide
  + `pdf automation guide.xlsx`). **Gitignored — the repo is public; client data never
  leaves this machine.** The layout knowledge is encoded in parsers/docs instead.

## Open
1. First LIVE month with the colleague's own statements (fresh multi-page PDFs).
2. Multiple clients per PDF — parsers currently assume one account per PDF.
3. `MGMT_FEE_RATE` still unset (fee rule to be agreed).

## Deferred (placeholders left in)
- Email ingestion / more file formats — add a new reader in `shared/readers/`.

## Earlier sessions
- 2026-06-29 (session 2): went live on public GitHub `warrenlimzf/pinnacle-invoice-automation`
  (colleague uses Download ZIP, no account); renamed workbook to `nav_master.xlsx`;
  re-drop = force reprocess; `--redo` rebuilds all; email + rulebook docs added.
- Session 1: core pipeline built from synthetic layouts; Windows wheels vendored
  (Py 3.11–3.13); Windows = colleague's OS confirmed.

## Superseded
- `docs/FOR_COLLEAGUE_AI.md` (her AI fills Account No) — obsolete: the engine now reads
  the account number off every statement header itself.
