"""Manual fallback: process every PDF currently in the inbox folders, once, then exit.

Use this when you'd rather run on demand than leave the watcher running, or to
re-run a batch. Already-processed files (same content) are skipped automatically.

  python run_all_once.py            # process all three banks
  python run_all_once.py LGT        # process only one bank
"""
import sys

import config
from shared.index import already_processed, mark_processed
from shared.logging_setup import get_logger
from shared.process import process_pdf

log = get_logger("run_all_once")


def main(argv):
    banks = [b for b in argv if b in config.BANKS] or config.BANKS
    total = 0
    for bank in banks:
        for pdf in sorted(config.inbox_dir(bank).glob("*.pdf")):
            if already_processed(pdf):
                log.info(f"[{bank}] skip (already processed): {pdf.name}")
                continue
            try:
                log.info(f"[{bank}] processing {pdf.name}")
                process_pdf(bank, pdf)
                mark_processed(pdf)
                total += 1
            except PermissionError:
                log.error(f"[{bank}] Close the Excel/Word file first, then re-run. ({pdf.name})")
            except Exception:
                log.exception(f"[{bank}] FAILED: {pdf.name}")
    log.info(f"Done. Processed {total} new file(s).")


if __name__ == "__main__":
    main(sys.argv[1:])
