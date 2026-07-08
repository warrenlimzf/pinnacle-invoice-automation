"""Central configuration. Everything tweakable lives here, in ONE place.

Paths are all relative to this file, so the whole folder can be copied to the
Windows PC and it just works. Nothing here points outside this folder, and
nothing ever goes to the internet.
"""
from pathlib import Path

# Project root = the folder this file sits in.
ROOT = Path(__file__).resolve().parent

# The three banks. These names are used for folder names, Excel tab names,
# and the verification .docx file names. Keep them as the 3-letter codes.
BANKS = ["LGT", "BoS", "UBS"]


# --- Per-bank locations -----------------------------------------------------
def inbox_dir(bank: str) -> Path:
    """Folder where your colleague drops that bank's client statement PDFs."""
    return ROOT / "banks" / bank / "inbox"


def verification_docx(bank: str) -> Path:
    """The Word doc (one per bank) holding the screenshot snapshots to eyeball."""
    return ROOT / "banks" / bank / f"{bank}_verification.docx"


# --- Shared outputs ---------------------------------------------------------
OUTPUT_DIR = ROOT / "output"
MASTER_WORKBOOK = OUTPUT_DIR / "nav_master.xlsx"    # one workbook, 3 tabs
LOGS_DIR = ROOT / "logs"
SNAPSHOT_DIR = LOGS_DIR / "snapshots"               # PNG crops kept for reference
PROCESSED_INDEX = ROOT / "processed_index.json"     # files read AND written to the Excel
FAILED_INDEX = ROOT / "failed_index.json"           # files that could NOT be read yet (+ reason)
NEEDS_REUPLOAD_REPORT = OUTPUT_DIR / "NEEDS_REUPLOAD.txt"  # plain-English "what to remove & re-upload"


# --- Screenshot settings ----------------------------------------------------
# Higher DPI = sharper screenshot but bigger image. 200 is a good readable default.
SNAPSHOT_DPI = 200
# Padding (in PDF points, 72 = 1 inch) added around a found value so the
# screenshot shows surrounding context, not just the bare number.
SNAPSHOT_PADDING = 45


# --- FEE LOGIC (PLACEHOLDER) -----------------------------------------------
# We agreed to define the real rule once we look at a real statement together.
# Example only: a 1% management fee on net NAV would be MGMT_FEE_RATE = 0.01.
# Leave as None and the Fee column stays blank until we set the real rule.
MGMT_FEE_RATE = None
