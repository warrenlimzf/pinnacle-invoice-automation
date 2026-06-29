"""Owns the master workbook (output/fees_master.xlsx) — one tab per bank.

Finance convention (as requested):
  - HARDCODED values (read straight off the PDF) are BLUE
  - FORMULA cells (e.g. LGT's reconstructed Gross NAV) are BLACK

Each row = one statement PDF. Re-processing the same file UPDATES its row.
The Account No column is left blank for the colleague's own AI to fill in.
"""
from datetime import datetime
from pathlib import Path
from typing import List

from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from shared.model import ClientResult

# Column layout (1-based)
COL_ACCOUNT = 1   # A
COL_GROSS = 2     # B
COL_NET = 3       # C
COL_SOURCE = 4    # D
COL_PAGE = 5      # E
COL_UPDATED = 6   # F
COL_FLAGS = 7     # G
ADDBACK_START = 9         # I onwards (LGT add-back line items)
ADDBACK_CLEAR_TO = 24     # clear up to col X when updating a row

HEADERS = ["Account No", "Gross NAV", "Net NAV", "Source PDF", "Page",
           "Updated At", "Flags"]

NUM_FMT = "#,##0.00"
BLUE = Font(color="FF0000FF")      # hardcoded inputs
BLACK = Font(color="FF000000")     # formulas / computed
BOLD = Font(bold=True)


def _ensure_workbook(path: Path, banks: List[str]) -> Workbook:
    if path.exists():
        wb = load_workbook(path)
    else:
        wb = Workbook()
        wb.remove(wb.active)
    for bank in banks:
        if bank not in wb.sheetnames:
            ws = wb.create_sheet(title=bank)
            for c, head in enumerate(HEADERS, start=1):
                cell = ws.cell(row=1, column=c, value=head)
                cell.font = BOLD
            if bank == "LGT":
                note = ws.cell(row=1, column=ADDBACK_START,
                               value="LGT add-back line items (negative figures) — "
                                     "Gross NAV = Net NAV minus these →")
                note.font = BOLD
    return wb


def _find_row(ws, source_name: str):
    for r in range(2, ws.max_row + 1):
        if str(ws.cell(row=r, column=COL_SOURCE).value or "").strip() == source_name:
            return r
    return None


def write_result(path, bank: str, banks: List[str],
                 result: ClientResult, page) -> None:
    """Insert/update one statement's row. Raises PermissionError if the workbook
    is open in Excel (Windows locks it) — caller logs and retries later."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = _ensure_workbook(path, banks)
    ws = wb[bank]

    source_name = Path(result.source_pdf).name
    r = _find_row(ws, source_name) or (ws.max_row + 1)

    # Account No — only set if we have it; never overwrite a value she/AI filled.
    if result.account_no:
        ws.cell(row=r, column=COL_ACCOUNT, value=result.account_no).font = BLUE

    # Net NAV — always hardcoded blue.
    if result.net_nav is not None:
        c = ws.cell(row=r, column=COL_NET, value=result.net_nav)
        c.font, c.number_format = BLUE, NUM_FMT

    # clear any stale add-back cells from a previous run of this row
    for col in range(ADDBACK_START, ADDBACK_CLEAR_TO + 1):
        cell = ws.cell(row=r, column=col)
        cell.value, cell.comment = None, None

    if result.gross_is_formula:
        # LGT: write each add-back (blue, with its label as a comment), then a
        # live formula for Gross = Net - SUM(add-backs).
        last_col = None
        for i, ab in enumerate(result.addbacks):
            col = ADDBACK_START + i
            cell = ws.cell(row=r, column=col, value=ab.value)
            cell.font, cell.number_format = BLUE, NUM_FMT
            cell.comment = Comment(f"{ab.label}", "automation")
            last_col = col
        net_ref = f"{get_column_letter(COL_NET)}{r}"
        if last_col:
            rng = f"{get_column_letter(ADDBACK_START)}{r}:{get_column_letter(last_col)}{r}"
            formula = f"={net_ref}-SUM({rng})"
        else:
            formula = f"={net_ref}"   # no negatives -> Gross = Net
        g = ws.cell(row=r, column=COL_GROSS, value=formula)
        g.font, g.number_format = BLACK, NUM_FMT
    else:
        # UBS / BoS: Gross is read straight off the PDF -> hardcoded blue.
        if result.gross_nav is not None:
            c = ws.cell(row=r, column=COL_GROSS, value=result.gross_nav)
            c.font, c.number_format = BLUE, NUM_FMT

    ws.cell(row=r, column=COL_SOURCE, value=source_name)
    ws.cell(row=r, column=COL_PAGE, value=page)
    ws.cell(row=r, column=COL_UPDATED,
            value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ws.cell(row=r, column=COL_FLAGS, value="; ".join(result.flags))

    wb.save(path)
