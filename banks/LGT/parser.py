"""LGT statement parser — one of the 3 distinct per-bank scripts.

PLACEHOLDER. It already runs end-to-end (reads the PDF, finds candidate Gross/Net
NAV values, screenshots them, writes to Excel + docx). But the label wording and
client-name logic below are GUESSES and MUST be checked against a real LGT sample.

To finish this for LGT, once we have a sample PDF:
  1. Confirm exactly how "Gross NAV" / "Net NAV" are written -> update *_LABELS.
  2. Confirm how the client is identified -> update _extract_client().
  3. Confirm the fee rule -> shared/fees.py + config.MGMT_FEE_RATE.
"""
from pathlib import Path
from typing import List

from shared.extract import find_label_value
from shared.fees import calculate_fee
from shared.model import ClientResult, FieldHit
from shared.readers.pdf_reader import PdfReader

# TODO(LGT sample): adjust to LGT's exact wording.
GROSS_LABELS = ["gross nav", "gross net asset value", "gross asset value"]
NET_LABELS = ["net nav", "net asset value"]


def parse(pdf_path) -> List[ClientResult]:
    reader = PdfReader()
    items = reader.extract_text_items(pdf_path)

    client = _extract_client(pdf_path, reader)

    gross_v, gross_pg, gross_box = find_label_value(items, GROSS_LABELS)
    net_v, net_pg, net_box = find_label_value(items, NET_LABELS)

    result = ClientResult(client=client, gross_nav=gross_v, net_nav=net_v,
                          source_pdf=str(pdf_path))
    if gross_pg is not None:
        result.hits.append(FieldHit("Gross NAV", gross_v, gross_pg, gross_box))
    if net_pg is not None:
        result.hits.append(FieldHit("Net NAV", net_v, net_pg, net_box))

    result.fee = calculate_fee(result)
    return [result]


def _extract_client(pdf_path, reader) -> str:
    # TODO(LGT sample): replace with real client-name extraction from the PDF.
    # For now we use the file name so the pipeline produces visible output.
    return Path(pdf_path).stem
