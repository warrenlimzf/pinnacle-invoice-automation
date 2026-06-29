"""LGT statement parser.

Layout (from the sample) — 'Statement of assets':
    Asset allocation/currency        Amount in USD
    Liquidity                          223,742.84
    Credit                          -1,109,240.85     <- negative line item
    Short-term investments              13,688.06
    Bonds                              949,128.55
    Equities                         2,010,656.06
    Hedge funds                        162,304.32
    Derivatives                        -35,864.31     <- negative line item
    Total                            2,214,414.67     <- this is NET NAV

LGT shows only the Net NAV (the Total). Gross NAV is reconstructed by adding back
the negative line items, written into Excel as a live formula (see shared/fees.py).
"""
from typing import List

from shared.extract import (amounts_in_line, find_line_label_eq, first_amount,
                            group_lines, line_label, union_bbox)
from shared.fees import gross_from_addbacks
from shared.model import AddBack, ClientResult, FieldHit
from shared.readers.pdf_reader import PdfReader

# Header that marks the top of the asset-allocation list.
_HEADER_HINTS = ("amount in", "asset allocation/currency")


def parse(pdf_path) -> List[ClientResult]:
    lines = group_lines(PdfReader().extract_text_items(pdf_path))
    res = ClientResult(source_pdf=str(pdf_path), gross_is_formula=True)

    total_line = find_line_label_eq(lines, "Total")
    if total_line:
        amt = first_amount(total_line)
        if amt:
            res.net_nav = amt[0]

    # The allocation rows live between the header and the Total line, same page.
    header_line = next(
        (ln for ln in lines if any(h in ln["text"].lower() for h in _HEADER_HINTS)),
        None,
    )
    if total_line and header_line:
        page = total_line["page"]
        top_y, bot_y = header_line["y1"], total_line["y0"]
        item_boxes = []
        for ln in lines:
            if ln["page"] != page or not (top_y < ln["y0"] < bot_y):
                continue
            amts = amounts_in_line(ln)
            if not amts:
                continue
            value, box = amts[0]
            item_boxes.append((ln["x0"], ln["y0"], box[2], box[3]))
            if value < 0:                       # a negative line item -> add it back
                res.addbacks.append(AddBack(label=line_label(ln) or "item", value=value))

        # Screenshot the WHOLE allocation table so she can eyeball all add-backs.
        table_box = union_bbox(
            (header_line["x0"], header_line["y0"], header_line["x1"], header_line["y1"]),
            (total_line["x0"], total_line["y0"], total_line["x1"], total_line["y1"]),
            *item_boxes,
        )
        res.hits.append(FieldHit("Net NAV (Total) & add-back items",
                                 res.net_nav, page, table_box))

    res.gross_nav = gross_from_addbacks(res.net_nav, res.addbacks)  # for docx display

    if res.net_nav is None:
        res.flags.append("Net NAV not found (expected a 'Total' row)")
    if not res.addbacks:
        res.flags.append("No negative line items found — Gross will equal Net")
    return [res]
