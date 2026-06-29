# STATUS

## Done & verified (against synthetic PDFs that replicate the 3 real sample layouts)
- 3 banks (LGT, BoS, UBS), each with `inbox/` + its own real `parser.py`.
- Folder-watch trigger (`watcher.py`) + manual run (`run_all_once.py`).
- Launchers for BOTH OSes: `*.command` (Mac) and `*.bat` (Windows).
- Pipeline: PDF → Gross/Net NAV → master Excel (3 tabs) → section screenshot → per-bank `.docx`.
- Local-only screenshots via PyMuPDF (NOT MinerU — MinerU uploads to cloud).
- File-safety: originals never moved/deleted; de-dupe by content hash.

## Extraction logic (real, not placeholder)
- **UBS** — reads "Total gross assets" / "Total net assets"; handles SPACE thousands + SGD prefix.
- **BoS** — Gross = the "Assets" (100%) row; Net = "Total Net Asset Value". Net=Gross when liabilities 0.
- **LGT** — Net = "Total"; finds negative line items; Gross = live Excel formula `=Net-SUM(addbacks)`.
- Finance formatting: hardcoded = BLUE, formulas = BLACK. Add-back cells tagged with line-item name.

## Open
1. **Validate against real layouts** — confirm via dummy/redacted PDFs or the colleague's
   answers in `docs/STATEMENT_SPEC_TEMPLATE.md` (esp. multi-portfolio PDFs, multi-page,
   exact label wording, BoS non-zero-liability case).
2. **Account No (column A)** — currently blank; filled by colleague's own AI via
   `docs/FOR_COLLEAGUE_AI.md`. Could be automated once we know where it sits on each statement.
3. **Multiple clients per PDF** — parsers currently assume one account per PDF.

## Deferred (placeholders left in)
- Email ingestion / more file formats — add a new reader in `shared/readers/`.

## Open question for Warren
- Which OS does the colleague actually run on — Mac or Windows? (Both are supported; this
  only changes which launcher + auto-start instructions to point her to.)
