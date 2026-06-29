# Bank NAV automation — how to use it

Drop a bank's client-statement **PDF** into that bank's folder. The tool reads the
**Gross NAV** and **Net NAV**, writes them into an Excel spreadsheet, and saves a
**screenshot** of the exact spot on the PDF it read them from into a Word document.
You open the Excel and the Word doc side by side and check they match.

**Your client files never leave the computer.** Nothing is uploaded to the internet.

Works on **Mac** (`.command` files) and **Windows** (`.bat` files) — use whichever
matches the computer it runs on.

---

## One-time setup
1. **Install Python 3** if needed: https://www.python.org/downloads/
   - On **Windows**, tick **"Add python.exe to PATH"** on the first install screen.
2. Run setup once:
   - **Mac:** double-click **`setup.command`** (first time: right-click → Open → Open).
   - **Windows:** double-click **`setup.bat`**.
   This installs the software libraries (needs internet once — for the libraries only,
   never your client files).

## Everyday use — two options

### A. Automatic (recommended)
1. Start the watcher:
   - **Mac:** double-click **`run_watcher.command`**
   - **Windows:** double-click **`run_watcher.bat`**
   Leave the window open.
2. Drop a statement PDF into the right folder:
   - LGT → `banks/LGT/inbox/`
   - Bank of Singapore → `banks/BoS/inbox/`
   - UBS → `banks/UBS/inbox/`
3. It processes the file within a second or two. Watch the window for "done".
4. Close the window when finished.

### B. On demand
Put PDFs in the inbox folders, then run **`run_once.command`** (Mac) / **`run_once.bat`**
(Windows). It processes everything waiting, then stops.

---

## Do I need to delete old files first? — No.
Leave whatever's already in the folders. The tool remembers what it has already done
(by the file's content), so **old files are never re-processed and nothing is duplicated**.
Just copy the **new** PDF in; only that new file gets processed. Your original PDFs are
**never moved or deleted**.

## Where the results are
- **Excel:** `output/fees_master.xlsx` — one tab per bank, one row per statement.
  - Numbers read off the PDF are **blue** (hardcoded). Calculated cells are **black**
    (formulas) — e.g. LGT's Gross NAV = Net NAV with the negative line items added back.
- **Word (to eyeball):** `banks/<bank>/<bank>_verification.docx` — the screenshots.

> If you see a "permission"/"file is open" message: close the Excel or Word file, then
> drop the PDF again. Windows/Mac won't let the tool write while you have it open.

## What each bank does
- **UBS / BoS:** Gross NAV and Net NAV are read straight off the statement.
- **LGT:** the statement shows only the Net NAV (the "Total"). The tool finds the negative
  line items (e.g. Credit, Derivatives) and writes a **formula** that adds them back to
  give the Gross NAV, so you can audit it. Each add-back cell is tagged with its name.

## Filling Account Numbers
Column A (Account No) is left blank for you to fill with your own AI — see
`docs/FOR_COLLEAGUE_AI.md`.

## Make it auto-start when you log in (optional)
- **Mac:** System Settings → General → Login Items → add `run_watcher.command`.
- **Windows:** press `Win+R`, type `shell:startup`, Enter; paste a **shortcut** to
  `run_watcher.bat` there.

## If something looks wrong
Check the log at `logs/automation.log`, and the **Flags** column in the Excel (it notes
when a figure couldn't be found).
