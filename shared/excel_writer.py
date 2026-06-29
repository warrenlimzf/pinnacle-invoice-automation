"""Owns the master workbook (output/fees_master.xlsx) with one tab per bank.

Each row is one client. Re-processing the same client UPDATES that client's row
rather than adding a duplicate (matched on the Client name).
"""
from datetime import datetime
from pathlib import Path
from typing import List

from openpyxl import Workbook, load_workbook

HEADERS = ["Client", "Gross NAV", "Net NAV", "Fee", "Source PDF", "Page", "Updated At"]


def _ensure_workbook(path: Path, banks: List[str]) -> Workbook:
    if path.exists():
        wb = load_workbook(path)
    else:
        wb = Workbook()
        wb.remove(wb.active)  # drop the default empty sheet
    for bank in banks:
        if bank not in wb.sheetnames:
            ws = wb.create_sheet(title=bank)
            ws.append(HEADERS)
    return wb


def write_record(path, bank: str, banks: List[str], record: dict) -> None:
    """Insert or update one client row in the given bank's tab.

    Raises PermissionError if the workbook is currently open in Excel (Windows
    locks the file). The caller logs this clearly and the file is retried later.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = _ensure_workbook(path, banks)
    ws = wb[bank]

    new_row = [
        record.get("client"),
        record.get("gross_nav"),
        record.get("net_nav"),
        record.get("fee"),
        record.get("source_pdf"),
        record.get("page"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ]

    client_key = str(record.get("client", "")).strip().lower()
    found_row = None
    for r in range(2, ws.max_row + 1):
        existing = ws.cell(row=r, column=1).value
        if existing is not None and str(existing).strip().lower() == client_key:
            found_row = r
            break

    if found_row:
        for col, value in enumerate(new_row, start=1):
            ws.cell(row=found_row, column=col, value=value)
    else:
        ws.append(new_row)

    wb.save(path)
