---
name: feedback_expand_acronyms
description: expand every acronym in parentheses on first use in a session — SD/networking/AI lanes are dense with them and the learner is 10 years out from school
metadata:
  type: feedback
---

**Expand every acronym on first use, inline, in parentheses** — "VPC (Virtual Private Cloud)", "RTT
(round-trip time)", "SNI (Server Name Indication)". Set by the learner Aug 3, 2026 mid-networking
session: *"when we do acronyms and there are a lot in networking, can we make sure to put in
parentheses what they are or what they stand for. I dont know what a VPC is."*

**Why:** system design and AI-systems material is unusually acronym-dense, and the learner is ~10
years past the coursework where these were introduced (their words). An unexpanded acronym doesn't
degrade the explanation gracefully — it **halts** it: they either stop to ask (costing a turn) or nod
past a term the rest of the paragraph depends on. That is the [[feedback_spine_first]] failure in
miniature — volume of correct detail displacing the load-bearing idea — except here one word does it.
It also silently breaks the Recall Cards, which are written to be answered cold weeks later.

**How to apply:**
- First use in the session gets the expansion; later uses don't need it. Do it in **chat and in the
  written note** — the note is reread cold, where there is no one to ask.
- Applies to the ones that feel too basic to expand, which are exactly the ones that get skipped:
  IP, TCP, TLS, DNS, CDN, VPC, RTT, LB, QPS, TTL, ACID, CAP.
- A `## 🔤 The acronyms, expanded` table at the top of a concept card is the durable version of this
  (see `concepts/networking_basics.md`) — write one for any card with more than ~4 acronyms.
- Don't over-swing into a glossary lecture: expansion in parentheses, then keep going. The expansion
  is a parenthetical, not a section.

Related: [[feedback_spine_first]], [[feedback_turn_economy]] (depth goes in the note, not the chat).
