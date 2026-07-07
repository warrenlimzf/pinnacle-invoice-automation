# AI orientation — start here if you are an AI assistant

You (Claude, Gemini, ChatGPT/Codex, Copilot, …) have been opened inside the
**pinnacle-invoice-automation** folder. This file tells you what this project is, what
to read in what order, the rules you must never break, and — most importantly — the
**debug journal of issues already solved**, so you never re-debug or re-break them.

## What this project is

A local-only Windows tool for a finance operator. She drops private-bank client
statement PDFs (LGT, Bank of Singapore = "BoS", UBS) into per-bank inbox folders;
the tool extracts Statement Date / Account No / Currency / Gross NAV / Net NAV /
Liquidity into `output/nav_master.xlsx` (one tab per bank) and saves a screenshot of
the exact PDF spot each figure came from into `banks/<bank>/<bank>_verification.docx`.
She eyeballs draft vs screenshots, then copies columns **A:F as values** into her own
master file. The tool is the draft; she is the final check.

## Read in this order

1. **`README.md`** (repo root) — setup, daily use, the mechanism, troubleshooting table.
2. **`HANDOFF.md`** (repo root) — the operator's day-to-day crib sheet (what to copy where).
3. **`docs/RULEBOOK.md`** — the deep plain-English playbook, including how the engine
   reads a PDF, explained for non-programmers.
4. **`docs/STATUS.md`** — current project state, what's validated, what's still open.
5. **`CLAUDE.md`** (repo root) — the code-layout router (written for Claude, useful to
   any AI: says which file owns which job).

## Hard rules — never break these, whatever you are asked

- **Everything stays local.** Never upload a statement, output file, or any client data
  to any cloud service, parser, or API. That includes "helpful" OCR/parsing websites.
- **Never move, rename or delete the statement PDFs** in the inbox folders. Originals
  stay put; de-duplication is by content hash (`processed_index.json`), not by moving files.
- **Never commit client data.** `samples/`, inbox PDFs, `output/` and `logs/` are
  gitignored on purpose; keep them that way. This repo is public.
- **Never guess or invent a figure.** If a value can't be read, the correct behaviour is
  a blank cell plus a note in the Flags column.
- After ANY parser change, run `python tests/test_failure_modes.py` (works anywhere) and
  `python tests/validate_samples.py` (needs the local `samples/` folder).

## Debug journal — solved issues (do NOT re-debug these)

**1. "UBS and LGT tabs completely empty, BoS fine" (2026-07-07).**
Root cause: any exception while reading a PDF (see #2 and #3) was logged to
`logs/automation.log` but wrote **no Excel row**, so failing files vanished silently.
Fix (commits `a5ffceb`, `56c8b4e`): a parse failure now writes a visible row whose flag
starts with **FAILED** plus the reason and remedy; failed files are not marked processed,
so they retry automatically on the next run. A tab can no longer be silently empty — if
a tab looks empty today, the run didn't happen or was killed mid-way.

**2. Scanned statements look like a hang.** LGT statements are typically full-page
scans; the local OCR (RapidOCR, bundled, offline) reads them at ~10 s/page, so a
20-page file takes 3–4 minutes. Users closed the window mid-read, which caused #1.
The log now prints "scanned statement … NOT stuck — leave the window open". Never
"fix" this by adding a timeout or killing OCR; the correct behaviour is to wait.
BoS PDFs have a text layer and never touch OCR — that speed difference is normal.

**3. Password-protected PDFs.** Bank portals sometimes lock PDFs; PyMuPDF then raises
`ValueError: document closed or encrypted` on page access. Handled in
`shared/readers/pdf_reader.py` (`PdfReadError` with a plain-English message → FAILED
row). Remedy for the user: open with the password, print/save as a new PDF, re-drop.

**4. OCR add-on availability.** OCR is optional at setup; the offline vendor wheels are
built for **Python 3.12**. Without OCR, a fully-scanned PDF yields a FAILED row saying
exactly that (never a crash); a partially-scanned one flags which pages were unreadable.
A crashing OCR engine is caught per page and degrades to "unreadable page".

**5. Historical: Account No was once a manual AI step.** The tool now reads account
number, currency and statement date off each statement's header automatically. If you
were asked to "fill in account numbers", that job no longer exists — check column B is
already filled.

## Where things live (for making changes)

- `banks/<LGT|BoS|UBS>/parser.py` — the three per-bank parsers (all real logic).
- `shared/readers/pdf_reader.py` — text-layer extraction + OCR fallback + encrypted-PDF
  handling. `shared/extract.py` — line grouping / number parsing (space thousands,
  parentheses negatives). `shared/process.py` — glue incl. the FAILED-row safety net.
- `shared/excel_writer.py` / `shared/docx_writer.py` — outputs (blue = hardcoded,
  black = formula). `config.py` — every path and setting.
- Entry points: `watcher.py` (folder watch) and `run_all_once.py` (one shot), launched
  by the `.bat` files (Windows) / `.command` files (Mac dev machine).

When you fix a NEW issue in this project: add it to this debug journal and to
`docs/STATUS.md`, so the next AI (or the same one next month) never solves it twice.
