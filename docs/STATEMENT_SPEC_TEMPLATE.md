# Statement spec — fill this in per bank (no client data needed)

This is how your colleague tells me what's in the PDFs **without me ever seeing a
real client statement**. She fills one block per bank, describing the *layout and
wording*, not the actual numbers/names. A redacted screenshot of just the figures
section (like the three she already sent) is the ideal companion to this.

For each bank answer these. "Same as sample" is a fine answer where the sample covers it.

## Per-bank questions
1. **Where is Gross NAV / Net NAV?** What is the exact row label? (e.g. UBS:
   "Total gross assets", "Total net assets"; BoS: "Assets" row / "Total Net Asset
   Value"; LGT: only "Total".)
2. **Number format** — commas (`10,208,537.88`), spaces (`7 032 282`), or other?
   Currency prefix shown (SGD/USD)? Decimal places?
3. **One client per PDF, or several?** If several portfolios/accounts appear in one
   PDF, which figure is the account-level one we want?
4. **Multi-page?** Is the figures section always on page 1, or can it move?
5. **Edge cases** — can Net = Gross (e.g. BoS when liabilities are 0)? Can values be
   negative (LGT)? Any "as of" date variations in the label?
6. **Account number** — where does it appear on the statement (top header? a labelled
   field?) and what does it look like (length/format)? (Used by the AI step — see
   `FOR_COLLEAGUE_AI.md`.)
7. **Anything weird** — footnotes, asterisks, sub-totals that look like the total, etc.

---

## The fastest, safest way to actually finish this
**Dummy statements.** Ask your colleague to take one real PDF per bank and replace the
names/account numbers/figures with *fake* values, keeping the exact layout, fonts and
labels. Those fake PDFs are safe to send me. I tune the parser against them and it will
then work on the real ones — because the parser keys off layout and labels, not values.

If even that's too much: she runs the tool on real files herself and sends me only the
**log line** (numbers, no names) or the resulting **Excel row**, and screenshots of any
spot the tool got wrong. I debug from that without ever seeing client identity.
