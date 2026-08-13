---
name: project_sd_mock_model
description: SD = mock interviews on HelloInterview's 35-question board (Aug 13, 2026) — learner studies independently, coach interviews and scores; the three-lane study model is retired
metadata:
  type: project
---

**Set by the learner Aug 13, 2026**, replacing the three-lane study model outright:

> *"SD is way too open ended for us to tackle the way we've been tackling it. Let's do this instead. I
> will study on the side via HelloInterview and your job is to hold mock interviews based on the
> questions."*

**The split:** the learner learns system design on their own via HelloInterview. **The coach's entire
job is cold mock interviews on HelloInterview's questions, scored on the 7-point rubric.** Nothing on the
schedule is "read about X". Teaching happens on request, off-schedule, unrated.

| | |
|---|---|
| **Board** | HelloInterview's 31 question breakdowns + 4 no-write-up practice questions = **35 rows**, at their tiers |
| **Cadence** | `mock_plus_deep_dive` — Sunday cold mock (3.0 units) + one **conditional** midweek deep-dive round (2.0), which does not exist until a design is banked with open probes |
| **Rating** | 🟢 needs #1–4 **and** #5 forks / #6 failure modes / #7 evolve-operate. **A prepared mock (breakdown already read) caps at 🟡** — ask before, not after |
| **Artifacts** | one debrief per mock in `system_design/mocks/`, whose `❓ Open probes` section is the deep-dive round's material |

## ⏸️ Current state: STUDY MODE — no SD slot goes on the board (set Aug 13, 2026, same session)

> *"let's skip this week's mock interview. I will be doing core concepts + key technology on
> HelloInterview and when I am ready, I will be coming over to do the mock interviews. So I will do
> another restructure session to lockdown the core concepts + key technologies in a way where we don't go
> too deep and make sure they are where they need to be for a system design interview."*

- **Build every week with zero SD slots** until the learner opens one. No mock, no deep-dive round, no
  placeholder.
- **The next SD session is a restructure session**, not a mock: scoping Core Concepts + Key Technologies
  to **interview depth and no deeper**, so their study has a stopping condition. **They call it.**
- ⚠️ **Do not nudge.** Asking "ready for a mock yet?" at each build converts a learner-owned gate into a
  coach-owned one, which is the same failure as driving progression ([[feedback_let_learner_pace]]).
- **The whole board is 🔴 and inert**, including Rate Limiter — its three July reps were cleared at the
  learner's request in the same pass, because they were staged sessions against a different rubric on a
  different source and a carried-forward 🟡 would price a re-mock against a rating no mock produced.
- **Cost, already accounted:** every day without an SD slot carries an unseen DSA problem, which is now
  all seven; intake caps bind before that rule does, so probes fill the remainder.

### ⭐ Depth: a HIGH ceiling, a SENIOR bar — they are different things

The learner corrected the first framing (*"interview depth and no deeper"*) the same day:

> *"there is a staff engineer system design section that is worth exploring after this initially
> junior/senior level system design is done so we can have a high ceiling during the mocks but not
> exceptional depth is expected."*

- **Ceiling = how far a probe may go: high.** Keep pushing until the answer runs out; that is how the
  edge gets found, and an interviewer who stops at the bar never locates it.
- **Bar = the depth a checkpoint must reach to pass: junior/senior.** Exceptional depth does not gate 🟢.
- **So a probe that runs past the bar costs NOTHING on the rating.** Record it under `❓ Open probes` and
  mark it *above the current bar* — that distinction is what later lets someone tell "didn't know it"
  from "wasn't expected to yet."
- **The rubric is unchanged.** #5 forks / #6 failure modes / #7 evolve-operate are **habits of reasoning,
  not exotic knowledge**; a senior candidate has them. Staff material later deepens a single deep dive,
  it does not add checkpoints.
- **Sequence:** core at senior depth → mocks → **then** the staff tier, which **raises the ceiling, not
  the bar**. ⏳ Its source is not yet pinned — HelloInterview's *in a hurry* pages carry no staff section;
  their level-keyed material looks like the company guides (`/guides/meta/e3`…). **Ask for the link; do
  not guess a URL.**
- ⚠️ **When the bar moves, ratings stop being comparable across the move** — same failure as rewriting a
  Recall Card mid-series. Date the change in `study_guide.md` and read earlier 🟢s as "🟢 at the senior bar."

**What was retired, so it doesn't creep back:** lanes ①/②/③ · note-building as a scheduled rep ·
Recall-Card blind sprints · the Bootstrap→Transition→Mastery arc · designs-pull-blocks and its pull queue
· the prerequisite-tech gate · the technology/concept/component tracker rows (now frozen reference cards,
off the review engine). **The AI System Engineering track was deleted in the same pass** — never started,
no sessions, no trigger to restore; its one interview-relevant design is the **ChatGPT** row.

**Why, and this is the part worth keeping.** The repo was trying to be a textbook *and* a scoreboard.
After ~6 weeks of lanes the textbook half stood at **2 of 9 technology notes, 0 of 8 patterns, 2 of 9
core concepts** — not a diligence failure, a scope failure: writing a system-design textbook is
open-ended work with no exit condition, and it competed for the same slots as the thing being graded.
HelloInterview is a finished textbook. **The repo keeps the two jobs it is better at than a website:
measurement over time, and the adversarial half you cannot do alone.**

**How to apply.** Read `system_design/study_guide.md` (mechanics) before running a mock and
`senior_ramp.md` (order, phases, rubric) before proposing one. **Never write the question into the weekly
schedule file** — that lets its breakdown be read in advance, which caps the mock. Name it at the session,
same discipline as [[project_recognition_probes]]. Previously attempting a design is *not* "prepared";
reading the worked answer is. Related: [[feedback_coverage_gap_ledger]] (the probe bank moved into the
debrief), [[project_sd_roi_line]], [[feedback_dsa_before_sd]].
