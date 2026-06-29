"""Generic helpers the bank parsers share.

PLACEHOLDER HEURISTICS. `find_label_value` is a reasonable first guess: it looks
for a label like "Net NAV" on the page and grabs the nearest number to its right
on the same line. Once we have a real statement from each bank, we refine the
label wording (and, if needed, the geometry) in each bank's parser.
"""
import re
from typing import Dict, List, Optional, Tuple

# Matches numbers like 1,234,567.89  or  -1234.5  or  12,345
_NUM_RE = re.compile(r"^[-+(]?[\d,]*\.?\d+\)?$")


def to_float(token: str) -> Optional[float]:
    """Turn a statement number string into a float. Handles commas, and
    parentheses/CR meaning negative. Returns None if it isn't a number."""
    if token is None:
        return None
    s = token.strip()
    neg = s.startswith("(") and s.endswith(")")
    s = s.replace("(", "").replace(")", "").replace(",", "").replace("+", "").strip()
    try:
        val = float(s)
    except ValueError:
        return None
    return -val if neg else val


def find_label_value(
    items: List[Dict],
    label_variants: List[str],
    y_tol: float = 3.5,
) -> Tuple[Optional[float], Optional[int], Optional[Tuple[float, float, float, float]]]:
    """Find a label and return (value, page, bbox).

    - value: the number read just after the label (or None if no number found)
    - page:  0-based page index where the label is
    - bbox:  rectangle covering the label + the number, for screenshotting

    Returns (None, None, None) if the label isn't found at all.
    """
    variants = [v.lower() for v in label_variants]

    for variant in variants:
        parts = variant.split()
        n = len(parts)
        pages = sorted({it["page"] for it in items})

        for page in pages:
            page_items = [it for it in items if it["page"] == page]
            # reading order: top-to-bottom, then left-to-right
            page_items.sort(key=lambda it: (round(it["y0"], 1), it["x0"]))

            for i in range(len(page_items) - n + 1):
                window = page_items[i:i + n]
                words = [w["text"].lower().strip(":").strip() for w in window]
                if words != parts:
                    continue

                # label found — its bounding rectangle
                lx0 = min(w["x0"] for w in window)
                ly0 = min(w["y0"] for w in window)
                lx1 = max(w["x1"] for w in window)
                ly1 = max(w["y1"] for w in window)

                # look for a number to the RIGHT of the label, same line
                same_line = [
                    it for it in page_items
                    if it["x0"] >= lx1 - 1 and abs(it["y0"] - ly0) <= y_tol
                ]
                same_line.sort(key=lambda it: it["x0"])
                for cand in same_line:
                    if _NUM_RE.match(cand["text"].replace(",", "x").replace("x", ",")):
                        val = to_float(cand["text"])
                        if val is not None:
                            bbox = (
                                min(lx0, cand["x0"]), min(ly0, cand["y0"]),
                                max(lx1, cand["x1"]), max(ly1, cand["y1"]),
                            )
                            return val, page, bbox

                # label found but no number beside it — still return the label
                # region so the screenshot shows the area for a human to check.
                return None, page, (lx0, ly0, lx1, ly1)

    return None, None, None
