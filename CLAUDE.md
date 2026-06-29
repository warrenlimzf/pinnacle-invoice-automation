# Pinnacle Invoice / Fee Automation — router

Local-only tool: reads bank client-statement **PDFs**, pulls **Gross NAV + Net NAV**,
writes them to a master Excel (3 tabs, finance-formatted), and screenshots the exact PDF
section each number came from into a per-bank Word doc for human eyeball verification.

Real sample layouts are in `invoice examples/` (LGT.png, BoS.png, UBS.png) — the parsers
are tuned to these. Bank specifics:
- **UBS** "Total gross assets"/"Total net assets"; SPACE thousands + SGD prefix.
- **BoS** Gross = "Assets" (100%) row; Net = "Total Net Asset Value".
- **LGT** only Net ("Total"); Gross = Excel formula adding back negative line items.
Excel finance format: hardcoded = BLUE font, formulas = BLACK.

## 🔒 Hard constraints (client banking data — non-negotiable)
- **Everything runs locally. Nothing is ever uploaded.** No cloud parsers (this is
  why we use local `PyMuPDF`, NOT MinerU — MinerU uploads to its cloud).
- **Never move/delete the colleague's statement PDFs.** Originals stay in `inbox/`.
  De-duplication is by content hash in `processed_index.json`, not by moving files.
- Builds on Mac, **runs on Windows**. Keep all code cross-platform (use `pathlib`,
  no hard-coded `/` or `\` paths). The `.bat` files are the Windows entry points.

## Layout (what each piece does)
- `config.py` — ALL paths + the fee setting (`MGMT_FEE_RATE`). One place to tweak.
- `watcher.py` — auto-trigger: watches the 3 inboxes, processes new PDFs.
- `run_all_once.py` — manual one-shot processing.
- Launchers: `*.command` (Mac) + `*.bat` (Windows): setup / run_watcher / run_once.
- `banks/<LGT|BoS|UBS>/parser.py` — the **3 distinct per-bank parsers** (real logic).
- `shared/extract.py` — line grouping + number parsing (commas AND space thousands).
- `shared/fees.py` — LGT Gross-from-add-backs ("fee formula").
- `shared/excel_writer.py` — master workbook; blue=hardcoded, black=formula; upsert by filename.
- `shared/docx_writer.py` — per-bank verification `.docx` (values + add-backs + snapshots).
- `shared/snapshot.py` — renders a PDF section to PNG. `shared/process.py` — the glue.
- `output/fees_master.xlsx` — generated. `logs/` — run log + snapshot PNGs.
- `docs/STATEMENT_SPEC_TEMPLATE.md` — how colleague specifies layouts w/o sharing data.
- `docs/FOR_COLLEAGUE_AI.md` — prompt for her AI to fill Account No (column A).

## Open (see docs/STATUS.md)
- Validate against real/dummy PDFs (multi-portfolio, multi-page, BoS non-zero liabilities).
- Account No is blank (column A) → filled by colleague's AI for now.
- Confirm colleague's OS (Mac vs Windows) — both supported.

## Run (dev)
`python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
then `python run_all_once.py` (after a PDF is in an inbox).
