---
name: feedback_kickoff_table_format
description: Kickoff board table — problem name IS the file link; no separate file column
metadata:
  type: feedback
reconciled: 2026-08-30
---

⚠️ **TIGHTENED Sep 4, 2026 — a presented lineup is PROBLEM NAME + LINKS, NOTHING ELSE.** No
technique, no note, no difficulty, no comfort, no units. The learner: *"The tables should just be
the name of the problems and links, nothing else."* Anything in a Note/Focus column — or a technique
parenthetical carried in the title (`Course Schedule IV (Floyd-Warshall)`, `closes the Stack phase`) —
**spoils the recognition front-gate**, which is the whole thing the gate exists to measure. Comfort/
units belong in the schedule file for planning; they do **not** ride the lineup shown to the learner.

**⭐ SOURCE FIX (rung 1) — build the lineup from `scripts/links.py <n> ...`, VERBATIM. Never
hand-copy schedule rows.** `links.py` reads the title from the file header, so it emits a clean
`[<n> <title>](path) · [LC/NC]` with no technique parenthetical and no Note column. Hand-copying a
schedule row is exactly how the spoiler leaks — the row carries `(Floyd-Warshall)` in its title and a
Note cell full of rep directives. Run the script, paste its lines, add nothing. This is the same
top-of-ladder move that keeps the scaffold-links and broken-path cases from lapsing.

**Why a source fix and not more prose:** this lapsed twice in two days as a paragraph rule (124 on
Sep 3 — a "Focus" column; 84/1462 on Sep 4 — technique in title + Note column), each time because the
output format was rebuilt by hand from the schedule. A rule anchored to *"remember to strip the
columns"* decays; a rule anchored to *"the lineup IS `links.py` output"* has nothing to strip.

**Legacy (superseded above):** The kickoff board was a table with `#` · `Problem` (linked) · `Start`
(comfort) · `[LC]`/`[NC]`. The learner asked Aug 22, 2026 to fold the file column into the linked name
(*"the link can just be the problem and no need for a file column at all."*). The Start/comfort column
is now gone too — see the tightening above. Both links the kickoff rule requires
([[feedback_kickoff_table_links]]) still travel with the name; premium problems link NeetCode.
