# Email to colleague — ready to send

> Copy everything below the line into an email. The GitHub link is live and public,
> so she does not need a GitHub account or any login to download it.

---

**Subject: The bank NAV tool — how to set it up (about 10 minutes, one time)**

Hi [name],

Here is the little tool that reads the Gross NAV and Net NAV off the LGT, Bank of Singapore and UBS statements so you don't have to type them by hand. Everything runs on your own PC and nothing is ever uploaded anywhere, so the client files stay private.

It is a one-time setup, then daily use is just dropping the PDFs into folders and checking the numbers.

## One-time setup (do this once)

**1. Install Python 3.12.**
Go to https://www.python.org/downloads/release/python-3120/ and download the "Windows installer (64-bit)". Run it. On the very first screen, **tick the box that says "Add python.exe to PATH"** before you click Install. That box matters, so please don't skip it.

**2. Download the tool.**
Open this link: https://github.com/warrenlimzf/pinnacle-invoice-automation
Click the green **Code** button, then **Download ZIP**. Save it, then right-click the downloaded file and choose **Extract All** to unzip it. Put the unzipped folder somewhere easy like your Documents.

**3. Run the setup file.**
Open the folder. Double-click **`setup.bat`**. A black window opens and installs what it needs (this works without internet). When it says "Setup complete", press a key to close it. You only ever do this once.

## Daily use

**4. Start the tool.**
Double-click **`run_watcher.bat`**. A window opens and stays open. **Leave that window open** while you work, that is the tool running and watching for files. (To stop it later, just close that window.)

**5. Drop in the statements.**
Inside the folder there are three inbox folders. Drop each bank's PDF into its own one:
- `banks\LGT\inbox`
- `banks\BoS\inbox`
- `banks\UBS\inbox`

The moment a PDF lands, the tool reads it and fills in the numbers automatically. Your original PDFs are never moved or deleted.

**6. Check and copy.**
Open `output\nav_master.xlsx`. There is one tab per bank. Next to it, open the matching Word file (for example `banks\LGT\LGT_verification.docx`), which holds a screenshot of the exact spot on the PDF each number came from. Glance at them side by side to confirm the numbers match the screenshots. Then copy the first six columns (Statement Date, Account No, Currency, Gross NAV, Net NAV, Liquidity) into your own master file, pasting **as values** (Paste Special → Values). Everything, including the account number, is filled in automatically now.

## A few handy things

- **You only ever touch two files: `setup.bat` (once) and `run_watcher.bat` (each day).** You can ignore everything else in the folder, including the files ending in `.command` (those are for a Mac).
- **If you delete a row by mistake and want it back:** delete that bank's PDF from its inbox folder, then drop the same PDF back in. The tool will rebuild that row.
- **If the Excel or Word file is open when you drop a PDF,** the tool will tell you to close it. Just close the file and drop the PDF in again.
- **To stop the tool:** close the black window. To start it again the next day, double-click `run_watcher.bat`.

- **Blue vs black numbers in the Excel:** blue means the number was read straight off the PDF; black means it is a live formula the tool built (for example LGT's Gross NAV, which adds back the negative line items). When you paste into your master as values, both become plain numbers.

The tool has been checked against real statements from all three banks (including a UBS statement with several portfolios and a Bank of Singapore account with an overdraft) and every figure matched. Still, for your first few real statements please do glance at the screenshots — you are the final check.

Shout if anything is unclear and I'll walk you through it.

Thanks,
Warren
