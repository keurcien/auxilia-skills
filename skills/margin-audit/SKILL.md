---
name: margin-audit
description: Recompute gross margins from raw order exports and flag operations below target. Use when margins look off, when finance asks for a margin audit, or before a pricing decision.
license: MIT
compatibility: Requires Python 3.11+ with pandas and openpyxl
metadata:
  author: keurcien
  auxilia-requires: "python>=3.11; pandas>=2.1, openpyxl; egress=none"
---

# Margin audit

## When to use

Margins reported by an operation look wrong, or someone wants them recomputed
from the raw export rather than trusted from the dashboard.

## Steps

1. Ask for the raw order export (CSV) if it is not already in the workspace.
2. Clean it: `python scripts/clean.py <export.csv> cleaned.csv` — drops
   cancelled orders and normalises currency columns.
3. Compute margins per operation: `python scripts/margins.py cleaned.csv margins.xlsx`.
4. Read `references/rules.md` for the margin targets per category before
   flagging anything.
5. Report the operations below target, worst first, with the recomputed
   margin next to the reported one.

## Testing without a real export

`python scripts/fake_data.py fake.csv` writes a synthetic export that
`margins.py` reads directly. Add `--raw` to get currency formatted like a real
export (`12,50€`) so the file has to go through `clean.py` first. Four of the
twelve generated operations sit below their category target.
