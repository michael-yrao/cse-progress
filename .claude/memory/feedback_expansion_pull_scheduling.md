---
name: feedback_expansion_pull_scheduling
description: Post-NC150, weekly schedule generation populates application slots via pull_interview.py gated by learned patterns and weighted by comfort; pulled problems get identical Clean/Shaky/Blank treatment
metadata:
  type: feedback
---

Once NC150 is largely retired and the learner enters the knowledge-expansion phase, **weekly schedule generation is the trigger** for the application thread. This extends [[feedback_end_of_week_schedule]] and [[feedback_proactive_scheduling]] — the weekly build now assembles, in priority order:

1. **Due reviews first (spaced-rep sweep)** — everything with `Next Review Date ≤ end of the coming week`, slotted Blank → Shaky → Clean → Retired.
2. **Active blocks = current learning** — the next **expansion-tier techniques** (segment tree, KMP, XOR trie, …) from the expansion queue. This is the protected 45-min slot.
3. **Application pulls = warmup/remaining slots** — run `python scripts/pull_interview.py --company <Name>`, which gates a company's problems to patterns already learned (detected from `dsa/leetcode` solution folders). **Weight by comfort:** check the comfort level of each already-learned pattern and favor pulls that exercise patterns trending 🟡 Shaky (reinforce the slipping ones) over ones solidly 🟢/🏆.
4. **Identical Clean/Shaky/Blank treatment** — a pulled interview problem is a first-class tracked problem: scaffold it, solve it, ask Clean/Shaky/Blank, log it in `dsa_progress.md`, let spaced repetition schedule its return. Pulled problems, expansion-technique problems, and NC150 problems are all handled the same way — nothing about a pull is special once it's in the tracker.

**Why:** The user specified that the interview pull isn't an ad-hoc tool — it's driven by the same weekly-schedule cadence as everything else, informed by per-pattern comfort, so application practice flows through the identical spaced-repetition engine as NC150.

**How to apply:** During NC150 (milestone phase) there are no interview pulls yet — the roadmap is the work. Once in the expansion phase, at weekly generation: sweep reviews → fill active blocks with expansion techniques → fill remaining slots with comfort-weighted `pull_interview.py` suggestions → log and schedule all of them via the normal comfort system. Respect the daily cap; protect the active block.
