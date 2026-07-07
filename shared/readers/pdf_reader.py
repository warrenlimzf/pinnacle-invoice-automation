"""PDF reader, backed by PyMuPDF (the `fitz` module). Fully offline.

PyMuPDF gives us each word's text AND its exact rectangle on the page. We need
the rectangle so we can later screenshot the precise section a number came from.

OCR fallback: some PDFs are just pictures of a statement (a scan, or a page
someone screenshotted and re-saved). Those have NO text layer, so PyMuPDF finds
no words. If the optional local OCR engine (RapidOCR) is installed, any page
with no text is rendered to an image and read locally — nothing is uploaded
anywhere. Without OCR installed, such pages are skipped with a clear log line.
"""
from typing import Dict, List, Optional

import fitz  # PyMuPDF

from shared.logging_setup import get_logger

from .base import StatementReader

log = get_logger("pdf_reader")


class PdfReadError(Exception):
    """The PDF could not be read at all. The message ends up in the Excel
    Flags column for the colleague to act on — keep it plain English."""

_OCR_DPI = 300  # render resolution for OCR; 300 reads bank tables reliably

_ocr_engine = None
_ocr_import_failed = False


def _get_ocr():
    """Lazily import RapidOCR (optional dependency). Returns None if unavailable."""
    global _ocr_engine, _ocr_import_failed
    if _ocr_engine is not None or _ocr_import_failed:
        return _ocr_engine
    try:
        from rapidocr_onnxruntime import RapidOCR
        _ocr_engine = RapidOCR()
    except Exception:
        _ocr_import_failed = True
        log.warning(
            "This PDF has no text layer (it's a scanned image) and the optional "
            "OCR engine isn't installed. Run setup again with internet, or "
            "re-download the original statement PDF from the bank portal."
        )
    return _ocr_engine


def _ocr_page_items(page, page_no: int) -> List[Dict]:
    """OCR one image-only page; return word items in PDF-point coordinates."""
    ocr = _get_ocr()
    if ocr is None:
        return []
    zoom = _OCR_DPI / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    result, _ = ocr(pix.tobytes("png"))
    items: List[Dict] = []
    if not result:
        return items
    scale = 1.0 / zoom  # image pixels -> PDF points
    for box, text, _score in result:
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        x0, x1 = min(xs) * scale, max(xs) * scale
        y0, y1 = min(ys) * scale, max(ys) * scale
        # OCR returns whole text regions ("Total gross assets as of 31.03.2026").
        # Downstream logic works on WORDS, so split each region into words and
        # give each a proportional slice of the region's box. Adjacent number
        # groups ("14", "870", "285") stay close enough to merge back later.
        words = text.split()
        if not words:
            continue
        total_chars = max(sum(len(w) for w in words) + (len(words) - 1), 1)
        cursor = x0
        width = x1 - x0
        char_w = width / total_chars
        for w in words:
            w_width = char_w * len(w)
            items.append({
                "text": w,
                "page": page_no,
                "x0": cursor, "y0": y0,
                "x1": cursor + w_width, "y1": y1,
            })
            cursor += w_width + char_w  # one space between words
    return items


def no_text_hint(info: Optional[Dict]) -> str:
    """A flag suffix explaining unreadable pages, for when a parser can't find
    its overview page. Empty string if every page was read fine."""
    pages = (info or {}).get("no_text_pages") or []
    if not pages:
        return ""
    pg = ", ".join(str(p) for p in pages)
    if _ocr_import_failed:
        return (f" — note: page {pg} of the PDF is a scanned image and the "
                "optional OCR engine isn't installed. Re-run setup and include "
                "OCR, or download a text-based copy of the statement.")
    return (f" — note: page {pg} of the PDF is a scanned image that OCR "
            "could not read. Try re-downloading the original statement.")


class PdfReader(StatementReader):
    def extract_text_items(self, path, info: Optional[Dict] = None) -> List[Dict]:
        """All words with their rectangles. `info`, if given, is filled with
        `no_text_pages`: 1-based pages that had no text layer AND could not be
        OCR'd — so parsers can explain a missing overview page."""
        if info is None:
            info = {}
        info["no_text_pages"] = []
        items: List[Dict] = []
        doc = fitz.open(str(path))
        try:
            if doc.needs_pass and not doc.authenticate(""):
                raise PdfReadError(
                    "the PDF is password-protected. Open it in a PDF viewer "
                    "(enter the password), print/save it as a new PDF, and "
                    "drop that unlocked copy into the inbox instead")
            for page_no in range(len(doc)):
                page = doc[page_no]
                # get_text("words") -> list of (x0, y0, x1, y1, "word", block, line, word_no)
                words = page.get_text("words")
                if words:
                    for w in words:
                        items.append({
                            "text": w[4],
                            "page": page_no,
                            "x0": w[0], "y0": w[1], "x1": w[2], "y1": w[3],
                        })
                    continue
                try:
                    ocr_items = _ocr_page_items(page, page_no)
                except Exception:
                    log.exception(f"OCR crashed on page {page_no + 1} of {path} — "
                                  "treating the page as unreadable")
                    ocr_items = []
                if ocr_items:
                    log.info(f"page {page_no + 1} of {path} had no text layer — "
                             f"read it with local OCR instead")
                    items.extend(ocr_items)
                else:
                    info["no_text_pages"].append(page_no + 1)
        finally:
            doc.close()
        if not items:
            if _ocr_import_failed:
                raise PdfReadError(
                    "the whole PDF is a scanned image and the optional OCR "
                    "engine isn't installed. Re-run setup and include OCR, or "
                    "download a text-based copy of the statement from the bank portal")
            raise PdfReadError(
                "no readable text found in this PDF — it looks like a scanned "
                "image that even OCR could not read. Try re-downloading the "
                "original statement from the bank portal")
        return items

    def full_text(self, path) -> str:
        doc = fitz.open(str(path))
        try:
            return "\n".join(page.get_text() for page in doc)
        finally:
            doc.close()
