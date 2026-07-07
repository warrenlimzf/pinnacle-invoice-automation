# ⚠️ SUPERSEDED — the tool now fills Account No itself

> As of 2026-07-07 the automation reads the account number, currency and statement
> date straight off each statement's header (LGT "Client number", BoS "Portfolio No.",
> UBS "Portfolio number"). Column B fills automatically and this AI step is no longer
> needed. Kept only for reference.

# Filling in the Account Numbers (for your colleague + her AI)

The automation fills **Gross NAV** and **Net NAV** automatically. The **Account No**
column (column A) is left blank on purpose, for you to fill using your own AI
(ChatGPT / Gemini / Copilot) **on your own computer**, so the account numbers never
have to leave your machine.

## What you have
- `output/nav_master.xlsx` — one tab per bank (LGT / BoS / UBS). Each **row** is one
  statement, identified by the file name in the **Source PDF** column (D).
- The original statement PDFs, still sitting in each `banks/<bank>/inbox/` folder.

## The goal
A finished **3-column table** per bank tab: **Account Number | Gross NAV | Net NAV**.
Gross/Net are already filled. You only need to add the **Account Number** in column A.
(This Excel is a draft — once column A is filled, she copies the A:C block, **Paste Special
→ Values**, into her master file. See `HANDOFF.md`.)

## The job
For each row, read the account number off the matching PDF (the one named in column D)
and type it into **column A (Account No)** of that same row.

## Copy-paste prompt for your AI
> I have a spreadsheet `nav_master.xlsx` with tabs LGT, BoS and UBS. Each row has a
> "Source PDF" filename in column D and an empty "Account No" in column A. For each row,
> open the matching PDF in the folder `banks/<TAB NAME>/inbox/`, find the client's
> **account number** (it appears in the statement header / account-details section), and
> write it into column A of that row. Do not change any other cells. The Gross NAV / Net
> NAV columns are already filled — leave them, and leave the blue/black font formatting
> as-is. List any PDF where you can't find an account number so I can check it manually.

## Tips
- Keep the **font formatting**: hardcoded values are **blue**, formulas are **black**.
  Account numbers you type are hardcoded inputs, so make them **blue** too if you can.
- Do this **after** the automation has run (so the rows exist).
- If you tell me exactly where the account number sits on each bank's statement (see
  `STATEMENT_SPEC_TEMPLATE.md`, question 6), I can make the Python read it automatically
  and you won't need this AI step at all.
