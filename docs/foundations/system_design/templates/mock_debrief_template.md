# Mock debrief — <Question> (<YYYY-MM-DD>)

> Copy to `../mocks/<YYYYMMDD>_<slug>.md` and fill it **in the session, right after the mock.**
> The rating goes in [`../mastery/design_progress.md`](../mastery/design_progress.md); this file is the
> evidence behind it and the source of the next deep-dive round.

| | |
|---|---|
| **Question** | [<name>](<hellointerview url>) — <Easy/Medium/Hard> |
| **Cold?** | **yes** / **no — breakdown already read, so this caps at 🟡** |
| **Time** | <start>–<end>, <n> min |
| **Rating** | 🟢 / 🟡 / 🔴 — proposed by the coach, confirmed by the learner |

## Score — the seven checkpoints

| # | Checkpoint | Pass? | Evidence — what actually happened |
|---|---|---|---|
| 1 | Requirements | ✅/❌ | |
| 2 | Estimation | ✅/❌ | |
| 3 | API + data model | ✅/❌ | |
| 4 | High-level architecture | ✅/❌ | |
| 5 | Forks defended | ✅/❌ | |
| 6 | Failure modes named unprompted | ✅/❌ | |
| 7 | Evolve & operate (incl. the curveball) | ✅/❌ | |

**Evidence, not impressions.** "Named the celebrity hot-key before being asked" is evidence; "seemed
comfortable with fan-out" is not.

### Staff signals — observed, not scored

Not an eighth checkpoint. Noted because they are the difference between a correct design and a senior
one, and because they are invisible unless written down at the time
([the post](https://www.hellointerview.com/blog/staff-level-system-design)).

| Signal | Observed? | Note |
|---|---|---|
| Peer-level — didn't explain the 101 unprompted | | |
| Triaged what's hard vs routine, early | | |
| Justified the complexity it carried — ⚠️ **and the design still meets the pinned NFRs** (non-functional requirements) | | |
| Transferred something actually operated before | | |
| **Decided, rather than listing options** | | |

### ⬆️ Probes that went above the current bar

Listed separately from the score **on purpose**: these cost nothing on the rating. Without this section a
later reading cannot tell *didn't know it* from *wasn't expected to yet*.

-

## The design that came out

<Mermaid diagram or a 5-line prose description of the boxes and arrows. Enough to make the next
deep-dive round possible without re-running the mock.>

**Numbers pinned:** <QPS, storage, bandwidth, ratios — whatever was committed to>

**Forks taken:** <trigger → choice → why → where it breaks>

## The curveball

**Thrown at ~minute <n>:** <the requirement change>

**What happened:** <what broke, what was kept, what it cost — and whether the learner or the interviewer
named the breakage first>

## ❓ Open probes — the bank

**Bare questions only. Never write the answer here.** These are what the next deep-dive round on this
design runs on, and an answered probe is a spent probe. Bound them by the L6 ROI line — everything
interview-relevant that this mock could not answer, and nothing else.

1.
2.
3.

## Study assignments

What this mock showed is missing, pointed at the material that covers it. **These are the learner's own
study time, not slots.**

- <gap> → [HelloInterview: <page>](<url>)
- <gap> → local card: [<card>](../concepts/<card>.md)
