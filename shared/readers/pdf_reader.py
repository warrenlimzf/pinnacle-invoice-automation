"""PDF reader, backed by PyMuPDF (the `fitz` module). Fully offline.

PyMuPDF gives us each word's text AND its exact rectangle on the page. We need
the rectangle so we can later screenshot the precise section a number came from.
"""
from typing import Dict, List

import fitz  # PyMuPDF

from .base import StatementReader


class PdfReader(StatementReader):
    def extract_text_items(self, path) -> List[Dict]:
        items: List[Dict] = []
        doc = fitz.open(str(path))
        try:
            for page_no in range(len(doc)):
                page = doc[page_no]
                # get_text("words") -> list of (x0, y0, x1, y1, "word", block, line, word_no)
                for w in page.get_text("words"):
                    items.append({
                        "text": w[4],
                        "page": page_no,
                        "x0": w[0], "y0": w[1], "x1": w[2], "y1": w[3],
                    })
        finally:
            doc.close()
        return items

    def full_text(self, path) -> str:
        doc = fitz.open(str(path))
        try:
            return "\n".join(page.get_text() for page in doc)
        finally:
            doc.close()
