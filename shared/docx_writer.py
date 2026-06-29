"""Owns the per-bank verification Word doc (banks/<bank>/<bank>_verification.docx).

For each client it appends a heading, the values we read, and the screenshot(s)
of the exact PDF section those values came from. Your colleague opens this next
to the Excel and eyeballs that they match.
"""
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from docx import Document
from docx.shared import Inches, Pt, RGBColor

from shared.model import ClientResult, FieldHit


def append_verification(docx_path, result: ClientResult,
                        images: List[Tuple[FieldHit, Path]], pdf_path) -> None:
    """Append one client's verification block to the bank's docx.

    images: list of (FieldHit, png_path) — the screenshots to paste.
    """
    docx_path = Path(docx_path)
    pdf_path = Path(pdf_path)

    if docx_path.exists():
        doc = Document(str(docx_path))
    else:
        doc = Document()
        doc.add_heading("Verification snapshots", level=0)
        intro = doc.add_paragraph(
            "Each entry below shows the exact section of the source statement "
            "where Gross NAV and Net NAV were read. Compare against the Excel."
        )
        intro.runs[0].italic = True

    doc.add_heading(result.client, level=1)

    meta = doc.add_paragraph()
    meta.add_run("Source file: ").bold = True
    meta.add_run(pdf_path.name)
    meta.add_run(f"    |    Processed: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    vals = doc.add_paragraph()
    vals.add_run("Gross NAV: ").bold = True
    vals.add_run(f"{result.gross_nav}    ")
    vals.add_run("Net NAV: ").bold = True
    vals.add_run(f"{result.net_nav}")

    for hit, png in images:
        cap = doc.add_paragraph()
        run = cap.add_run(f"{hit.label}  (page {hit.page + 1})")
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        if png and Path(png).exists():
            doc.add_picture(str(png), width=Inches(6.0))

    doc.add_paragraph("")  # spacer between clients
    doc.save(str(docx_path))
