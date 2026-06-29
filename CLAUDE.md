# Pinnacle Invoice / Fee Automation — router

Local-only tool: reads bank client-statement **PDFs**, pulls **Gross NAV + Net NAV**,
writes them to a master Excel (3 tabs), and screenshots the exact PDF section each
number came from into a per-bank Word doc for human eyeball verification.

## 🔒 Hard constraints (client banking data — non-negotiable)
- **Everything runs locally. Nothing is ever uploaded.** No cloud parsers (this is
  why we use local `PyMuPDF`, NOT MinerU — MinerU uploads to its cloud).
- **Never move/delete the colleague's statement PDFs.** Originals stay in `inbox/`.
  De-duplication is by content hash in `processed_index.json`, not by moving files.
- Builds on Mac, **runs on Windows**. Keep all code cross-platform (use `pathlib`,
  no hard-coded `/` or `\` paths). The `.bat` files are the Windows entry points.

## Layout (what each piece does)
- `config.py` — ALL paths + the fee setting (`MGMT_FEE_RATE`). One place to tweak.
- `watcher.py` — auto-trigger: watches the 3 inboxes, processes new PDFs. (`run_watcher.bat`)
- `run_all_once.py` — manual one-shot processing. (`run_once.bat`)
- `banks/<LGT|BoS|UBS>/parser.py` — the **3 distinct per-bank parsers**. PLACEHOLDERS.
- `banks/<bank>/inbox/` — where statement PDFs are dropped.
- `shared/readers/` — pluggable file-format layer (PDF today; add Excel/CSV later here).
- `shared/snapshot.py` — renders a PDF section to PNG (the screenshot).
- `shared/excel_writer.py` — master workbook, 3 tabs, upsert by client.
- `shared/docx_writer.py` — per-bank verification `.docx` (snapshots + values).
- `shared/process.py` — glue: parse → Excel → screenshot → docx.
- `output/fees_master.xlsx` — generated. `logs/` — run log + snapshot PNGs.

## ⚠️ Still PLACEHOLDER — needs a real sample PDF per bank to finish
1. **Label wording** in each `banks/*/parser.py` (`GROSS_LABELS` / `NET_LABELS`).
2. **Client-name extraction** (`_extract_client` — currently uses the file name).
3. **Fee rule** (`shared/fees.py` + `config.MGMT_FEE_RATE`).
See `docs/STATUS.md` for the current state and next steps.

## Run (dev, on Mac)
`python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
then `python run_all_once.py` (after a PDF is in an inbox).
