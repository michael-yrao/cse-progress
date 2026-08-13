# System Design Study Guide — the mock-interview model

> **📍 Overarching career goal & apply strategy → [`../career_strategy.md`](../career_strategy.md).**
> SD *sequence, rubric and phase gates* → [`senior_ramp.md`](senior_ramp.md).
> This guide is the SD *mechanics*: how a mock runs, how it is scored, what gets written down.

## The split — study is yours, the interview is mine

**Adopted Aug 13, 2026, replacing the three-lane study model.**

| | Owner |
|---|---|
| **Learning system design** — concepts, technologies, patterns, the worked breakdowns | **the learner**, via [HelloInterview](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction), on their own time, off the schedule |
| **Interviewing you on it** — cold mocks, sustained pushback, scoring, what to fix next | **the coach**, in the slots below |

**Why the old model was replaced, stated once so it isn't relitigated.** The repo was trying to be a
textbook *and* a scoreboard, and the textbook half never finished: 2 of 9 technology notes written, 0 of
8 patterns, 2 of 9 of HelloInterview's core concepts — after roughly six weeks of lanes. That is not a
diligence problem. Writing a system-design textbook from scratch is open-ended work with no exit
condition, and it was competing for the same slots as the thing that actually gets graded. HelloInterview
is a finished textbook. The repo keeps the two jobs it is genuinely better at than a website:
**measurement over time**, and **the adversarial half you cannot do alone.**

**What this means in practice:** nothing on the schedule is "read about X" any more. If a mock shows you
don't know sharding, the fix is your own study time on HelloInterview's sharding page, not a slot.

## ⏸️ Current state: study mode — no SD slot is scheduled (set Aug 13, 2026)

**The learner is working through HelloInterview's Core Concepts and Key Technologies first, and mocks
start when they say so.** Until that signal:

- **No SD slot goes on the weekly board.** Not a mock, not a deep-dive round, not a placeholder. A day
  with no SD slot carries an unseen DSA problem by the standing rule, so the cost is already accounted
  for.
- **The next SD session is a restructure session, not a mock** — scoping Core Concepts + Key
  Technologies to *interview depth and no deeper*, so the study has a stopping condition. The learner
  calls it; do not schedule it.
- **Don't nudge.** Asking "ready for a mock yet?" at each build converts a learner-owned gate into a
  coach-owned one. Mocks begin when they open one.

**This is a state, not a pause with a date** — it clears on their word, which is repo-evaluable in the
only sense that matters here ([[feedback_gate_on_internal_state]]): it is their call about their own
readiness, never an external event or a calendar.

## Cadence — two slots, and one of them is conditional

| Slot | Shape | Cost | Runs when |
|---|---|---|---|
| **Sunday — the mock** | one **cold ~45-min mock** on the next question, + ~15 min debrief | **3.0 units** | always |
| **One midweek — the deep-dive round** | ~25 min of sustained pushback on a **design already mocked**: forks, failure modes, evolve/operate (rubric #5/#6/#7 only). No new question, no framework walk | **2.0 units** | only once ≥1 design is banked, and only against a design whose debrief has open probes |

**The third lane is gone and the slot goes back to DSA warmups.** Under `three_weekly` the two midweek
slots cost four DSA warmup reps a week; the deep-dive round costs two. The rest returns to the 🟢 backlog.

**The deep-dive round is not a consolation slot.** At L6 the round is won on #5/#6/#7, and a full mock
spends most of its 45 minutes on #1–4 getting the skeleton down. Splitting them means the senior half
gets its own dedicated rep instead of whatever time is left at minute 40 — which, on every design run so
far, has been none.

**When nothing is banked, the midweek slot does not exist.** Do not fill it with reading, note-building,
or a second mock. An empty deep-dive queue means the board needs mocks, not more slots.

## The mock — how it runs

### Before

- **The question comes from [`senior_ramp.md`](senior_ramp.md)'s order**, one per session. It is named at
  the start of the session, not in the weekly schedule — see the cold rule below.
- **The mock must be cold on that question.** Cold means *you have not read that question's
  HelloInterview breakdown.* Studying the core concepts, technologies and patterns is the whole point of
  the split and never disqualifies anything; reading the worked answer to the exact question you are
  about to be asked does.
- **Having attempted the design before is not "prepared."** A second run at a question you once worked
  through yourself is a retry, and a DSA retry can still earn 🟢. What caps the rating is having read
  **the worked answer**, not having thought about the problem.
- **A prepared mock caps at 🟡.** If you have read the breakdown, say so up front — it is still worth
  running, and it still gets a debrief, but it cannot earn 🟢. Same rule as a no-code DSA blueprint: the
  rep is real, the measurement isn't. **Say it before, not after** — a 🟢 recomputed downward later is
  worth less than an honest cap.
- **The schedule names the slot, never the question.** Writing "Sunday: Ticketmaster" into the weekly file
  lets it be read up in advance, which destroys the only thing the mock measures. Same reason the
  recognition probe's problem is never written down.

### During — what the coach does

Interviewer, not coach. Specifically:

- **No teaching, no hints, no leading questions.** If you stall, the interviewer waits, then asks what
  you're weighing — they do not supply the box.
- **Timeboxed to HelloInterview's Delivery budget**, which is already [`framework.md`](framework.md):
  requirements ~5 min · core entities ~2 · API ~5 · high-level design ~10–15 · deep dives ~10. Time
  called out loud at each boundary.
- **Altitude held at HLD through steps 1–4.** Dropping into a box — fields, DB internals, persistence
  config — before step 5 gets named as the slip it is: *"drawing a box, or standing inside one?"*
- **Every bare adjective gets pushed on.** "Read-heavy" → what ratio, what absolute numbers. Every choice
  gets asked for its condition and its breaking point. This is the interviewer doing it, not the coach
  reminding you to.
- **One curveball requirement change, around minute 30**, mandatory at L6 — a new non-functional
  requirement that invalidates part of the design ("now it has to be multi-region", "now the write rate
  is 50×"). How the design bends is a graded checkpoint, not a bonus.
- **Deep-dive probes are drawn from the bank** — the previous debriefs' open questions, plus the standing
  probe list at the bottom of this file.

### After — the debrief

**The debrief is where the artifacts come from, and it is not optional.** Immediately after the mock,
in the same session:

1. **Score the seven rubric checkpoints pass/fail** ([`senior_ramp.md`](senior_ramp.md)), out loud, with
   the evidence for each — not a summary impression.
2. **Propose the comfort rating and confirm it with the learner** (same protocol as DSA: the coach infers
   it from what happened and proposes; the learner's call is final; honesty over agreeableness).
3. **Write [`mocks/<YYYYMMDD>_<slug>.md`](mocks/)** from [`templates/mock_debrief_template.md`](templates/mock_debrief_template.md): the score line, what the design ended up being, the
   curveball and how it went, and — the part that gets reused — **the open probes.**
4. **Log the row** in [`mastery/design_progress.md`](mastery/design_progress.md) and let the interval
   engine set the next date.

**Open probes are written as bare questions, never as summaries of the answer.** They are simultaneously
the coverage report and the next deep-dive round's material, and a probe that carries its own answer is
spent on the page. This is the rule that used to live in the teaching-session gap ledger; it moves here
intact because a mock generates the same thing more honestly — the questions you could not answer under
time pressure, rather than the topics the session happened not to reach.

## Rating

Full rubric and the reasoning behind it: [`senior_ramp.md`](senior_ramp.md). In brief:

| | |
|---|---|
| 🟢 **Clean** | #1–4 solid **and** #5 forks, #6 failure modes, #7 evolve/operate all pass. Cold only |
| 🟡 **Shaky** | skeleton solid, senior half thin. Also the ceiling for any prepared (non-cold) mock |
| 🔴 **Blank** | couldn't drive the framework cold |

Intervals are the standard engine: +30 / +10 / +2, streak 2 → +60, retired at 3 → +180.

**A re-mock of the same question is a different rep, not a re-read.** By the time a 🟡 comes back at +10
days you will have studied the breakdown, so the second run is a *prepared* mock by definition — and it
is scored on #5/#6/#7, which reading the breakdown does not hand you. The rating floor rises with the
material, which is the intended shape.

## What the repo no longer does

Listed explicitly, because each of these will look reasonable again in a month:

- **No lanes ①/②/③.** One mock slot and one conditional deep-dive slot; nothing bids against them.
- **No note-building as a scheduled rep.** `technologies/`, `components/` and `concepts/` are frozen as
  reference. New cards are written only if the learner wants one, on their own time.
- **No blind sprints against Recall Cards.** Those measured whether a card was retained; the mock measures
  whether the knowledge shows up under pressure, which is the thing being graded.
- **No Bootstrap → Transition → Mastery arc.** One question = one row = one cold mock = one rating. A
  design spread across sittings cannot be rated cold, and an unratable rep leaves the engine while looking
  like progress.
- **No "designs pull the blocks" pull queue.** Hitting something cold mid-mock is now a line in the
  debrief and an assignment for your own study time, not a slot next week.
- **No prerequisite-tech gate.** It existed to stop a mock being wasted on unknown technology. You are
  studying ahead of the board now; if a mock lands on something you haven't read, that is information and
  the debrief records it.

**Teaching still happens on request.** Ask about anything, any time, and it gets explained properly —
spine first, procedure before proof, one job per turn. It is just not a scheduled slot, and it is never
rated.

## Standing probe bank — the interviewer's ammunition

Fired during deep dives and in the midweek round. Kept here because the coach owns them now; the learner
gains nothing from rehearsing the list, which is why it is not a study checklist.

- "What happens when this component dies? What about when it's *slow* rather than dead?"
- "How does this behave at 10×? 100×? Which piece saturates first?"
- "Two users do X at the same instant — what happens?"
- "Why *this* database / queue / cache and not the alternative? What would change your mind?"
- "Where's the bottleneck, and how would you shard/cache/replicate around it?"
- "How do you keep these two copies in sync? What if they diverge?"
- "How would you roll this out with zero downtime? How would you migrate the existing data?"
- "What does this cost, and what's the cheapest thing you'd give up first?"
- "Which failures take down one region and which take down all of them?"

### The recurring forks — memorize the deciding question, not the answer

| Fork | Deciding question | Picks A ⟶ / ⟵ Picks B |
|------|-------------------|------------------------|
| SQL ⟷ NoSQL | Multi-row transactions / joins, or scale-out + flexible schema? | ACID & relations ⟶ SQL / massive scale, simple access ⟶ NoSQL |
| Strong ⟷ eventual consistency | Is a stale read *incorrect*, or just slightly old? | money/inventory ⟶ strong / feeds, counts ⟶ eventual |
| Sync ⟷ async (queue) | Must the caller wait, or can the work be deferred? | needs the answer now ⟶ sync / fire-and-forget, spikes ⟶ async |
| Cache-aside ⟷ write-through | Read latency or write freshness? | read-heavy ⟶ aside / can't serve stale ⟶ write-through |
| Replication ⟷ sharding | Read-bound, or write/storage-bound? | too many reads ⟶ replicas / too much data ⟶ shards |
| Push ⟷ pull (fan-out) | Few writers→many readers, or many writers→few readers? | celebrity read fan-out ⟶ pull / normal ⟶ push-on-write |

**The fusion sentence, which is what the rating is listening for:** *"I'll use [choice] because
[quantified pressure]; it trades [X for Y] and holds while [condition] — it breaks at [scale], where I'd
move to [alternative]."*

## Known gaps carried forward

- **HLD diagramming.** Named Aug 9, 2026 as a real gap, not an assumption (*"I don't know how to draw this
  at all"*). The notation is: a box is something that can fail independently, an arrow is a request from
  caller to callee, draw one path at a time left to right. Tooling: Excalidraw for whiteboard motion,
  Mermaid in the debrief for the durable copy. **If this blocks a mock again, it becomes a requested
  teaching session, off-schedule and unrated** — not a lane.
- **Networking / TCP.** Rolled back to untaught Aug 9 at the learner's request (*"I don't feel I actually
  maintained it at all"*). Now a HelloInterview study item —
  [Networking Essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials).
  The local card ([`concepts/networking_basics.md`](concepts/networking_basics.md)) stays as reference.

## Below the interview-ROI line — after all this, not during

Real-world depth with low interview return. Not scheduled, not tracked; listed so the boundary stays
visible. **Designing Data-Intensive Applications** (Kleppmann) cover to cover · consensus internals (Raft
→ Paxos → ZAB) · distributed transactions (2PC, sagas, Percolator, Calvin) · consistency theory
(linearizability → causal, CRDTs) · storage engines (LSM vs B-tree, WAL, MVCC) · stream processing
(exactly-once, watermarks, backpressure) · the foundational papers (GFS, MapReduce, Bigtable, Dynamo,
Spanner, Chubby, Kafka, Raft).

## Where things live

| Thing | Owner |
|---|---|
| **State** — comfort, streak, next review per question | [`mastery/design_progress.md`](mastery/design_progress.md) |
| **The plan** — question order, the 7-point rubric, phases + exit gates | [`senior_ramp.md`](senior_ramp.md) |
| **The mechanics** — this file |
| **The syllabus** — what topics exist | **HelloInterview.** The local cross-walk is [`coverage_map.md`](coverage_map.md) |
| **The delivery framework** — the six steps and their budgets | [`framework.md`](framework.md) |
| **Mock debriefs** — one per mock, the open-probe bank | [`mocks/`](mocks/) |

**Reference material, frozen:** [`technologies/`](technologies/) (2 cards) ·
[`components/`](components/) (3) · [`concepts/`](concepts/) (9) ·
[`case_studies/url_shortener.md`](case_studies/url_shortener.md) (superseded by the Bitly mock) ·
[`archive/`](archive/).

⚠️ **A status written in prose is a status that will be wrong in three weeks.** If the engine can compute
it, do not write it here.
