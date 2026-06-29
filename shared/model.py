"""Small data containers passed between the parser, Excel writer and docx writer.

Using typing.Optional (not the `X | None` syntax) so this runs on Python 3.9+
as well as newer versions, since the Windows PC's Python version may differ.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class FieldHit:
    """One extracted number plus exactly where it was found on the PDF, so we can
    screenshot that section for human verification."""
    label: str                       # e.g. "Gross NAV"
    value: Optional[float]           # the number we read (or None if not found)
    page: int                        # 0-based page index in the PDF
    bbox: Tuple[float, float, float, float]  # (x0, y0, x1, y1) region to screenshot


@dataclass
class ClientResult:
    """Everything we extracted for one client from one statement PDF."""
    client: str
    gross_nav: Optional[float] = None
    net_nav: Optional[float] = None
    fee: Optional[float] = None
    hits: List[FieldHit] = field(default_factory=list)  # for the screenshots
    source_pdf: str = ""
