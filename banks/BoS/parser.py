"""Bank of Singapore (BoS) statement parser.

Layout (from the sample):
    Assets                 10,208,537.88   100.00     <- Gross AUM (the 100.00% row)
    ...breakdown...
    Liabilities             0.00            0.00
    Total Net Asset Value  10,208,537.88              <- Net AUM (bottom)
When Liabilities are 0, Gross == Net. Otherwise the top 'Assets' row is Gross and
the bottom 'Total Net Asset Value' is Net.
"""
from typing import List

from shared.extract import (find_line_label_eq, find_line_text_contains,
                            first_amount, group_lines)
from shared.model import ClientResult, FieldHit
from shared.readers.pdf_reader import PdfReader


def parse(pdf_path) -> List[ClientResult]:
    lines = group_lines(PdfReader().extract_text_items(pdf_path))
    res = ClientResult(source_pdf=str(pdf_path))

    # Gross = the row whose label is exactly "Assets" (the 100.00% row).
    gross_line = find_line_label_eq(lines, "Assets")
    # Net = the "Total Net Asset Value" row.
    net_line = find_line_text_contains(lines, "total net asset value", "net asset value")

    if gross_line:
        amt = first_amount(gross_line)       # first number = value (second = the %)
        if amt:
            res.gross_nav, box = amt
            res.hits.append(FieldHit("Gross NAV (Assets)", res.gross_nav,
                                     gross_line["page"],
                                     (gross_line["x0"], gross_line["y0"], box[2], box[3])))
    if net_line:
        amt = first_amount(net_line)
        if amt:
            res.net_nav, box = amt
            res.hits.append(FieldHit("Net NAV (Total Net Asset Value)", res.net_nav,
                                     net_line["page"],
                                     (net_line["x0"], net_line["y0"], box[2], box[3])))

    if res.gross_nav is None:
        res.flags.append("Gross NAV not found (expected an 'Assets' row)")
    if res.net_nav is None:
        res.flags.append("Net NAV not found (expected 'Total Net Asset Value')")
    return [res]
