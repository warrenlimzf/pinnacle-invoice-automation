# STATUS

## Done (scaffold, runs end-to-end)
- Folder structure: 3 banks (LGT, BoS, UBS), each with `inbox/` + its own `parser.py`.
- Folder-watch trigger (`watcher.py`) + manual run (`run_all_once.py`) + Windows `.bat`s.
- Pipeline: PDF → extract Gross/Net NAV → master Excel (3 tabs) → section screenshot → per-bank `.docx`.
- Screenshots are local via PyMuPDF (NOT MinerU — MinerU uploads to cloud; data must stay local).
- File-safety: originals never moved/deleted; de-dupe by content hash (`processed_index.json`).

## Open — needs ONE real (or redacted) sample PDF per bank
1. **Label wording** — confirm how each bank prints "Gross NAV" / "Net NAV";
   update `GROSS_LABELS` / `NET_LABELS` in each `banks/*/parser.py`.
2. **Client name** — confirm where the client is identified on the statement;
   update `_extract_client()` (currently falls back to the file name).
3. **Fee rule** — define with the colleague; set in `shared/fees.py` + `config.MGMT_FEE_RATE`.
4. **Multiple clients per PDF?** — current parsers assume one client per PDF. If a
   statement covers many clients, `parse()` should return several `ClientResult`s.

## Deferred (placeholders left in)
- Email ingestion / other file formats — add a new reader in `shared/readers/`.
