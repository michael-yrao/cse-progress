---
name: feedback_self_evaluation
description: On any self-correction, append a note to self_eval_log.md; periodically meta-review the log to promote recurring mistakes into durable rules
metadata:
  type: feedback
reconciled: 2026-09-10
---

Run a continuous self-improvement loop so mistakes convert into durable rules instead of silently recurring.

## 1. On every correction — log it

Whenever something you did gets corrected — whether **you** catch it or the **user** does — append a one-line dated entry to `self_eval_log.md` in this folder. Do this in the same flow as the fix, not later. An entry is warranted for: a wrong value logged, an artifact mislabeled, a missed propagation (unstaged file, unscheduled due problem), a spoiler slip, a bad assumption, etc. Format:

```
- YYYY-MM-DD — <what went wrong> → <the fix>. Root: <why it happened>. [P1|P2] (status: open | consolidated→[[rule]])
```

`[P1]` = broke "close the loop completely/proactively"; `[P2]` = broke "user owns thinking + code, you coach" (see [[feedback_operating_principles]]). Default status is `open`.

## 2. Periodically — meta-review the log

At the **start of each week's first session** (or whenever `open` entries reach ~8), do a self-evaluation of the self-evaluations:
- Cluster the `open` entries by root cause.
- Any root cause that appears **2+ times** gets promoted — **using the ladder below**, so the mistake is prevented structurally, not just remembered.
- Mark promoted entries `consolidated→<the actual fix>`. Leave true one-offs `open` (they may still cluster later).
- Keep the log append-only; don't delete entries, just update their status.

### ⚠️ The intervention ladder (added 2026-08-02, from the first full clustering pass)

**A memory file is the WEAKEST available fix and must not be the default.** Measured over 47 entries:
of the 9 rules promoted to a memory file with ≥10 days of exposure, **7 recurred anyway** —
`feedback_no_spoilers` five times, `feedback_read_before_asserting` four. Meanwhile **4/4 entries closed
`fixed-at-source` never recurred**, and the two memory promotions that held (`feedback_infer_comfort`,
the old SD lane structure, since retired — now [[project_sd_mock_model]]) held because they are *not really paragraphs*: one
is a numbered step in CLAUDE.md's workflow, the other is encoded in the shape of the schedule files.

Rank the options; take the strongest one that applies:

1. **Source fix** — make the tool structurally incapable of the mistake. *(4/4 held)*
2. **Hook** — bind it to a tool call or event the mistake cannot avoid. `scaffold_links_reminder.py` ended
   a 5-lapse streak that four memory-file reinforcements had not dented.
3. **Numbered step** in a workflow the agent must walk through to finish the task. Two homes, and the
   choice is by trigger (added 2026-09-10 with the skill refactor):
   - **A skill reference** (`.claude/skills/cse-coach/references/*.md`) for a **coaching-moment** rule —
     one that fires when the learner starts/reviews a problem, scaffolds, builds the week, or runs a mock.
     The skill loads reliably at exactly that moment, so a step placed there is read when it is needed and
     costs nothing the rest of the time. This is the strongest "step" for a coaching rule.
   - **The always-injected CLAUDE.md** for a **cross-cutting / unprompted** rule — one with no single
     coaching trigger (an always-on gate, a repo-maintenance meta-rule). CLAUDE.md is injected every turn,
     so the rule fires without the skill being loaded.
4. **Memory file** — reserve for genuine judgement calls with **no mechanizable trigger** (e.g. "strip down
   instead of explaining more"). *(7/9 recurred)*

**Diagnostic question for any lapsing rule: "is this a step in an executable list, or merely a paragraph?"**
— and, once it is a step, **"does it fire at a coaching moment (→ skill reference) or unprompted (→ CLAUDE.md)?"**
A rule that must fire *unprompted* cannot live only in an opt-in read (a memory file *or* a skill reference):
CLAUDE.md is always injected, the skill and memory are opt-in, and on 2026-08-02 an entire session ran with
no memory loaded at all. See `decisions.yml` `skill-layer-in-intervention-ladder`.

**This section applies to this file too.** The meta-review was itself a paragraph-rule with no trigger, and
it went unrun for 19 days while the log grew to 20 `open` entries against a threshold of ~8. It is now
gate 2 in `.claude/hooks/session_start_memory.py`.

**Why:** The user wants mistakes to feed back into the system. A one-off correction is noise; a *repeated* one is a missing rule. This loop surfaces the repeats. It's the same synthesis we did manually to produce [[feedback_operating_principles]] — now automated and ongoing.
