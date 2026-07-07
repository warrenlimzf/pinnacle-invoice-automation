# Bank NAV automation (LGT · Bank of Singapore · UBS)

Drop a private-bank client-statement **PDF** into that bank's inbox folder. The tool
reads **Statement Date, Account No, Currency, Gross NAV, Net NAV and Liquidity** off
the statement, writes them into one Excel workbook (one tab per bank, one row per
statement), and saves a **screenshot of the exact spot on the PDF** each number came
from into a Word document — so you check the numbers by eyeballing, not re-typing.

**Privacy: everything runs on your own computer. Nothing is ever uploaded anywhere.**
The PDF reading, the OCR, the Excel writing — all of it is local. No account, no
internet login, no cloud service touches the statements. (That is also why no real
statement or output file is ever committed to this repository.)

Documentation map:
- **This README** — setup, daily use, how it works, and every known problem + fix.
- **[docs/RULEBOOK.md](docs/RULEBOOK.md)** — the full plain-English playbook (same
  content as here, in more depth, including the mechanism explained for non-programmers).
- **[HANDOFF.md](HANDOFF.md)** — the day-to-day operator crib sheet (what to copy where).
- **[docs/FOR_COLLEAGUE_AI.md](docs/FOR_COLLEAGUE_AI.md)** — **if you are an AI assistant**
  (Claude / Gemini / ChatGPT / Copilot) opened inside this folder, start THERE. It says
  what to read, where the handoff is, and lists every issue already debugged.
- **[docs/STATUS.md](docs/STATUS.md)** — project state and the debug journal.

---

## Setup & use (Windows)

### Step 1 — install Python *(ONE time ever — skip this forever after)*
Download **Python 3.12** — the "Windows installer (64-bit)" from
<https://www.python.org/downloads/release/python-3120/> — and run it.
On the very first screen, **tick "Add python.exe to PATH"** before clicking Install.
That box matters; don't skip it.

Python and everything else this tool uses is **free, open-source software. There is
nothing to buy.** Version 3.12 specifically, because the offline OCR add-on bundled in
`vendor/` was built for it.

> Already installed Python once? Then every future update starts from **Step 2**.

### Step 2 — download the latest tool *(repeat this whenever there's an update)*
1. Open <https://github.com/warrenlimzf/pinnacle-invoice-automation> (no account needed).
2. Click the green **Code** button → **Download ZIP**.
3. Right-click the ZIP → **Extract All**. Put the folder somewhere easy (e.g. Documents).
4. If you had an older copy: **copy your statement PDFs** from the old folder's
   `banks\<bank>\inbox\` folders into the new folder's same inbox folders, then the old
   folder is yours to keep or bin. (Your PDFs are the only thing worth carrying over —
   the tool rebuilds the Excel/Word outputs from them.)

### Step 3 — run setup *(once per downloaded copy)*
Double-click **`setup.bat`**. It installs the bundled libraries **offline** from the
`vendor/` folder (no internet needed) and asks about the **OCR add-on — answer Y**:
some banks (LGT especially) send statements as scanned images, and without OCR those
can't be read. When it says setup is complete, close the window.

### Step 4 — daily use
- **Automatic (recommended):** double-click **`run_watcher.bat`** and leave the window
  open. Drop each bank's PDF into its inbox folder:
  `banks\LGT\inbox\` · `banks\BoS\inbox\` · `banks\UBS\inbox\`
  Each file is processed the moment it lands.
- **On demand:** put the PDFs in the inboxes first, then double-click **`run_once.bat`**.

**⏳ Important — scanned statements are SLOW, not stuck.** Statements with a text layer
(BoS) finish in under a second. Statements that are scanned images (typically LGT) are
read page-by-page with local OCR at roughly **10 seconds per page — a 20-page statement
takes 3–4 minutes**, and the window prints progress lines the whole way. **Leave the
window open until it says done.** Closing it mid-read is exactly how rows go missing.
This cost is paid **once per file, ever**: processed files are remembered (by content),
so the next run skips them instantly.

### Step 5 — check, then copy into the master file
1. Open `output\nav_master.xlsx` (one tab per bank) next to that bank's Word file
   (`banks\<bank>\<bank>_verification.docx`, which holds the screenshots).
2. Glance that each row's numbers match its screenshot. **Blue** numbers were read
   straight off the PDF; **black** cells are live formulas the tool built (e.g. LGT's
   Gross NAV = Net NAV with the negative line items added back — each add-back cell is
   tagged with its name).
3. Copy the **A:F block** (Statement Date | Account No | Currency | Gross NAV | Net NAV
   | Liquidity) into your own master file, pasting **as values** (Paste Special →
   Values), so the formulas become plain numbers.

The Excel/Word here are a **draft / staging area**, never the final deliverable.
Your original PDFs are **never moved, renamed or deleted**.

---

## How it actually works (the mechanism)

**Two kinds of PDF, two reading paths.** A normal PDF stores its text as data — the
file literally says which characters sit where — and the tool copies that out in
microseconds (every BoS statement). A *scanned* PDF stores each page as one photograph:
millions of pixels and no text anywhere. For those pages only, the tool falls back to
**OCR (optical character recognition)**: it renders the page to a high-resolution image
and a small local AI model recognises the character shapes — "these pixels say
1,234,567.89, at this position." That recognition is heavy image processing, hence
~10 seconds per page, but printed bank statements are OCR's easiest input, so the
figures come out exact. The OCR engine (RapidOCR) is bundled and runs entirely on your
PC — nothing is sent anywhere.

**Finding the numbers.** Each bank has its own parser, keyed to that bank's real layout:
- **UBS** — statements can bundle several portfolios; the portfolio number's suffix
  (e.g. `…-03`) selects the right "Portfolio 03" table, and Gross / Net / Liquidity are
  read from its **Market value** column. The header's whole-relationship totals are
  deliberately ignored when a portfolio table exists.
- **BoS** — Gross = "Investment Assets", Net = "Total Net Asset Value". Negatives print
  in parentheses; an overdrawn account can genuinely have a negative Net. Overdrafts are
  captured with an audit formula (Gross + Liabilities − Net = 0) in the Check column.
- **LGT** — the statement shows only the Net NAV ("Total"). The tool collects the
  negative line items (Credit, Derivatives, …) and writes Gross NAV as a **live Excel
  formula** adding them back, so the derivation is auditable cell by cell.

**Nothing is guessed, and nothing fails silently.** If a figure's label can't be found,
the cell stays blank and the **Flags** column says so. If a whole PDF can't be read, the
tool writes a row whose flag starts with **FAILED** and states the exact reason and fix
— a bank tab can never be silently empty. Failed files are retried automatically on the
next run. Every number that *is* written has a screenshot proving where it came from.

**File memory.** Each processed PDF is remembered by its content (a hash), not its
name — old files are never re-processed, nothing duplicates, and re-dropping a file
after deleting its row rebuilds exactly that row.

---

## Troubleshooting — every problem seen so far, and the fix

| What you see | What it means | What to do |
|---|---|---|
| Lines like *"page N … had no text layer — read it with local OCR instead"* | **Not an error.** That statement is a scan; OCR is reading it at ~10s/page. | Wait. Leave the window open until "done". |
| A bank tab in the Excel is empty | The window was closed mid-OCR (scans take minutes), so those files never finished. | Run again and let it finish. Current versions also print a "NOT stuck — leave the window open" notice. |
| A row's flag starts with **FAILED — the PDF is password-protected** | Bank portals often lock PDFs with a password; a locked PDF can't be read by any tool. | Open the PDF with its password, **print/save it as a new PDF** (this removes the lock), drop the unlocked copy in. |
| A row's flag says the PDF is **a scanned image and the OCR add-on isn't installed** | Setup was run without the OCR add-on, or on a Python other than 3.12. | Re-run `setup.bat` and answer **Y** to OCR (install Python 3.12 first if needed). Then just run again — failed files retry automatically. |
| *"Permission"* / *"file is open"* message | Excel or Word has the output file open, so Windows blocks writing. | Close the file, drop the PDF in again (or re-run). |
| A blank cell + a note in Flags | That figure's label wasn't found on the page — the tool never guesses. | Check the statement; if the bank truly changed its wording, the parser needs a small update. |

Full run log: `logs\automation.log` — every action and error is recorded there.

---

## For developers / AI assistants

- Start at **[docs/FOR_COLLEAGUE_AI.md](docs/FOR_COLLEAGUE_AI.md)** (reading order, hard
  rules, and the debug journal of solved issues).
- Code layout: `banks/<bank>/parser.py` (per-bank logic), `shared/` (reader, OCR
  fallback, Excel/Word writers), `config.py` (all paths/settings), `watcher.py` +
  `run_all_once.py` (entry points).
- Tests: `python tests/test_failure_modes.py` runs anywhere (synthetic PDFs);
  `python tests/validate_samples.py` checks all real samples to the cent but needs the
  local, **never-committed** `samples/` folder.
- Hard rules: everything stays local (no cloud parsers), originals are never
  moved/deleted, and no client data is ever committed — `samples/`, inbox PDFs and
  outputs are gitignored.
