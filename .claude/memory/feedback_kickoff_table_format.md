---
name: feedback_kickoff_table_format
description: Kickoff board table — problem name IS the file link; no separate file column
metadata:
  type: feedback
reconciled: 2026-08-30
---

The start-of-day kickoff board is a compact table: the **problem name is the markdown link to
its `.py` file**, and a trailing `[LC]`/`[NC]` cell carries the source link. **No separate file
column** — collapse it into the linked name.

Columns: `#` · `Problem` (linked to the .py path) · `Start` (comfort) · source link (`[LC]`/`[NC]`).

**Why:** The learner asked for this Aug 22, 2026 — *"the link can just be the problem and no need
for a file column at all."* A standalone repo-path column was redundant once the name itself links.

**How to apply:** Keeps both links the kickoff rule requires ([[feedback_kickoff_table_links]] — the
.py path AND the LC/NC url), just packed into two cells instead of three. Premium problems (e.g. 271)
link NeetCode, not the dead LC page.
