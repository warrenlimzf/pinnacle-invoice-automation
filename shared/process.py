"""The glue: process ONE statement PDF end-to-end for a given bank.

  parse -> write to Excel tab -> screenshot each value's section -> paste into docx

This is what both the watcher and the manual 'run once' script call.
"""
import importlib
from pathlib import Path
from typing import List

import config
from shared.docx_writer import append_verification
from shared.excel_writer import write_record
from shared.logging_setup import get_logger
from shared.model import ClientResult
from shared.snapshot import snapshot_region

log = get_logger("process")


def _bank_parser(bank: str):
    """Load banks/<bank>/parser.py (the 3 distinct per-bank scripts)."""
    return importlib.import_module(f"banks.{bank}.parser")


def process_pdf(bank: str, pdf_path) -> List[ClientResult]:
    pdf_path = Path(pdf_path)
    parser = _bank_parser(bank)
    results: List[ClientResult] = parser.parse(pdf_path)

    snap_dir = config.SNAPSHOT_DIR / bank

    for res in results:
        # 1) screenshots of each section a value came from
        images = []
        for hit in res.hits:
            safe_client = "".join(c if c.isalnum() else "_" for c in res.client)[:40]
            safe_label = hit.label.replace(" ", "")
            png = snap_dir / f"{pdf_path.stem}__{safe_client}__{safe_label}.png"
            try:
                snapshot_region(pdf_path, hit.page, hit.bbox, png)
                images.append((hit, png))
            except Exception:
                log.exception(f"[{bank}] could not screenshot {hit.label} for {res.client}")

        # 2) Excel row (insert/update)
        write_record(config.MASTER_WORKBOOK, bank, config.BANKS, {
            "client": res.client,
            "gross_nav": res.gross_nav,
            "net_nav": res.net_nav,
            "fee": res.fee,
            "source_pdf": pdf_path.name,
            "page": (res.hits[0].page + 1) if res.hits else "",
        })

        # 3) verification docx for eyeballing
        append_verification(config.verification_docx(bank), res, images, pdf_path)

        log.info(f"[{bank}] {res.client}: gross={res.gross_nav} net={res.net_nav} "
                 f"fee={res.fee} ({len(images)} snapshot(s))")

    return results
