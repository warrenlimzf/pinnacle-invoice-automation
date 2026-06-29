"""UBS statement parser.

Layout (from the sample): a top summary block with two lines
    Total gross assets as of <date>      SGD 7 032 282
    Total net assets   as of <date>      SGD 5 139 637
Numbers use SPACES as thousand separators, prefixed with the currency code.
Both Gross and Net NAV are read directly.
"""
from pathlib import Path
from typing import List

from shared.extract import (amount_after_currency, find_line_text_contains,
                            group_lines)
from shared.model import ClientResult, FieldHit
from shared.readers.pdf_reader import PdfReader


def parse(pdf_path) -> List[ClientResult]:
    lines = group_lines(PdfReader().extract_text_items(pdf_path))
    res = ClientResult(source_pdf=str(pdf_path))

    gross_line = find_line_text_contains(lines, "total gross assets")
    net_line = find_line_text_contains(lines, "total net assets")

    if gross_line:
        amt = amount_after_currency(gross_line)
        if amt:
            res.gross_nav, box = amt
            res.hits.append(FieldHit("Gross NAV", res.gross_nav, gross_line["page"],
                                     (gross_line["x0"], gross_line["y0"], box[2], box[3])))
    if net_line:
        amt = amount_after_currency(net_line)
        if amt:
            res.net_nav, box = amt
            res.hits.append(FieldHit("Net NAV", res.net_nav, net_line["page"],
                                     (net_line["x0"], net_line["y0"], box[2], box[3])))

    if res.gross_nav is None:
        res.flags.append("Gross NAV not found (check 'Total gross assets' wording)")
    if res.net_nav is None:
        res.flags.append("Net NAV not found (check 'Total net assets' wording)")
    return [res]
