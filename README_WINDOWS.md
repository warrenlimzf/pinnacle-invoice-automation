# How to use this on the Windows PC

A plain-English guide. No coding needed once it's set up.

## What it does
You drop a bank's client-statement PDF into that bank's folder. The tool reads the
**Gross NAV** and **Net NAV**, puts them into an Excel spreadsheet, and saves a
**screenshot** of the exact spot on the PDF where it got each number into a Word
document. You then open the Excel and the Word doc side by side and check they match.

**Your client files never leave this computer.** Nothing is uploaded to the internet.

---

## One-time setup (do this once)

1. **Install Python** (if it isn't already): go to https://www.python.org/downloads/,
   download, run the installer, and on the FIRST screen tick **"Add python.exe to PATH"**,
   then click Install.
2. Double-click **`setup.bat`** in this folder. A black window opens, installs what's
   needed, and says "Setup complete." (This step needs internet ONCE — only to fetch the
   software libraries, never your client files.) Close the window.

---

## Everyday use

You have two ways to run it. Pick whichever suits you.

### Option A — Automatic (recommended)
1. Double-click **`run_watcher.bat`**. A window opens and says it's watching. **Leave it open.**
2. Drop a statement PDF into the right bank folder:
   - LGT statements → `banks\LGT\inbox\`
   - Bank of Singapore → `banks\BoS\inbox\`
   - UBS → `banks\UBS\inbox\`
3. Within a second or two it processes the file automatically. Watch the window for
   "done". Repeat for as many files as you like.
4. Done for the day? Just close the window.

### Option B — On demand
1. Put your PDFs into the inbox folders above.
2. Double-click **`run_once.bat`**. It processes everything sitting in the inboxes, then stops.

---

## Where your results are

- **Excel:** `output\fees_master.xlsx` — one tab per bank (LGT / BoS / UBS), one row per client.
- **Word (for eyeballing):** inside each bank folder, e.g. `banks\LGT\LGT_verification.docx` —
  shows the screenshot of where each number was read from.

Open the Excel and the matching Word doc side by side to verify.

> **Tip:** If you see a message about the file being "open" / "permission" — close the Excel
> or Word file first, then drop the PDF again (or re-run). Windows won't let the tool write
> while you have the file open.

---

## Make it start automatically when you log in (optional)
So the watcher is always running without double-clicking:
1. Press `Windows + R`, type `shell:startup`, press Enter. A folder opens.
2. Right-click `run_watcher.bat` (in this project folder) → **Copy**.
3. In the Startup folder, right-click → **Paste shortcut**.
Now the watcher starts every time you log in.

---

## Notes
- Your original PDFs are **never moved or deleted** — they stay where you put them.
- Dropping the same file twice is fine; it's skipped the second time. A corrected file
  (different content) is processed again.
- If something looks wrong, the log is at `logs\automation.log`.
- **Not finished yet:** the exact way each bank labels "Gross NAV"/"Net NAV" and the fee
  formula still need to be tuned using a real sample statement from each bank. Until then
  the numbers are best-effort. Send a sample of each and it gets locked in.
