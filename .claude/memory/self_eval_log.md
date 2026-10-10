# Self-Evaluation Log

<!-- single-source-ok: an append-only dated log. Entries state what a value WAS at the time,
     which is the point of a log — they must never be back-dated to match today's config. -->

Append-only log of corrections. Governed by [[feedback_self_evaluation]]. Newest at top. Meta-review promotes recurring root causes into rules; entries are never deleted, only re-statused.

## 🔬 META-REVIEW 2026-09-19 — the review pipeline itself got instrumented (digest + archive), plus 2 promotions

Triggered by the OVERDUE banner (~14 open since the 2026-09-10 review). Run LITM-safe: clustered from
`python scripts/meta_review_digest.py` (one line per open entry) instead of reading the ~1350-line log —
which is the point of this review, since the learner asked for a way to "read these and update skills/hooks
without getting hit with LITM." The digest is now the standing instrument for that.

**Instrumented the loop (Interest 2):**
- **`scripts/meta_review_digest.py`** (new) — prints the open entries as ~15 lines so a review never pays the
  ~79K-token scan. Tag-agnostic, so it caught two untagged entries the SessionStart banner's `[P\d]` regex
  silently misses (2026-09-17/09-18). Format rule added to [[feedback_self_evaluation]] §1: every entry now
  carries `[Px]` (right after the date) AND a `fam:` recurrence-family tag, so future clustering is mechanical.
- **`self_eval_archive.md`** (new) — 49 closed (consolidated/resolved) blocks moved out (log 1358→1071 lines),
  byte-completeness asserted. All OPEN entries and both prior META-REVIEW sections stay in the live log.

**Promotions (2+ recurrence → up the ladder):**
1. **Banned openers** (Aug 15 prose, recurred 09-19) → **hook** `problem_link_reminder.py::banned_opener`
   (rung 2), the mirror of `advance_prompt_tail`; + SKILL.md §1 clause + `decisions.yml` `banned-openers-to-hook`.
2. **Kickoff scope-limiter** (09-12 greeting, 09-13 greeting, 09-18 name-alongside-session-start = 3×) →
   **skill reference** `scaffolding.md` scope § now states a problem name narrows scope ONLY when no
   session-start phrase shares the message, and never override the `kickoff_scaffold_reminder.py` flag.

**Recommendations — BUILT this session at the learner's go-ahead (all 3):**
- **Variant-label errors** (09-15 stale method-name suffix + 09-18 build tagged the wrong due variant, 3 rows
  = 2×): source fix in `new_problem.py::existing_method_name` (strips an accreted `_<date>[_variant]` run so the
  stub base can't accumulate; snake_case names untouched; 8 tests) + `weekly-build.md` rule (the board variant
  parenthetical is READ FROM the due tracker row, never hand-typed).
- **Overdue rows not seated on the built board** (09-14, schedule-integrity family): added check 3 to
  `scripts/check_schedule_integrity.py` — flags any tracker row due ≤ the week's Sunday that is seated on no
  day (reuses `effort_budget.parse_rows`). On first run it surfaced two real overdue 🟢s (875, 1584).
- **Scaffold-lifecycle phantoms** (watch-cluster: 08-31 delete-scaffold≠delete-row, 09-13 follow-on
  upfront-scaffold→phantom-rows, 09-16 stranded probe): new `scripts/check_phantom_scaffolds.py` flags phantom
  rows (empty Rep Dates / `Unknown` difficulty) AND stranded probes (an earned probe under `dsa/probes/`,
  outside `solutions.roots`). Found the real stranded probe 648. Wired report-only into pre-commit + close-out.

**Bookkeeping:** re-statused 09-17 dropped-721 (→ `remaining.py`, shipped in-body) and 09-12 (superseded by
09-13's hook+gate) to consolidated. Left genuine one-offs open (09-16 stuck_log-failure-mode, 09-17 912-rating,
09-14 bare-numbers [hook-covered]).

**Deferred (semantic, not mechanical):** batch-archiving the ~80 pre-09-10 open one-offs that survived prior
reviews. The digest already makes them cost-free (it filters to opens-after-last-review), so this is optional
cleanup, and re-statusing an open entry as "reviewed/dormant" is a judgement call, not a partition. Cadence reset.

## 2026-09-16 [P3] — logged the coach-caught bugs as the sticking point instead of the learner's own recurring failure mode (540)
Closing 540 🟡, the stuck_log sticking point I wrote headlined the three bugs *I* surfaced (midpoint formula, snap-ordering, `r=m`). The learner corrected: their actual recurring error is narrower and different — using a **value comparison** (`nums[m]` vs `nums[m±1]`) to snap to the pair-start, when that is a pure **index/modular** step; the `l=m+2` movement I'd bundled in was never their issue. The coach's caught-bug list ≠ the learner's repeated failure mode; a stuck_log entry is most valuable when it names the *latter*, which the learner often knows better than the coach. **How to apply:** when logging a non-Clean rep, ask/confirm "what's the part that keeps getting you?" before writing the sticking point, rather than defaulting to the bugs found this rep. Recurrence family: any 🟡/🔴 close-out. Fixed the 540 entry same turn. If it recurs, climb to a review-workflow step ("confirm the learner's own sticking point before writing the stuck_log line"). open.

## 2026-09-14 [P3] — bare problem numbers in end-of-turn tallies tripped the link hook 3× in one session
Three closing recaps ("today's tally: 207 🎓, 743 🟡, 787 🔴", "162 and the probe still open", etc.) named
board problems by bare number without a markdown link → `problem_link_reminder.py` blocked each, and I paid
the link debt each time. Enforcement is already handled (the hook catches it every turn, rung-2), so this is
not a missing-guard problem — it's that I keep *generating* the debt in the one place a link adds nothing (a
recap of work already linked earlier in the session), which wastes a turn per occurrence. Root: treating the
tally as prose rather than as a lineup subject to the links-only rule. Behavioral fix (stated in-session, now
durable): **in a recap of already-completed work, refer to problems by title or outcome, not by bare number**
— if a number must appear, link it. No rung-1/2 change needed (the hook is the safety net); this entry exists
so the habit is visible to meta-review rather than dying with the context window. Recurrence family: the
links-only rule ([[feedback_lineup_links_only]]) has lapsed 10+× historically. open.

## 🔬 META-REVIEW 2026-09-10 — first review in 40 days; the two live recurring roots were fixed structurally this session

Overdue by the loop's own cadence (last meta-review 2026-08-02). The 2026-09-10 memory-audit did the
structural clustering; this records the promotions and resets the cadence. The trigger itself was the
biggest finding — the meta-review had **no firing mechanism** and sat unrun; now computed by
`meta_review_banner()` in `session_start_memory.py` (see [[feedback_self_evaluation]]).

**The two roots with 2+ recurrences — both promoted OFF the memory layer this session:**
- **Lineup/link spoilers & missing links** (Focus/Note columns 09-03, 09-04; the 12-lapse links history).
  → Promoted to the **skill**: `references/scaffolding.md` "Presenting the kickoff / lineup board" +
  `references/review-workflow.md`, backed by the `links.py` source-fix. Memory why merged into
  [[feedback_lineup_links_only]]. This is a skill-reference promotion, the new top "step" rung.
- **Push-to-act / advance-the-learner tails** (08-26, 09-03, 09-04, 09-09). A memory paragraph
  ([[feedback_let_learner_pace]]) that kept recurring → promoted to **SKILL.md principle 3** ("the learner
  sets the tempo"), a top-level always-loaded coaching principle. Stronger rung than the paragraph.

**Everything else** reviewed as one-offs (no 2+ cluster) — left `open`; they may still cluster later.
**Ladder lesson reinforced:** both promotions went to the *skill* layer, not another memory file — the
skill loads at the coaching moment, which is exactly where these lapse. The memory-paragraph rung stays the
weakest (its 7/9 recurrence record is why).

**Deferred (mechanical, low-risk):** physically archiving the ~10 `consolidated→` entries + the 08-02 July
cluster body to `self_eval_archive.md` — the log isn't injected, so its size costs no context; do it when
convenient rather than risk mis-slicing an append-only file at session end.

- **2026-09-01 [P2] `open`** — Learner, mid-239: *"stop once the conversation has resolved… in the
  last 4 exchanges the agent suffixed with 'code it' with no added benefit."* After the recognition
  call was confirmed and the deque-direction invariant was settled, I kept appending an imperative
  tail (**"Code it."**) to three consecutive resolved turns. This is the **advance-prompt tail**
  ([[feedback_let_learner_pace]]) in imperative clothing — same failure as "ready for the next one?",
  driving progression the learner already owns. The turn was *done*; the tail added nothing and made
  the coach the one pushing pace. **Fix:** when a point resolves, end the turn — no "code it", no "go",
  no "on to X". Silence is the correct close. Watch for a cluster with [[feedback_let_learner_pace]]
  and [[feedback_turn_economy]] on redundant tails.

- **2026-08-31 [P2] `open`** — Caught at the weekly build, unprompted: **deleting an unattempted
  scaffold does NOT undo the tracker row it already minted.** 84 Largest Rectangle was scaffolded on
  Aug 30, the night stood down, and the file was deleted per the 227 precedent — but discovery had
  already run, and a row `| Unknown | 84 ... | 🔴 | 0 | | | |` was sitting in `dsa_progress.md`
  uncommitted, for a rep that never happened. Removed here; re-running `update_review_dates.py`
  confirms it does not come back (no file, no discovery). **The rule was incomplete, not wrong.**
  CLAUDE.md and both Aug 29/Aug 30 schedule notes say "delete the scaffold" as if that were the whole
  remedy; the row is a *second* artifact and needs its own deletion. It survived because it is
  invisible in normal use — blank dates mean it adds no scheduled demand and never appears in a due
  list, so nothing surfaces it except reading the tracker's tail. **Fix landed:** CLAUDE.md's scaffold
  rule now names both artifacts, and the phantom row's shape (`Unknown` difficulty + blank dates) is
  written down as the thing to grep for. Root cause: an undo written for the *cause* (the file) and
  not the *effect* (the row) — watch for a cluster on "cleanup that reverses the trigger but not the
  side effect."

- **2026-08-27 [P3] `open`** — Asked "what problems are left today", I answered with a table whose
  file links were **dead on click**: I copied the paths verbatim from the schedule row
  (`../../../dsa/...`, correct relative to the schedule file three folders deep) instead of writing the
  **repo-root-relative** path the chat renderer needs. Learner: *"clicking the link does nothing."* The
  correct form was already known — [[feedback_kickoff_table_links]]:44 specifies `dsa/...`. Root cause:
  transcription from the source artifact rather than emitting the documented form. **Gap surfaced:** the
  Stop hook (`problem_link_reminder.py`) validates that a number sits *inside* a markdown link, never
  that the path resolves — so a present-but-dead link passes it clean. Not cheaply closable (the hook
  can't know the chat renderer's base dir), so it stays trust-bound. **Fix on me:** when a schedule row
  is the source, rewrite its `../../../` prefix to a repo-root-relative path before emitting to chat.
  Watch for a cluster on "copied a relative path out of a nested file."

- **2026-08-20 [P2] `open`** — During a 53 (prefix-sum) discussion I wrote that 560/974/525
  "keep them all (min, or a hashmap)", conflating the min-prefix flavor (max subarray) with the
  hashmap flavors. Learner caught the inconsistency across two turns. **Fix stated:** min-prefix →
  max-sum only; count-map → 560/974 (counting); index-map → 525 (longest). Root cause: an imprecise
  parenthetical in a discrimination explanation — the exact place precision matters most, since the
  learner is building the recognition map. One-off for now; watch for a cluster of "loose parenthetical
  in a technique-discrimination answer."

- **2026-08-18 [P2] — ran `new_problem.py` as a "verification" and it stashed the learner's finished work.** After renaming 235's file, ran the scaffold command again to confirm it now resolved to the right path. **It is not a dry run.** It inserted an empty dated stub at the top of `class Solution` and moved the entire body — including the completed, already-rated Aug 18 attempt — out to `.history/`.
  **Caught immediately and fully undone**: empty stub removed, stash pasted back, stash file deleted, all six dated attempts verified present, and today's attempt re-run against its test cases to confirm the code is intact.
  **Why it was nearly worse than it looked:** `restore_history.py` would NOT have rescued this. Its guard checks whether today's dated attempt has a real body — the fresh stub was `pass`, so restore would have correctly declined, left the stash out, and the file would have been **committed as a blank stub with the real solution sitting in `.history/`**. Recoverable, but only by someone who noticed.
  **Root cause:** treating a **mutating** command as an inspection. The scaffold scripts are write-first by design; there is no read-only mode that answers *"where would this resolve?"*. ⚠️ **Rung-1 candidate:** `new_problem.py --dry-run` printing the resolved path and the create-vs-retry decision without touching disk. That is exactly the question being asked here, and there is currently no safe way to ask it.
  **Second-order note:** this is the third time today a durable artifact was damaged by an action taken to *check* something (the mis-priced day, the axis-fusion in `techniques.yml`, this). `open` — added to `project_upstream_candidates.md` scope alongside the `--schedule-day` defect.

## 🔬 META-REVIEW 2026-08-02 — the promotion step itself is the weak link

First full clustering pass (47 entries, 20 `open` — well past the ~8 trigger; the loop's step 2 had not
been run since Jul 14). The dominant finding is not about any individual rule. It is about **what the loop
does when it finds a repeat**, and it is measurable:

**Of the 9 rules promoted to a memory file with ≥10 days of exposure, 7 recurred anyway.**

| Rule | Promoted | Recurrences after promotion |
|---|---|---|
| `feedback_no_spoilers` | Jul 5 | **5** |
| `feedback_read_before_asserting` | Jul 14 | **4** |
| `feedback_session_dating` | Jul 14 | **3** |
| `feedback_spine_first` | Jul 14 | 2 |
| `feedback_ask_complexity` | Jul 22 | 2 |
| `feedback_git_commit` | Jul 1 | 1 |
| `feedback_no_prior_attempt_comparison` | Jul 13 | 1 |
| `feedback_infer_comfort` | Jul 13 | **0 — held** |
| `project_sd_three_lane_structure` | Jul 14 | **0 — held** |

**Writing a rule down is not an intervention.** Every one of those recurrences happened with the rule
already written, already promoted, and (in several cases) already re-read.

**What distinguishes the two that held is the finding.** `feedback_infer_comfort` is a **numbered step in
CLAUDE.md's LeetCode Review Workflow** — the agent cannot reach the end of a rep without walking past it.
`project_sd_three_lane_structure` is encoded in the **shape of the schedule files themselves**. Neither
depends on remembering anything at the right moment. Every rule that recurred is a **paragraph**: a
posture to hold, a thing to remember to check, with no step and no trigger.

Cross-check against the other intervention types in the log: **4 entries closed `fixed-at-source`
(Jul 8 UTF-8 decode, Jul 12 `solution_class_end`, and two others). Zero recurred.**

### The rule this promotes

> **When the meta-review finds a repeat, a memory file is the *weakest* available fix and must not be the
> default. Rank the options and take the strongest one that applies:**
> 1. **Source fix** — make the tool incapable of the mistake (best; 4/4 held)
> 2. **Hook** — fire on a tool call or event the mistake can't avoid (`scaffold_links_reminder.py`)
> 3. **Numbered step** in a CLAUDE.md workflow the agent must walk through (`feedback_infer_comfort`)
> 4. **Memory file** — only for genuine judgement calls with no mechanizable trigger (7/9 recurred)
>
> And the diagnostic question for any lapsing rule: **"is this a step in an executable list, or merely a
> paragraph?"**

### Cluster A — "already promoted, still broke" *(7 entries)* → the above; audit below

Jul 20 · Jul 23 · Jul 30 · Jul 31 (links ×4, plus Jul 27 read-before-hinting, Jul 29 retry-handover
spoiler, Aug 2 complexity gate). Actions taken today: complexity gate → **step 1** of the review workflow;
memory index → **`session_start_memory.py` SessionStart hook** (the Aug 2 miss happened because the memory
files were never loaded at all, so *every* memory-resident rule was out of play — this one fix raises the
floor under all of Cluster A). Links already got its hook Jul 31.

### Cluster B — date handling *(Jul 25, Jul 29; 4+ lifetime)* → ✅ **SOURCE FIX SHIPPED, same session**

`feedback_session_dating` recurred 3× post-promotion because the root is **in the tools, not the agent**.
Fixed at tier 1: new `scripts/session_date.py`, wired into `new_problem.py` and `update_review_dates.py`
(`restore_history.py` already had its own detection). `--date` exists on all three as an **override**.

**Two things the implementation taught that the prescription had wrong:**

1. **"Add `--date`, defaulting to now" is tier 4 wearing tier-1 clothes.** A flag that must be remembered
   is a paragraph with a CLI. The default has to be right unaided, or nothing changed.
2. **`git log` is the wrong signal, and testing against the real Jul 29 data is what caught it.** The
   first implementation asked *"was the last commit yesterday?"* — but in a past-midnight session the last
   commit is usually **also** past midnight and carries the rolled-over date, so the signal is polluted by
   the very bug being fixed. It failed the exact case it was built for. Compounding it, commits are batched
   to session end, so mid-session the newest commit is often the *previous* session's, 24h+ back. The
   working signal is the workflow's own invariant: **the tree is committed clean at session end, so a dirty
   tree in the small hours means a session is in progress** — no timestamp involved. Recent-commit is kept
   as a weaker secondary. Verified against a Jul 29 00:35 replay → correctly returns 2026-07-29.

### Cluster C — acting on unverified state *(4 open)* → partly mechanizable

Jul 7 (attempt count from memory) · Jul 10 (labelled "new" without checking the tracker) · Jul 25 · Jul 27
(coached a stuck learner without reading their file). The Jul 27 shape — *read before **hinting**, not just
before asserting* — is the one with teeth, because it risks handing over something the learner already had.
✅ **Shipped same session as CLAUDE.md LeetCode Review Workflow step 2** — *"if the learner says they're
stuck, READ THEIR SOLUTION FILE BEFORE SAYING ANYTHING."* Not before *asserting*; before **hinting**.
Promoted without waiting for the predicted 4th occurrence: the ladder says take the strongest applicable
fix now, and waiting for one more failure to justify a fix you can already make is the same deferral
pattern that let the Jul 29 close-out bug happen twice in one day.

Jul 7 and Jul 10 (citing history from memory; labelling "new" without checking the tracker) stay `open` —
both are "read the tracker cell first", which has no clean trigger moment yet.

### Cluster D — teaching posture *(2: Jul 14, Jul 28)* → legitimately a paragraph

"Kept explaining instead of stripping down." No mechanizable trigger — it depends on reading the learner.
Leave in `feedback_procedure_first`; the *two-pushbacks-then-go-concrete* clause is the closest thing to a
trigger and is already written. This is the category memory files are actually for.

### Cluster E — one-offs, correctly left open

Jul 1 (phase label) · Jul 2 (moved without clearing source) · Jul 23 (cap counted activities not problems)
· Jul 25 (freebie granularity) · Jul 26 (mechanism inventory) · Jul 29 (scaffold scope, learner-set →
already in CLAUDE.md). Each at 1 occurrence. Leave `open`; they may cluster later.

### Note on the loop's own health

The Jul 14 entry already warned: *"a log that accumulates without clustering is evidence nobody reads."*
It then accumulated for 19 days. **The meta-review is itself a paragraph-rule with no trigger** — same
disease as everything in Cluster A. It is now item 2 of the SessionStart hook's always-on gates, and
`feedback_self_evaluation` carries the intervention ladder above.

---

- 2026-08-19 — **Logged a recognition-gate miss on 323 Union-Find that wasn't one — the comment was right
  there in the file I had already read.** Asked twice, verbally, for shape → technique → discriminator;
  the learner went straight to code both times and I logged it in `recognition_gotchas.md` as *"gate not
  fired… no comment or answer given."* The file's first line, which I had read minutes earlier to check
  the code, was `# union find today` — a pre-code comment naming the technique. CLAUDE.md's own rule says
  *"the learner already writes pre-code comments; they paste that comment as the call"* — I asked for a
  spoken restatement of something already on the page, then penalized its absence. Learner: *"I skip it
  but still note down the technique in the comment on top so I don't have to copy paste it."* **Root:**
  same family as [[feedback_read_before_asserting]], sharper here because the read had already happened —
  the omission was in *crediting* what I'd read, not in failing to look. **Fix / how to apply:** treat an
  in-file pre-code comment as the recognition call by default; only ask verbally when the file has no
  comment at all before the first line of logic. Corrected the 323 ledger entry (partial credit: names
  the technique, no discriminator) rather than leaving the wrong one standing. [P2] (status: open — first
  occurrence of this specific shape; a 2nd would promote a "check the comment before asking" clause into
  [[feedback_recognition_gate]])

- 2026-08-17 — **Manufactured a deadline from a roadmap date range, then built a whole planning dilemma on it.** Working the Aug 24 seating I read *"Intervals + Greedy · Aug 24–Sep 13 · 14 problems"* as an obligation to land 14 by Sep 13, derived 5/week from it, found that fills all three weeks, and concluded the six carried items (84, 2097, 753, 34, 1552, 1462, 399) could not be absorbed until **Sep 14+**. I then presented that as a genuine choice — *"protect the phase date"* vs *"let the phase run long"* — and asked the learner to settle it. They corrected the premise: *"a phase is more like this is the introductory of this phase, not that we are planning to finish the phase by this date, thus advisory."* **[[feedback_phase_dates_are_advisory]] already said exactly that**, verbatim — *"a phase end-date is a checkpoint, not a deadline"* and *"a phase running long is a reason to keep intake LOW, never a reason to accelerate to finish it"* — and I had reconciled that very file earlier the same day. **Root:** every step of the arithmetic after the first was correct, which is what made it convincing; the error was entirely in step one, an unexamined premise imported from the shape of a table (a date range plus a count *looks* like a plan). Same family as the Aug 14 recognition-gate miss and the answer-length misapplication: a rule with an explicit trigger, executed as a general impression. **That is now four instances**, and the common thread is sharper than "trigger-as-vibe" — in all four I had the correct rule available and did not re-read it because the situation did not *feel* like the one the rule was about. **Fix / how to apply:** (a) the seating is now 3 phase + 2 carried per week, with every carried item dated Aug 24 / Aug 31 / Sep 7 instead of queued behind a phantom deadline; (b) the false choice is written into the schedule so it is not re-derived; (c) **when a plan's conclusion is "X cannot happen until date D", check what created D before presenting it** — if D came from a roadmap range rather than from an external constraint or the tracker, it is not a real date. [P1] (status: open — 4th trigger-as-impression instance; the meta-review should promote the pattern, not this instance)
- 2026-08-17 — **Committed and pushed ~12 times in one session under a rule that says ASK EVERY TIME — because CLAUDE.md still carried the superseded wording.** `feedback_batch_commits.md`, set by the learner the previous day, says *"ASK BEFORE EVERY COMMIT AND EVERY PUSH. No exceptions"* after the weaker *"commit once at session end"* let **31 commits** run in the Aug 15–16 session. I committed ~12 times on Aug 17, twice offering *"say the word and I'll push"* and then pushing anyway when the learner said *"call it a night"* — reading a close-out instruction as blanket authorization, which is precisely the *"do not decide unilaterally that this instance is the exception"* clause the rule spells out. **Root cause is NOT forgetting: CLAUDE.md step 8 still read "commit + push once at session end", with no ask-first clause.** CLAUDE.md is always injected; `.claude/memory/*.md` are opt-in reads — so when the two disagree, **the stale always-injected copy is the one that gets obeyed**, every time. ⭐ **This is the single-source-of-truth failure, in the rule about committing, found on the day I spent the whole session fixing that exact class elsewhere** — and it was invisible to every detector built: the value checker only tracks `cse.config.yml` numbers, and the retired-vocabulary list had no entry for the superseded *phrasing* of a workflow step. **Fix / how to apply:** (a) CLAUDE.md step 8 rewritten to carry the ask-first rule verbatim, with the note that the weaker rule lived *here* and that is why it won; (b) `ask-before-commit` added to `decisions.yml` so every rule file must now reconcile against it; (c) the standing behaviour — make edits, say what is staged, **stop**. Say "this is ready to commit" and wait. [P1] (status: open — first occurrence for me, but the second time this rule has been broken at scale, and the first time the cause was traced to CLAUDE.md rather than to judgement)
- 2026-08-17 — **Applied a brand-new rule to the one case it excluded, in the very next turn.** The learner adopted a hard cap: *"when answering a user question, it cannot be bigger than a small paragraph… additional info and followups can be provided in the form of a question on whether they want certain portions expanded."* I wrote it into CLAUDE.md **with the exclusion already stated** — *"answering a question — not doing work, not reporting a rep — is capped"* — and then, in my next message, applied it to a **work report**: truncated the account of what I had just committed and closed with *"want me to expand on any of…"*. The learner corrected it immediately: *"explaining what you did should not require a prompt from users. answering the users should."* **Why it is worse than a length error:** it produces the opposite of the rule's purpose. The cap exists so the load-bearing sentence gets read; gating a work report behind a question means what changed, what broke and what is unfinished are *withheld*, and the learner has to spend a turn buying back the record of work already done. **Root:** I encoded the distinction and then pattern-matched on surface shape — "my turn is long" — instead of on the trigger the rule actually names ("is this an answer to a question, or an account of what I did?"). Same family as [[feedback_ask_complexity]] and the Aug 14 recognition-gate miss: a rule with an explicit **trigger** executed as a general **mood**. That is now three instances of the same failure mode across three unrelated rules, which is the pattern worth promoting, not this rule's wording. **Fix / how to apply:** the cap is on *answering*; a work report is **delivered in full, unprompted** — what changed, what broke, what is still unfinished, stated without being asked. Never offer to explain your own work. When a rule names a trigger, check the trigger, not whether the output *feels* like the thing the rule was complaining about. [P1] (status: open — first occurrence for this rule, third for trigger-as-vibe; watch whether the next long turn is a report that gets truncated)
- 2026-08-14 (late) — **Flag-and-proceed on an off-schedule pull, plus a spoiler I authored one turn earlier.** In the 739 debrief I wrote up the index regression by **quoting the learner's own Aug 10 pre-code call on 503 verbatim** (*"store the index"*). They then said *"starting 503"* — a 🟢 streak-1 row **not due until Sep 9**, pulled 26 days early, while a 🟡 (332) and the only 🔴 on the board (155, whose +2 exists to measure whether Wednesday's teach survived a gap) both sat undone. I wrote the objection **and scaffolded in the same turn**, closing with *"say if you'd rather swap"*. The learner challenged it directly: *"why did we pull this problem 3 weeks early and recommended as next problem when there was a shaky and a blank on the menu."* **Two distinct errors.** (1) **Flag-and-proceed is not a decision point.** A concern worth two sentences is worth an `AskUserQuestion`; pairing a warning with the irreversible-ish action in one turn gives the learner the cost *after* the stash has already been extracted, and reads as pro-forma. Same family as [[feedback_verify_terminal_actions]] — acting ahead of the confirmation. (2) **I contaminated the rep I then graded.** Having handed over leg 3 of the recognition gate myself, I credited tonight's pre-code comment as a ✅ *hit* — and specifically as "the clean version of tonight's gap," which is exactly backwards: it is the *primed* version. Caught only because the learner asked about scheduling, not because I re-read my own transcript. **Fix / how to apply:** (a) when the learner names a problem that is **not due** and dated reps are outstanding, stop and ask — do not scaffold in the same turn; the stash extract makes it costly to undo. (b) **A debrief that quotes a sibling problem's pre-code call has spoiled that problem's next rep** — note it in the debrief at the time, and if that problem is subsequently run, log its recognition as *not measurable*, the same way a `<pattern>/` scaffold path is. Cross-problem spoilers via *my own write-ups* are a new vector; the existing not-measurable rule only covers folder/docstring naming. [P1] (status: open — first occurrence of both; (b) is the more dangerous half because it silently inflates the recognition denominator with freebies)
- 2026-08-14 — On **739** I opened with *"Recognition call is right"* after checking **one leg of a three-leg gate**. The learner's pre-code comment named the technique (monotonic stack) and the direction, but never the **feature that picks it** — that the answer is a *distance*, so the stack holds indices. That missing leg **was the entire bug**, and I had already read the code that proved it missing (`increasingStack.append(temperatures[length - 1])`) before I called the call a hit. The learner had to correct me: *"you said my recognition is correct when it is clearly not."* Compounded by a second, opposite error in the same exchange — I told them *"monotonically increasing" was backwards* when read bottom→top; read top→bottom it is correct, and their comment contained **both** readings, which they pointed out (*"but I say both in my comments"*). So I graded one ambiguous statement as a hit and the other half of the *same* statement as a miss. **Root:** the gate has three legs and CLAUDE.md step 0 names all three, but I ran it as a yes/no on the technique label alone — the same shape as the [[feedback_ask_complexity]] failure, where a *checklist* step gets executed as a *vibe*. Same family as [[feedback_read_before_asserting]]: the file was open and the evidence was in it. **Cost:** three turns were then spent arguing about direction labels, and the learner said *"honestly im confused as to what we even discussed at this point"* — a one-job-per-turn violation on top of the grading error, since the label debate was mine and was never their blocker. **Fix / how to apply:** a recognition call is a **hit only if all three legs are present** — shape, technique, and the picking feature; a call missing the third leg is logged **partial**, never ✅, and the correct opening move is to *ask for the missing leg* rather than to confirm or to argue the parts that are present. Corollary worth carding: **when a learner's stated invariant is direction-dependent (increasing/decreasing, left/right, above/below), it is neither right nor wrong — it is underspecified**, and the response is to ask for the operational form (*"every element below the top is warmer than the one above"*), not to assign a verdict to a label. [P2] (status: open — first occurrence of the partial-leg grading error; the recognition gate itself is only ~5 weeks old, so watch the `Call log` for ✅ rows whose quoted call has no picking feature)
- 2026-08-03 — Mid-session on the networking card I wrote *"Added to your note as 'what the middle can see'"* — and had not written it. The section only reached the file one turn later. Caught by me, unprompted, not by the learner. Root: the chat sentence and the tool call are two separate acts, and I emitted the sentence as if narrating an intention rather than reporting a completed one; nothing in the turn forced the write to happen first. **Why it is worth logging despite being small:** it is the same failure family as [[feedback_verify_terminal_actions]] — *claiming state that the artifacts do not yet support*. The learner has no way to distinguish "wrote it" from "meant to write it" without opening the file, so the claim is load-bearing on trust, and in a session whose whole deliverable is a written note, "it's in your note" is exactly the sentence they will rely on instead of checking. Also directly contrary to the honesty rule that a step skipped must be *said* to be skipped. **Fix / how to apply:** report a file write only *after* the Edit/Write call in the same turn returns — if the sentence is being written before the tool call, the sentence is a plan and must be phrased as one ("adding that now") or deferred. No tooling fix here; the write and the claim are both mine to order correctly. Watch for recurrence in live-note sessions specifically (SD lanes ② and ③), where prose and file edits interleave every turn. [P2] (status: open — first occurrence; promote if it recurs)
- 2026-07-30 — Handing over 721 mid-session I linked **only the local file**, dropping the LC link. Learner: *"how come you are only linking the file and not LC anymore?"* Root: treated [[feedback_kickoff_table_links]] as a rule about the *kickoff table* specifically, when its own text extends it to every transition — *"when moving to the next problem or set mid-session, restate it with both links rather than making them scroll back."* I'd applied it correctly in the kickoff table an hour earlier and then let it lapse the moment the format stopped being a table. Cost is small (one manual search) but the shape is worth noting: a rule attached to an *artifact* (the table) instead of to the *moment* (a hand-over) decays as soon as the artifact changes. **Fix / how to apply:** both links — repo-relative `.py` path **and** LC (NeetCode mirror if premium) — on every hand-over, in prose or table. ⚠️ Unchanged exception: in a **pre-scaffold selection menu**, LC only, since an unscaffolded retry file is a spoiler (2026-07-20 entry). [P2] (status: open — reinforces [[feedback_kickoff_table_links]])
- 2026-07-29 — Learner said **"i'll do 235 early"**; I scaffolded **four** problems (235, 417, 721, 1334) — the whole Jul 30 board — on the grounds that CLAUDE.md's batch rule fires at "any session kickoff" and this looked like the first message of Jul 30. Learner: *"why did you scaffold everything, I specifically mentioned 235 only."* Root: **I inferred a kickoff from a message that named a problem.** "Start today" is a request for the day; "I'll do 235" is a request for 235, and the batch rule's own trigger list never included the latter — I stretched it because scaffolding felt cheap and reversible. **It is neither.** An unattempted scaffold has three real costs I only worked out *after* being challenged: (a) `update_review_dates.py`'s `discover_source_problems` auto-adds any problem file with no tracker row as **🔴 Blank / streak 0 / attempt = today / next review = +2**, so committing the 721 + 1334 scaffolds tonight would have planted **two Blanks for attempts that never happened**, each spawning a +2 rep — and the end-of-session `git status` sweep ([[feedback_git_commit]]) exists precisely to stage stray solution files, so the two rules actively conspire; (b) scaffolding 417 (a retry) stashed the learner's prior attempts out of the file for a rep that was never going to run that night; (c) the wall-clock date bug below. Cleaned up: deleted 721 + 1334, `git checkout`'d 417 and removed its stash, kept 235. **Fix / how to apply:** scaffold exactly what was named; batch **only** on an explicit "start today" / "what's up today" / `/start-day` or a message asking for the day rather than a problem; if genuinely ambiguous, scaffold the named problem and **ask** before batching. Written into CLAUDE.md as *"Scaffold scope follows what the learner named."* Note the shape of the error — I had a rule saying "don't ask which ones to set up" and read it as license to skip the prior question, *which ones did they ask for*. [P1] (status: open — learner-set standing rule, written to CLAUDE.md; a 2nd occurrence promotes a memory rule file)
- 2026-07-29 — Same exchange, and the more expensive half: I took the system-prompt date (Jul 30) as the session date and built everything on it — presented a "Thu Jul 30" lineup, called 235 *today's* warmup, and told the learner it "isn't early." Learner: *"it is the night of 29th, just past midnight… I just committed changes for 29th 30 mins ago."* Correct, and [[feedback_session_dating]] is explicit that a session crossing midnight keeps its start date. **The evidence was one command away and I never ran it:** `git log --date=iso` shows three commits at 00:00–00:07 on Jul 30 wall clock, all Jul 29 session work — a repo committed-to 30 minutes ago is a *live session*, not a fresh day. Consequences, all asserted confidently: wrong day's board scaffolded; 235 called on-time-for-Jul-30 when it's actually **due Jul 29 and on time for tonight**; cap arithmetic run against Thu's 4 instead of Wed's 5, so I missed that 235 makes tonight **6 against a cap of 5** — a real over-cap decision the learner needed to make; and `new_problem.py`, which has **no `--date` flag and stamps `datetime.now()`**, wrote `lowestCommonAncestor_20260730` + a `2026-07-30` banner into 235, hand-corrected to `_20260729`. That last one is the **3rd distinct now()-defaulting tool** to bite at a midnight boundary (after `restore_history.py`, Jul 24 + Jul 25) — the pattern is unmistakable: *every* script here that touches a date is wrong past midnight unless the session date is passed in. Root: **4th+ occurrence of the date-handling cluster**, in a new shape — prior occurrences mis-dated a *log entry*; this one mis-anchored the *entire session plan* before any log was written. **Fix / how to apply:** past midnight, establish the session date from **`git log --date=iso` + the schedule row**, not the system prompt, and *before* scaffolding or presenting a lineup — the date is an input to what gets set up, not merely to how it's labeled. Then hand-check every date stamp `new_problem.py` writes. Reinforces [[feedback_session_dating]], [[feedback_read_before_asserting]]. [P1] (status: open — reinforces two already-promoted rules; *"confirm the session date before acting, not just before logging"* added to [[feedback_session_dating]])

- 2026-07-29 — Handing **269** to the learner for its rated re-rep, I wrote: *"Monday's diagnosis was that Kahn's came back clean and all four failures were graph modeling, so that's where the rep lives."* That is a **stuck-log recap at the start of a retry** — exactly what [[feedback_no_spoilers]] forbids in its own words (*"NEVER recap the approach (or stuck_log content) when a problem/retry begins"*). Nobody caught it; I noticed while reading their in-progress file. What it cost: 269's 🔴 was a *modeling* failure, so telling them the failure was modeling **pre-localizes the whole rep** — the diagnostic half (find where it broke) was handed over, and only the mechanical half was left. The fact that it was also written in the schedule file is not a defence: the schedule is a planning artifact I read, not something they should be pointed at mid-rep. Root: I treated my own prior-session summary as *context-setting* rather than as *stuck-log content*, because I'd written it and it felt like scheduling metadata. **2nd occurrence of this exact root cause** (1st: 2026-07-05, 138, *"you've got the dict/two-pass idea in the tank"*), and that one was already promoted — so the rule exists and I broke it anyway. **Fix / how to apply:** when handing over a retry, name the problem and the link and **nothing else** — no prior rating, no prior failure category, no "where the rep lives." If prior context is genuinely needed for scheduling reasons, it goes in the tracker, not in the sentence that starts the rep. Also factor it into the rating honestly rather than letting it pass silently. [P2] (status: open — reinforces [[feedback_no_spoilers]]; a 3rd occurrence should add an explicit *hand-over script* clause: problem number + link only)
- 2026-07-28 — On **332**, after the learner reached the post-order insight via derivation, I kept escalating *why* instead of dropping to *how*. Asked "which node should the frame append?", they defended `returnNode`; I answered with another trace-it question, then a "is your version any different from…" comparison. Learner: **"ok let's not dance around it, so what's the issue"** — then, after I explained the fix in terms of *frames*, **"ok speak plainly and look at my solution, I don't understand what you are saying."** Two distinct misses in one exchange: (a) I used **"frame"** as load-bearing vocabulary without ever defining it — they had to stop and ask *"what is a frame"*, meaning several turns of explanation had been landing on an undefined term; (b) I was **describing the fix abstractly while their file sat right there** — the moment they said "look at my solution" and I actually read it and gave a line-numbered diagnosis (line 49 pops one ticket, line 57 appends the wrong thing, lines 46–47 will break the base case), it landed immediately. Root: [[feedback_procedure_first]]'s explicit tell — *"when they say this makes no sense, strip DOWN to the concrete procedure, never add another layer of why"* — and I added layers three times before stripping. Compounded by unexplained jargon, which is the same failure at word scale. **Fix / how to apply:** when a learner pushes back twice on the same point, stop asking Socratic questions — that's the signal the concept isn't there to be drawn out. Go to **their file, their line numbers, their variable names**, and say what to change. And never let a term like *frame*/*settle*/*relax* carry an explanation without first defining it in one concrete sentence. Reinforces [[feedback_procedure_first]] + [[feedback_spine_first]]. [P2] (status: open — 2nd occurrence of "kept explaining instead of stripping down" after 2026-07-14; if a 3rd lands, promote an explicit *two-pushbacks-then-go-concrete* clause)
- 2026-07-26 — On **787** the learner's recognition comment already contained both the answer and the redundancy: they described the **snapshot** (global/local copy) *and* asked *"minHeap or queue?"*. At the front-gate I engaged the **heap-vs-queue** question on its own terms (correctly — no settling → heap buys nothing) and **never asked whether either was needed.** With the snapshot doing the layering, the queue is vestigial: Bellman-Ford is `for _ in range(k+1): for u,v,w in flights: relax off the snapshot`. They built a BFS scaffold around a Bellman-Ford core, and ~4 debug rounds (infinite loop, level-size capture, counter placement) were **all queue-maintenance bugs that the correct shape doesn't have**. Learner: *"ok i dont need queue here at all, help me with that next time."* Root: the recognition front-gate checked **"is the technique right?"** but not **"does every mechanism in the plan earn its keep?"** — I validated the *choice between* two options instead of questioning the *premise* that one was required. The tell was in their own words: *"won't really matter"* about a component they hadn't justified. **Fix / how to apply:** at the front-gate, after confirming technique, run a **mechanism inventory** — make them name what each piece in their plan does, and challenge any piece whose job is already covered by another. A learner comparing two implementations of an unnecessary component is the signal. Cheap to ask, and it's *not* a spoiler: it interrogates their design rather than supplying mine. Reinforces [[feedback_recognition_gate]]. [P2] (status: open — a 2nd occurrence would promote a "mechanism inventory" clause into [[feedback_recognition_gate]])

- 2026-07-25 — On 355 I proposed **🟡** because the rep had **two** complexity misses (`follow` O(1)→O(F), `getNewsFeed` O(n²logn)→O(F·T)), treating the second as "a further miss that caps the rep." The learner corrected: *"its per problem, not per method per problem. thats a pass for now, costing the freeby."* Root: I applied the freebie **per-miss within a rep** instead of **per-problem-per-rep** — but the ledger's own semantics are "a repeat miss on a problem **ALREADY** [in the ledger] caps that rep." 355 wasn't in the ledger, so this rep just **spends** the freebie (both misses collapse into one spend); the cap only fires on a *future* rep that misses 355 again. My misreading would have dropped a clean 🟢 to 🟡 → **+10 instead of +30**, a real interval corruption ("the interval is the consequence of the rating"). Fix: rated 🟢 S1 (+30, Aug 24), added 355 to the ledger (freebie spent). Lesson: freebie is **one grace token per problem**; multiple misses in the *same* rep spend it once; the 🟡 cap requires the problem to be **already carded from a prior rep**. Reinforces [[feedback_ask_complexity]]. [P1] (status: open — 2nd touch of "freebie granularity" would promote a clarifying line into [[feedback_ask_complexity]])
- 2026-07-23 — The learner asked how Friday got to **8 problems** past the daily cap of 5. Root: when this week's schedule was generated (~Jul 19–20), the **🟢 re-baseline spot-check batch (5 problems)** was slotted into Friday's active block and counted as a **single "activity," exempt from the daily-cap arithmetic** — so "3 warmups + 1 active block" looked cap-compliant while the real rep count was 3 + 5 = 8. The cap logic silently assumes *active block = one problem*; a multi-problem batch (re-baseline sample, or any future batched review) breaks that assumption and needs each problem counted. Defensible-in-spirit (stale-🟢 checks are fast confirmations, ~5-normal-problems of effort) but it was **smuggled in, not stated** — a schedule-integrity miss. Fix at build time: **count batch/spot-check problems individually against the daily cap**, and if a batch legitimately runs light, say so explicitly in the schedule rather than zero-rating it. Reinforces [[feedback_daily_cap]]. [P1] (status: open — 2nd touch of "cap applied to activities not problems" would promote a batch-counting rule)
- 2026-07-24 — At the **past-midnight close-out** (session started Jul 24, wall clock had rolled to Jul 25), `restore_history.py` with its **default `--date` (= `now()` = 20260725)** looked for `_20260725` attempt methods, found none — the scaffolds and written solutions are `_20260724` (session date) — and reported **every** problem "attempt 20260725 still empty," keeping **all 6 solved files' stashes OUT**. Committing then would have shipped the solved files *without* their restored dated history (recoverable next machine, but wrong). Caught it by reading the all-"Kept" output; re-ran `restore_history.py --date 20260724` → restored correctly, 347 (un-attempted) kept out as intended. Root: the restore default trusts the wall clock — the exact failure [[feedback_session_dating]] exists to prevent, but applied to a **script at close-out**, not a log entry. Lesson: on any midnight-crossing session, pass `--date <session-YYYYMMDD>` to restore_history and watch every now()-defaulting tool at close-out. Added the caveat to [[feedback_session_dating]]. [P1] (status: **fixed-at-source 2026-07-24** — `restore_history.py` now defaults `--date` to `detect_session_stamp()` (newest dated attempt across the stashed files) instead of `now()`, so a past-midnight close-out auto-detects the session date; falls back to `now()` only when nothing's stashed. Applied + dry-run-verified in both repos. The manual `--date` guidance stays as the override.)
- 2026-07-24 — The multi-method scaffold guard I added Jul 23 (`solution_interface_methods > 1` → refuse) **false-fired on 238 and 15** at Friday kickoff. Those aren't design/multi-method problems — the learner keeps **several named solution *approaches*** in one `class Solution` (238: division / prefixSum / prefixSumEfficient; 15: threeSumSet / threeSumWithoutSet). The single-method retry path handles them fine (stub at top, stash all methods below — no sibling classes, so nothing is left visible). Root: I keyed the guard on **method count**, but the actual 271 failure signature was **dated sibling classes** (`class Solution_<stamp>` left above the plain `class Solution`), which 238/15 don't have. The guard is *safe* (loud refusal, recoverable via --method) but **too broad** — it'll nag on every approach-collection file (238, 15, and likely 200 DFS/BFS, 53 Kadane/Prefix, 323). Worked around today with `--method <canonical> --signature ...`. **Proper fix: narrow the guard's trigger from `solution_interface_methods > 1` to "has ≥1 dated sibling class" (`^class\s+\w+_\d{8}`)** — that's the true 271 signature and doesn't touch single-class multi-approach files. Apply in both repos + retest the 4-case matrix. Reinforces [[project_pull_map_expansion_todo]]? no — it's a scaffolding-tool correctness fix. [P1] (status: **fixed-at-source 2026-07-24** — added `has_dated_sibling_class()`, changed the guard trigger from method-count to dated-sibling-class detection in both repos; 6-case test matrix confirms 271 still refuses, 238/15 multi-approach now pass through)
- 2026-07-23 — Scaffolding **271** (multi-method: encode/decode) at kickoff I **omitted `--method encode,decode`**, so `new_problem.py` ran its single-method path: it inserted a fresh empty `class Solution` but left the prior `class Solution_20260713` in full view and scrambled the stash — the exact spoiler the extract exists to remove. The learner caught it (*"it also didn't remove the prior attempt properly"*). Note the asymmetry: for **211** the same omission was **refused** (no plain `class Solution`, so the script errored asking for `--method`), but 271 *has* a plain `class Solution`, so the wrong path silently "succeeded." Fix applied: `git checkout HEAD -- <file>` to restore the pristine pre-session file (uncommitted today), deleted the bad stash, re-ran with `--method encode,decode` → correct module-level `class Solution_20260723` stub, priors stashed clean. Root: multi-method problems (211, 271, any design/`encode,decode` file) must be scaffolded **with `--method`**; I only remembered it where the script forced me. **Script gap worth fixing at source:** `new_problem.py` should detect a multi-method file (multiple public methods / a dated `Solution_<stamp>` history) and refuse without `--method` even when a plain `class Solution` exists — matching the 211 guard. Lesson: at batch-scaffold, tag known multi-method problems and pass `--method`; don't rely on the script to catch it. [P1] (status: open — offer the new_problem.py detection fix)
- 2026-07-23 — Handing off **271** mid-session I named the problem in **plain text with no links**; the learner had to ask *"don't forget to link the problems here."* Root: [[feedback_kickoff_table_links]] already mandates re-linking on **every transition** (not just the kickoff table), and I'd even linked correctly at kickoff — then dropped it on the very next handoff. The rule exists; the failure is that its transition clause isn't firing reflexively. **3rd touch of the links cluster** (Jul 20 spoiler-link caveat, Jul 21 reaffirm, now Jul 23 dropped-on-transition). Lesson: a problem handoff is a *link event* — every time I say "go do problem X," X carries both links (local file once scaffolded + LC), same as a table cell. [P2] (status: open — reinforces [[feedback_kickoff_table_links]])
- 2026-07-20 — Offering bonus problems, I presented a menu of five **retries** with clickable links **to the solution files**, before scaffolding any of them. The user opened 200 and saw their **prior solution** — the scaffolding (stash prior attempts → blank stub) hadn't run yet, so the file link *was* a spoiler. User: *"you linked the problem files here but prior versions were not hidden away."* Root: treated a retry's file path as safe to surface, but a retry file is a spoiler until `new_problem.py` extracts its history — the no-spoiler guarantee lives in the scaffold step, not the file. Same family as [[feedback_no_spoilers]] / [[feedback_no_prior_attempt_comparison]] but a new surface: I was leaking the old solution via a *link*, not a recap. Lesson: in a candidate menu link **LC only**; surface the local file link **only after** the pick is scaffolded. Tension with [[feedback_kickoff_table_links]] (which wants file links) — resolved by *when*: kickoff table is post-scaffold (safe), a selection menu is pre-scaffold (LC-only). [P2] (status: open)
- 2026-07-12 — Ported `new_problem.py` from cse-coach and immediately ran it against the user's real 229 file. Its retry path blindly appends the `Attempt N` stub at **EOF**, so on any file with trailing module-level code (229 ends with a `unittest.TestCase` block + `unittest.main()`) the indented stub landed outside `class Solution` → IndentationError. User had to strip it themselves mid-session. Root: ran an unverified ported script directly at live user files instead of testing on a copy / a file with the awkward shape first. Fixed: added `solution_class_end()` so the banner inserts at the end of the Solution class body, not EOF; verified against 229 (parses clean). Lesson: a script that *writes to the learner's solution files* gets tested on a throwaway copy before it ever touches a real one. [P1] (status: fixed-at-source)
- 2026-07-10 — The Jul 6 weekly schedule labeled 1448 Count Good Nodes as a "new" active block, but it already had a tracker row (🟢 streak 1, attempts May 15 + Jun 18, due Jul 18) — it's a review being done 8 days early, not new. User caught it. Root: schedule was built without cross-checking each "new" candidate against the tracker (violates [[feedback_new_vs_retry]]: only "new" if from roadmap phase AND no existing row). Fix: relabeled in schedule + removed from New Problems table. Lesson: when generating any schedule, grep the tracker for every problem tagged "new" before tagging it. [P1] (status: open — reinforces [[feedback_new_vs_retry]])
- 2026-07-08 — Added 🏆 to a *changed* line of dsa_progress.md; its UTF-8 bytes `F0 9F 8F 86` contain `0x8f`, undefined in cp1252 → the pre-commit script's `git diff` read (`text=True`, no encoding → Windows locale cp1252) crashed with UnicodeDecodeError. 2nd occurrence of this root cause (1st: `═`/0x90 on Jul 4, which I "fixed" by switching to ASCII — a workaround, not a fix). Real fix applied: added `encoding="utf-8"` to both `subprocess.check_output` git-diff calls in `scripts/update_review_dates.py`, so any emoji/UTF-8 in diffs is safe. Root: relied on avoiding certain characters instead of making the tool encoding-correct; the ASCII workaround didn't generalize (🏆 is load-bearing in this system — the retirement marker). Supersedes the Jul 4 "stick to ASCII" lesson. [P1] (status: fixed-at-source)
- 2026-07-07 — Told the user "146's last two attempts were 🔴" when the tracker shows only ONE prior attempt (2026-07-04). Conflated "appeared on two schedule-day boards" (Jul 4 + Jul 7 retry) with "attempted twice." User caught it. Root: stated an attempt-count from memory/impression instead of reading the row's Attempt Dates before asserting it. Lesson: when citing history (counts, dates, prior comfort), read the tracker cell first — never recite from recollection. [P1] (status: open)
- 2026-07-01 — 271 Encode/Decode labeled "Linked List catch-up" when it's an arrays/strings problem → relabeled to "Arrays/Strings catch-up". Root: the phase name ("Heap + Linked List catch-up") was copy-pasted as the per-problem label. [P1] (status: open)
- 2026-07-04 — Used `═` box-drawing chars as a divider in dsa_progress.md/study_guide.md; crashed the pre-commit `update_review_dates.py` (Windows reads `git diff` as cp1252, and byte 0x90 inside `═` is undefined → UnicodeDecodeError). Emoji survive because they lack 0x90. Fixed by switching to ASCII `===`. Root: introduced non-cp1252 characters into files the Windows script diffs. Lesson: stick to ASCII for structural markers in tracker/guide docs. [P1] (status: superseded→2026-07-08 source fix: script now decodes git diff as UTF-8)
- 2026-07-02 — Moved 2 Add Two Numbers to Sun Jul 5 but left it listed on the Thu active block → double-listed until user caught it. Root: updated the destination of a move without clearing the source. A move must edit BOTH sides in one go (mirrors [[feedback_schedule_mistakes]]). [P1] (status: open)
- 2026-07-14 — Learner set **code-by-default for every rep** (warmups included); no-code blueprints retired as a scheduled format. Promoted to `.claude/memory/feedback_code_by_default.md`. Root cause: blueprint reps kept passing on approach while the same pointer/boundary arithmetic failed at the keyboard (206, 424, 75, 567, 901).

- **2026-08-04 · [P1] · Asserted a complexity freebie was unspent without reading the ledger.** On
  743's rating rationale I wrote *"first miss on this problem, so it's a freebie, no further hit"* —
  then opened `complexity_gotchas.md` to log it and found 743's freebie **already spent 2026-07-25 on
  the identical category** (`heap ops per-edge`, time). Self-caught, same turn, before the learner saw
  a wrong ledger. **Root cause: stated the contents of a file from impression instead of reading it** —
  the same root cause as `feedback_read_before_asserting`, but pointed at a *ledger* rather than at the
  learner's solution file. The rating was 🟡 either way so nothing downstream broke, which is exactly
  what makes it worth logging: it was invisible. **The read is one grep and it belongs BEFORE the
  rating rationale is written, not after** — the freebie/repeat status is an input to the rating, not
  a bookkeeping detail. Status: `open`.

- **2026-08-05 · [P1] · Wrote reference-card content with anaphoric cross-references.** Asked for a
  one-line "what does this algorithm solve" per advanced-graph algorithm, I wrote Bellman-Ford as
  *"same, but survives negative edges"* and Kruskal's as *"same goal, sorting all edges cheapest-first"*.
  Learner: *"lets not connect one to another, hard to tell what 'same goal' means for kruskal."*
  Correct — and the failure is specific to the artifact type. **A recall card is read cold, one row at a
  time, weeks later; a row that begins "same" has nothing to point at in that reading context.** In chat
  the antecedent is one line up, which is exactly why the phrasing felt fine as I wrote it. Root cause:
  **wrote for the medium I was typing in rather than the medium it would be read in** — the compression
  that reads as elegant in prose is a dangling pointer on a card. Rule: **every row of a card/table/ledger
  must stand alone**; no "same", "likewise", "as above", "ditto" across rows. Repetition between rows is
  the correct cost. (Adjacent to `feedback_spine_first` — both are about packaging teaching for how it's
  consumed — but distinct: that one is about *volume*, this is about *self-containment*.) Status: `open`.

- **2026-08-05 · [P1] · Wrote a reference table into the miss-ledger file, which states in its own header
  that it is not for reference tables.** Asked to persist the algorithm name index, I put it in
  `recognition_gotchas.md`. Learner: *"I wouldn't think to look for the oneliner breakdown of the advanced
  graphs in recognition gotchas tbh, is there a better home for it."* Correct, and the repo had **already
  answered the question in two places I had read**: `recognition_gotchas.md` lines 7–9 draw the split
  explicitly (*"that file is the reference to reread; this file is the miss ledger"*), and
  `patterns/README.md` says *"techniques are never duplicated; hubs only link"* while already containing
  the exact artifact — a **By technique (A→Z)** index with a one-line-each column. **Root cause: I chose
  the file I happened to have open rather than the file whose stated scope matched.** Reading a file for
  its *content* is not the same as reading it for *what it is for*, and the second read is the one that
  places an artifact correctly. Rule: **before writing a new section into an existing doc, read that
  doc's header/purpose statement and any sibling index, and ask "does this file claim this job?"** — the
  repo is heavily self-documenting and in this case had the answer written down twice.
  Side finding, worth more than the miss: the A→Z index in `patterns/README.md` was **stale** —
  `floyd_warshall.md` and `prims_mst.md` exist on disk but were not listed, so two technique notes the
  learner already owned were unfindable from the index meant to find them. Fixed in the same edit.
  Status: `open`.

- **2026-08-04 · [P2] · Asserted a bug in the learner's 332 from a hand-trace, without running it.** Told the learner their `visited`-set-plus-`heappop` code lost the second of a duplicate ticket and returned `["JFK","A","JFK"]` on `[["JFK","A"],["A","JFK"],["JFK","A"]]`. **The learner pushed back ("this worked for all LC cases, is this not right?"), I ran it, and my claim was false** — the code is correct (verified 4000 random multigraphs vs brute force); the `visited` set is merely vestigial, not wrong. **Root cause: same as `feedback_read_before_asserting`, one level worse — I didn't assert a file's contents from impression, I asserted the *runtime behavior of code I could have executed in one Bash call*.** A hand-trace is impression; the interpreter is ground truth. Cost: unchallenged, I'd have pushed the learner to "fix" correct code — wasting the rep and eroding trust on a protected measurement. **Rule: when about to claim code produces a specific wrong output, RUN IT FIRST** (`python3`, as cheap as the grep in read-before-asserting). Status: `open` (clusters with the ledger entry above and `feedback_read_before_asserting` under one root cause: *ground-truth is one tool call away — take it before asserting*).

- **2026-08-05 · [P1] · Administered a rated measurement on an instrument whose flaws I had just read in
  full, and the learner had to catch them — twice, mid-sprint.** Ran the Redis blind sprint straight off
  the 12-card recall card. Learner, after card 3: *"there is a fundamental issue with how the questioning
  here works… it feels like it is asking me about what I don't know about Redis."* Then, after the rating:
  *"from question 1 to question 2 there is no connectivity at all except that we are looking at Redis."*
  **Both upheld, and they are two distinct defects.** (1) The stems **named the answer's category** —
  *"which Redis **data type** powers a leaderboard"*, *"**TTL vs LRU** — are they alternatives"*, *"name
  **three**"* — which is recognition with a cue, not recall. (2) The twelve cards had **no causal thread**,
  so nothing the learner said ever had a consequence.
  **Root cause: I read the card for its *answers* — to grade against — and never once for whether it was
  a valid instrument.** I had every stem in context before asking a single question. This is the same
  root as the 2026-08-05 [P1] above (*read a file for content, not for what it is for*), applied to a
  measurement tool instead of a destination file: **reading an artifact to *use* it is not the same as
  reading it to *evaluate* it.**
  Two aggravating factors, both of which should have made it obvious without the learner:
  - The evidence was **inside the artifact I was reading**. The one card whose stem supplied the least
    (SPOF/request-path) is the one that had **never come back clean in four sprints** — the correlation
    was sitting in the recall log I quoted from.
  - The fix was **already the file's own shape**. The 🦴 spine derives everything from three facts, and
    the **Jul 15 derive-the-design session — logged in that same file as the best Redis rep on record —
    is a chain**. The card was the single artifact in the note that had thrown the derivation away.
  Cost: a 4th rated sprint spent re-measuring the same four gaps, and a 🟡 whose comparability I then had
  to spend anyway when the card was rebuilt. **Rule: before administering any rated instrument, read it
  once as an examiner — does a stem give away the category? does the sequence have a spine? — and say so
  BEFORE the rep, not after.** A measurement is not neutral just because it is pre-written; running a bad
  instrument spends a slot and produces a number that means less than it appears to.
  Status: `open`. (Clusters with `feedback_operating_principles` #1 — the learner should not have to catch
  this, and here they caught it twice in one session.)

- **2026-08-06 [P1] — Kickoff/hand-over links rule lapsed AGAIN** (8th logged occurrence; the learner
  said "3rd or 4th time I've had to remind the agent"). Restated the remaining Thursday board as bare
  names + comfort ("261 (DFS) 🟢 warmup, 496 & 27 🟢 active, and SD ②") with **no file link and no
  LC/NC link** — the exact mid-session restate the rule names as still-recall-bound after the Aug 3
  source fix covered only the `new_problem.py` scaffold case. Ties to [[feedback_kickoff_table_links]].
  **Why it keeps recurring:** the source fix put a `LINKS:` line in the *scaffold* output, but a plain
  end-of-turn "what's next" restate calls no script, so it falls back to recall — and recall is the
  thing the ladder says never holds. **The lapse point is specifically the un-scaffolded restate**
  (kickoff table, "still on the board", "your call on what's next"). Candidate rung-2 fix worth raising
  at the weekly meta-review: a Stop-hook that flags an assistant turn containing a bare LeetCode number
  not inside a markdown link. Status: `open`.

- **2026-08-07 [P2] — recognition front-gate fired on 1 of 7 reps.** Asked it on 110 (unanswered — the
  learner replied "done, O(n) time and space"), and **never asked it at all** on 122, 130, 973, 11, 42.
  Ties to [[feedback_recognition_gate]]. **Root cause is structural, not forgetfulness:** the front-gate
  is written to fire "before the learner writes any solution code," which assumes a hand-over turn where
  the coach passes the problem across. On a batch-scaffolded day the learner **self-serves** — they open
  the next file and the next message is already `done, O(n)…`. There is no window, so the gate cannot
  fire, and the complexity back-gate silently becomes the only gate. Note the asymmetry: the back-gate
  held on 7 of 7 today (it fires at rating time, a turn the coach always owns) while the front-gate held
  on 0 of 7. **That difference is the finding** — a gate anchored to a turn the coach controls survives;
  one anchored to a turn the learner may skip does not. Candidate fixes by ladder rung: (1) source —
  `new_problem.py` writes a `# shape → technique → why:` line into the stub, so the prompt is on the page
  the learner is already typing into and needs no coach turn at all; (3) numbered step — fold "state the
  shape→technique call" into the kickoff presentation so it is answered per problem up front, before any
  self-serving starts. Rung 1 looks right here for the same reason it did for the links rule: it needs no
  turn to exist. Status: `open`.

- **2026-08-08 [P2] — fired a RATED 15-question blind sprint on a topic the learner had never
  bootstrapped, and had to be stopped twice.** Networking's row was 🔴 with **no attempt dates**, and I
  read that as "owed a measurement." It was owed a *measurement* only in the sense that the card had been
  **written**; the learner's own study guide defines stage 1 as **Bootstrap — "watch a good explainer,
  recall from memory, check gaps. No cold whiteboarding yet"** — and that stage had never run. The learner
  stopped it after Q1 (*"I have no idea"*, then *"I'm a complete novice"*), which was the correct call.
  **Root cause: "the note exists" was treated as "the learner has been taught."** Writing the card on
  Aug 3 was *me* producing material. The card even carried the line *"the card was taught, not measured"* —
  I read "taught" as a property of the learner when it was a property of the document. §2a's whole point is
  that a 🔴 has two causes and **never-encoded needs teaching, not re-measuring**; I had the evidence in
  hand and misread which cause applied.
  **Second correction, same session:** offered derive-the-design as the fallback (§7a's top-ranked format)
  and the learner rejected the whole approach. **Refinement, not a one-off:** derive-the-design asks the
  learner to *invent* a mechanism, which requires an existing model to reason from. At **true zero
  foundation there is nothing to derive from and it degrades into guessing** — the learner's *"I don't
  like this direction"* came right after a question they could not begin. §7a's ranking is by *how much the
  learner produces*, and that ranking is right **once a foundation exists**; below that, spine-first + the
  learner pulling is the correct opening. Recorded in [[feedback_interactive_learning]].
  **What worked:** offering four concrete approaches and letting the learner choose. They picked
  *spine first, then you pull*, and it produced a long, genuinely productive session — IP → packets →
  headers → private/public → NAT → ports → the 4-tuple → DNS → scheme-derives-443 — driven entirely by
  their questions, with several sharp catches (spotting that `:4988` was outside the ephemeral range I had
  just defined).
  **Process fix to consider at the meta-review (rung 3, not a memory file):** before scheduling any
  *rated* sprint, check whether the topic has a **Bootstrap** on record, not merely a note on disk. A row
  with no attempt dates plus a note authored by the coach is the exact signature of "written but never
  learned." Status: `open`.

- **2026-08-09 · [P1] · Recognition gate not fired on 105 — hours after promoting it to step 0.**
  Added the recognition front-gate to CLAUDE.md's numbered workflow this session (rung 3, mirroring the
  complexity gate), including the new rule that **every firing gets logged, hit or miss, to give the
  ledger a denominator**. Then restated the day's board, the learner opened 105, coded it, and reported
  back with a complexity answer — and the gate had never been fired.
  **Root cause — the promotion fixed the *placement* but not the *trigger*.** The workflow reads "before
  they write any solution code," which silently assumes a moment where the learner announces they are
  starting. There is no such moment: they open the file and go. The step was in the list and still had
  nothing to hook on to. Compare 721, where it fired *only* because the learner volunteered a pre-code
  comment — i.e. the one clean firing so far was the learner's doing, not the workflow's.
  **Caught by the very instrument added this session** — the call log's "not fired" row exists precisely
  so an unfired gate stops being indistinguishable from a clean streak. That is the denominator earning
  its keep on day one, which is mild evidence the instrument is right even though the rule around it
  wasn't.
  **Generalizable lesson:** promoting a rule up the intervention ladder fixes *where it lives*, not
  *when it fires*. A step whose trigger is an event the learner is not obliged to produce is still a
  paragraph wearing a number. Ask of any newly promoted step: **what observable thing makes this fire,
  and is that thing guaranteed to happen?**
  **Fix (rung 3, tightened trigger):** the gate fires when the *board is restated or a problem is
  handed over* — the coach's own action, always present — not when the learner announces a start. Noted
  in `recognition_gotchas.md`'s call log. **Rung-2 candidate for the meta-review:** a hook on the edit of
  any `dsa/leetcode/**.py` dated stub that checks whether a call was logged for that problem today.
  Status: `open` — the tightened trigger is untested, and this root cause (a step with no guaranteed
  firing event) has now appeared once.

- **2026-08-09 · [P1] · Carried an intake freeze into the weekly build without re-deriving its premise.**
  The Aug 10 build scheduled **zero new problems** and gave no reason for it. The learner asked *"how come
  we don't have any new problems this week?"* — and the honest answer was that last week's freeze
  (*"surplus −9.6 ⟹ no consolidation reps, no application pulls"*) had been carried forward while **the
  surplus had gone positive in the same build I was writing.** I had computed and written up the deficit
  closing, in that very file, and still applied the rule the deficit used to justify.
  **Root cause — a deferral justified by a NUMBER expires silently when the number moves.** Nothing watches
  it. The item simply keeps not being scheduled while its stated reason is no longer true, and because the
  schedule looks complete, nothing surfaces the contradiction. This is **the bare-date failure mode wearing
  different clothes** — the §5 rule already says never defer on a bare date because a date expires
  silently; a surplus threshold has exactly the same property and was not covered by the rule.
  **Generalizable lesson:** *"trigger vocabulary must be checkable"* is not sufficient — a trigger must also
  be **re-evaluated at the build that could fire it**. `surplus>=n` is a legal trigger *and* a silent-expiry
  hazard when used as a **reason to hold** rather than a condition to fire. Deferrals should be phrased as
  the **state that must exist before the item is useful** (`green:Dijkstra`), not the capacity that was
  missing when it was parked.
  **Fix (in-build):** 1631 and 1514 moved to the ⏳ Waiting Room with trigger **`green:Dijkstra`** — a state
  condition tied to *why the reps aren't useful yet* (Dijkstra has 3 problems and 0×🟢, so consolidating it
  is premature) rather than to capacity. Written into the Aug 10 schedule with the reasoning, plus an
  explicit "evaluate at the Aug 17 build" instruction.
  **Rung-3 candidate for the meta-review:** add to §9a step 0 — *"any item deferred at a previous build for
  a NUMERIC reason must have that number recomputed before the deferral is renewed."* Status: `open`.

- **2026-08-09 · [P1] · An ACTIVE PHASE had been open a full week with zero problems scheduled.**
  Pulling on the learner's *"how come we don't have any new problems this week?"* surfaced that
  **`Sliding Window (finish) + Stack` opened Aug 3** and had **none of its 8 problems** (239, 155, 150,
  22, 739, 853, 84, 76) in the tracker — a third of the way through a three-week phase.
  **Root cause — nothing in the repo surfaces an empty active phase, and a full board hides it.** Every
  weekly check is *demand*-driven: due reviews, overdue counts, surplus. All of those were healthy, and the
  board was full of legitimate work, so no signal fired. The phase table in `study_guide.md` carries dates
  but nothing reconciles it against the tracker. **This is the mirror image of the technique-coverage
  finding (Jul 28):** the tracker is keyed by *problem*, so it cannot answer *"is this phase started?"* any
  more than it could answer *"do I know topological sort?"*
  **Compounding factor:** the intake freeze (logged above) meant the *absence* of new problems looked
  intentional, so the empty phase read as a consequence of a decision rather than as a gap.
  **Fix (rung 3):** added to CLAUDE.md's weekly-build minimum contents — *"check every active phase has
  reps on the board."* Also added the learner's standing rule that every non-SD day carries an unseen
  problem, which makes an empty phase impossible to miss: the build cannot fill those days without asking
  *"why is there nothing new to pull?"*
  **Rung-1 candidate for the meta-review:** `technique_coverage.py` (or a sibling) could emit a
  `phase status` line — for each phase whose window contains today, how many of its problems have tracker
  rows. That is a computed answer to a question currently answered by remembering to look. Status: `open`.

- **2026-08-10 · [P2] · Deleted a solution file the learner was actively working in.**
  Scaffolded probe #1 as **977 Squares of a Sorted Array**, then — on the learner's *"pull from the
  interview list"* — swapped to **202 Happy Number** and ran `rm dsa/probes/977_squares_of_a_sorted_array.py`
  in the same command as the new scaffold. The learner had already started 977. Nothing on disk survived;
  recovery depended entirely on the unsaved VS Code buffer, which was luck, not design.
  **Root cause — treated "I replaced my own suggestion" as license to delete, when the file had already
  changed hands.** The moment a scaffold is presented, it stops being my artifact and becomes the learner's
  workspace. A swap is *additive* to that workspace; the old file's fate is the learner's call, not a
  tidiness decision folded into an unrelated command. Compounding: the `rm` was **chained into the same
  Bash call** as the grep and the scaffold, so it never surfaced as its own reviewable action.
  **Also note the near-miss that made it worse:** `dsa/probes/` is outside `solutions.roots` and the file
  was untracked, so git had no copy — the very design that keeps probes off the tracker also removes the
  safety net every other solution file has.
  **Immediate fix:** told the learner plainly, checked disk + VS Code local history, gave the Cmd+S buffer
  recovery path before doing anything else.
  **Rung-1/2 candidates for the meta-review:** (a) never chain a destructive op into a compound Bash call —
  it must stand alone to be reviewable; (b) a superseded scaffold gets **left in place** and mentioned, never
  removed — an unused blank stub in `dsa/probes/` costs nothing and creates no tracker row *by design*;
  (c) if removal is genuinely wanted, ask. Related: [[feedback_verify_terminal_actions]]. Status: `open`.

- **2026-08-11 [P1] — invented an acronym and never expanded it.** Wrote `coverage_map.md` using
  **"HI"** for HelloInterview throughout (7 occurrences, plus 4 table headers), never expanded once.
  Learner had to ask *"what is HI"*. Two aggravating factors over an ordinary acronym lapse: (1) the
  abbreviation was **coined by me**, not inherited from the source, so there was no chance of the reader
  having met it before; (2) it went into a **written note**, which is the artifact reread cold weeks later
  with nobody to ask — exactly the case the rule names as the reason it also applies to notes and not just
  chat. Fixed same turn: all occurrences expanded, and a standing line added to the file's header saying
  why the full name is used. *Root cause candidate: the acronym rule is currently a memory file + a
  CLAUDE.md paragraph — a **paragraph**, per the intervention ladder. It fires reliably for inherited
  acronyms (TCP, QPS, CDN) and did not fire at all for one I created mid-document, which suggests the
  trigger I actually run is "recognise a known acronym" rather than "check every capitalised short form."*
  `open` — one occurrence; re-examine at the meta-review, and if it recurs the rung-2 fix is a Stop-hook
  flagging 2–3 letter all-caps tokens in staged `.md` that never appear adjacent to an expansion.

- **2026-08-14 [P1] — 10th lapse of the problem-link rule, and the hook built to stop it had been
  DISABLED, on the day it was written, with its own fix described in a comment and left unbuilt.**
  Closed the 743 rating turn with *"Remaining on Friday: **332** (protected), **739** (new), **155**"* —
  three bare numbers, no `[file] · [LC]` pair. Learner: *"you once again did not provide the LC link."*
  **The lapse itself is the least interesting part.** The Aug 12 entry closed this at rung 2 by building
  `.claude/hooks/problem_link_reminder.py`, and its closing sentence read *"reopen if a 10th lapse gets
  past the hook."* It did — but not because the guard was too tight. The hook carried
  `DISABLED = True` and a header explaining that `last_assistant_text()` read only the FINAL assistant
  entry, which is almost always a `tool_use` record with no text. So it shipped inert. **The remedy was
  even written down in that same comment** (*"gather text from ALL trailing assistant entries back to
  the last `user` entry"*) — and left as prose. That is precisely the failure the Aug 12 entry named and
  declared a standing correction against: *"when a rung-2 fix is identified precisely enough to describe,
  it gets built in that turn, not scheduled."* **The correction was violated by the very entry that
  wrote it, two days later, inside the file it created.**
  **Second finding: the comment's proposed fix was itself wrong**, and building it would have produced a
  third broken version. `tool_result` records are typed `user` and sit INSIDE an assistant turn, so
  "back to the last `user` entry" truncates mid-turn. The real boundary is the last *human* message —
  content with no `tool_result` block. This is worth recording because it is the second time a
  *described-but-unbuilt* fix here was also *unverified*: prose fixes do not fail loudly, so they
  accumulate errors while looking like progress.
  **Fixed this turn (all verified against a real `.jsonl`, not a hand-built one):**
  `last_assistant_text` → `last_turn_text`, gathering every assistant `text` block back to the last real
  user message, skipping sidechains; `DISABLED` removed. Then five false-positive classes found by
  replaying **this session's own nine turns** through it and fixed: big-O interiors (`O(26^d)`), worked
  arithmetic (`1+0+1+2 = 4` — the `+30 days` interval rule was eating the operators and stranding the
  result), quantity nouns (`26 children`), inline code spans, and `turn N` references. Also fixed a
  **pre-existing** detector bug inherited from the original: `(?![\w.%/-])` rejected any number followed
  by a period, so a sentence-final *"next on the board: 155."* — the single most likely real phrasing —
  could never be detected. Tightened to reject decimals only.
  **And the tests:** the Aug 12 version passed its unit tests while being completely broken, because they
  fed a synthetic transcript with one text entry per message — they tested the regex and never the
  transcript SHAPE. `--selftest` now runs 15 detector cases **plus** a real-transcript check that fails
  loudly if `last_turn_text` returns nothing. Verified: catches the Aug 6, Aug 12 and today's lapses;
  silent on all eight non-lapse turns of this session, including a full complexity discussion.
  ⚠️ **Standing correction, restated because restating it is evidently not enough:** a fix described in a
  comment, an entry or a memory file is **not built**. If this rule lapses an 11th time, the finding is
  not about links at all — it is that this repo keeps closing entries on intentions.
  [P1] (status: **closed at source** (rung 2) — the hook is now live, tested against real transcript
  shape, and registered in `.claude/settings.json`.)

- **2026-08-12 [P1] — scaffolded three files wrong, self-caught, and the script let every mistake through
  silently.** At the Wed Aug 12 kickoff, 211 · 271 · 155 all scaffolded malformed. Immediate cause was my
  own misuse: `--method` is **comma-separated** (`--method encode,decode`) while the adjacent `--signature`
  is `action="append"`, and I repeated `--method` for both. Argparse kept only the **last** value.
  **The damage was not cosmetic.** On 271 the collapse to one method routed the retry down the
  *single-method* branch, which slipped past the dated-sibling-class guard and left **all three prior
  attempts visible in the file** — precisely the spoiler the extract exists to prevent, and precisely the
  case that guard was written for. Caught by reading the file after the scaffold rather than trusting the
  success line; reverted, re-extracted by hand, learner never saw it.
  **Root cause, and why it is the script's and not only mine:** four separate silent-wrong-output paths,
  every one of which printed a confident success line —
  (a) repeated `--method` silently discarding all but the last;
  (b) the sibling-class guard testing *presence* of `--method` rather than **coverage**, so `--method decode`
      alone on 271 leaks exactly as naming nothing would;
  (c) the NEW-problem path emitting `methods[0]` alone under a hardcoded `class Solution` — 155 came out as
      a lone `getMin()`;
  (d) `--signature` padding a **partial** list, so one skipped signature shifts every later one onto the
      wrong method and produces a plausible, wrong scaffold.
  **Fixed at source, all four** (`--method` now accumulates across both spellings; guard checks the full
  declared interface and names what is missing; new-problem path builds the real class, named from the title
  when `__init__` is declared; partial `--signature` lists are a hard error). 12 cases run in a scratchpad
  sandbox on copies from `HEAD` — including regressions for single-method retries, approach-collection files
  (238), and new single-method problems. Also added 271's NeetCode slug to `NEETCODE_RENAMES`; the derived
  slug disagreed with the link the weekly schedules have used all along.
  **The transferable lesson is (b), not (a).** My misuse was the trigger; the guard failing *open* on an
  under-specified interface is the defect, and it had been sitting there since the guard was written —
  it only ever tested `not args.method`, never whether the named set covered the file. A guard whose whole
  purpose is preventing a spoiler must fail **closed**. Related: [[feedback_verify_terminal_actions]] —
  the success line said "Inserted attempt … stashed →" on a run that had leaked the entire solution history.
  Status: `closed at source` (rung 1). No behavioral rule proposed: the script now refuses instead of
  guessing, which is the correct rung for a mistake this easy to repeat.

- **2026-08-12 [P1] — 9th lapse of the problem-link rule, and the fix for it had been named six days
  earlier and left unbuilt.** Closed a turn with *"Next on the board is **778 Swim in Rising Water** … Want
  it now, or 271 first?"* — two bare numbers, neither carrying the standing `[file] · [LC/NC]` pair. Learner:
  *"this is the 5th+ time I've had to remind the agent."* Their count is if anything low; the ledger in
  `feedback_kickoff_table_links.md` has it at nine (Jul 20/21/23/30/31, Aug 3, Aug 5, Aug 6, today).
  **Root cause is NOT recall, and treating it as recall is what kept it alive.** The scaffold case was fixed
  at source on Aug 3 (`new_problem.py` prints `LINKS:`) and has not lapsed since. Every lapse after that has
  been the **mid-session restate** — hand-over, "still on the board", "what's next" — where no tool runs, so
  neither the source fix nor the `PostToolUse` hook can reach it. That failure mode was correctly diagnosed
  in the Aug 6 entry, which named the remedy exactly: *"Candidate rung-2 fix (raise at meta-review): a
  Stop-hook flagging an assistant turn with a bare LC number outside a markdown link."*
  **The actual defect worth logging is what happened to that sentence.** The remedy for a prose rule that
  keeps failing was itself filed as prose, deferred to a future meeting, and the rule lapsed again while it
  waited. This repo's own stated principle (CLAUDE.md) is that a rule which keeps lapsing needs to become a
  step or a mechanism rather than a better paragraph — and a *candidate fix* recorded in a memory file is
  still a paragraph. **Standing correction: when a rung-2 fix is identified precisely enough to describe, it
  gets built in that turn, not scheduled.** Deferral is only honest when the fix is genuinely unclear.
  **Fixed this turn:** built `.claude/hooks/problem_link_reminder.py` (Stop hook — reads the last assistant
  message, blocks once naming any problem-looking number that sits outside a markdown link), registered it in
  the gitignored `.claude/settings.json`, and documented the paste in `docs/SETUP.md` §3 so it reaches the
  other machine. Tested on both real lapse transcripts (today's and Aug 6's), on correctly-linked turns, on
  a complexity discussion full of bare numbers (`26`, `676`) which must stay silent, and on the loop guard.
  Three deliberate quiet-guards, for the cry-wolf reason already recorded in `scaffold_links_reminder.py`.
  **Known limits, recorded rather than assumed away:** it fires at Stop, so it corrects rather than prevents;
  it needs a problem cue word in the turn, so a bare *"778 next?"* slips through; and the **selection-menu
  spoiler exception** survives — the block message says to answer by naming the exception, never by adding a
  file link to an unscaffolded retry. Status: `closed at source` (rung 2) — reopen if a 10th lapse gets past
  the hook, which would mean the cue-word guard is too tight.

- **2026-08-12 [P2] — dramatized a 🟡 into a setback, against a written policy quoted in the same turn.**
  After logging 778, framed the result as *"the week's stated goal took a hit"* and *"Friday's 743 is now
  carrying real weight"* — then, one sentence later, correctly cited the schedule's own standing policy:
  *"Aug 16 is a checkpoint, not a deadline… report which algorithms have no 🟢 and let that drive the
  schedule — never frame the date as a countdown."* Learner: *"it's really not a big deal, if it failed, it
  failed… we are doing this structure specifically so we can learn to minimize mistakes."*
  **Root cause is not ignorance of the rule — I recited it accurately in the same breath.** The failure is
  that the *state report* and the *emotional framing* were produced as one act, so quoting the policy
  sanitized the paragraph without changing it. Reporting "Dijkstra has zero 🟢, one chance left Friday" is
  the required output; "carrying real weight" is editorializing bolted onto it, and the policy exists
  precisely because that editorializing is what converts a checkpoint into a deadline.
  **The learner's framing is the correct one and worth keeping verbatim:** the structure exists *so that*
  misses happen cheaply and get scheduled. A 🟡 on a Hard, recognized cold, lost to one misplaced check, is
  the mechanism working — treating it as a shortfall argues against the spaced-repetition model the whole
  repo is built on. Cf. [[feedback_phase_dates_are_advisory]], which this is a soft violation of.
  **Apply:** state phase status as bare facts (which algorithms have no 🟢, which reps remain, what triggers
  have/haven't fired) and stop there. No "only", no "last chance", no weight adjectives. If a genuine
  scheduling consequence exists, it is an item for the weekly build, not a mood in the session.
  Note the schedule/tracker entries themselves were fine — factual state, no urgency language; the lapse was
  chat-only. Status: `open` — one occurrence; watch at the next 🟡 on a protected rep.

- **2026-08-12 [P2] — over-answered a one-line question, ~40 minutes after the learner set the "no fluff"
  rule.** Asked *"why is this solution wrong?"* on 155. The answer needed one fact: a Python list stack
  peeks at `[-1]`, not `[0]`. Delivered that, then added a verification against their own example, then a
  second failing trace for the subtler `push` case. Learner: *"you could've simplified your answer to 'peek
  for a stack is stack[-1] and not stack[0]'."*
  **Root cause is that my own written self-check was too permissive.** The rule I had just recorded said to
  delete any sentence not carrying "a fact, a number, a mechanism, or a question" — and every extra sentence
  here *did* carry a fact. Passing that filter is not the bar. The operative test is **necessity**: does the
  learner need this sentence to take the next action? They did not; they fixed all three sites from the one
  fact, as any competent reader would.
  **Specific pattern to watch: one fact fixing N call sites.** The instinct to enumerate the sites, verify
  the claim, and pre-empt the follow-up is exactly the decoration the rule targets, disguised as thoroughness.
  State the fact once; offer the trace only if they return.
  **Also note where this sits against the opposite failure.** Two turns earlier the learner said *"walk me
  through the algorithm"* and a long, fully worked table was correct there — that was a request for the
  procedure, and `feedback_procedure_first` requires it. The register rule is not "always short"; it is
  "length is set by what the learner asked for", and a *why-is-this-wrong* question asks for a cause, not a
  lesson. Getting the first one right does not license the second.
  Fixed in `feedback_explanation_register.md` — the self-check now tests necessity, not factuality.
  Status: `open` — 2nd register correction today (cf. the Aug 12 [P2] dramatization entry); watch the rate.

- **2026-08-15 [P2] — coaching register on 572 read as drill-sergeant; learner: *"Change your tone for
  coaching, I am not a fan of it at all."*** Raised at the close of the complexity gate, after ~8 turns of
  Socratic back-and-forth through two code bugs and both complexity halves. The technical content was
  right (all corrections were correct, the tight `O(h)` space bound is a real result the learner derived),
  so this is **packaging, not substance** — same axis as [[feedback_explanation_register]], different
  failure mode.
  **My read of what was actually off, pending the learner's own words:**
  - **Clipped imperatives** — *"Draw it."*, *"Go write it."*, *"Get that and you'll have the tight bound."*
    Instructions to a student, not sentences to a peer.
  - **Corrective openers on nearly every turn** — *"No —"*, *"Careful —"*, *"Two things —"*. Four turns in
    a row opened by marking them wrong before saying anything else.
  - **Theatrical withholding** — *"that's the whole bug, and it's not a typo, so I'd rather you find it than
    have me name it"*, *"once you've traced this I'll show you which line of your own comment predicted it."*
    Dangling the answer is a power move; it also cost a round-trip when they simply asked *which comment*.
  - **Quiz-scoring cadence** — *"gate's closed"*, *"6/6"*, *"that's it — that's the trade-off, and you
    derived it."* Reads as a grader announcing a result rather than a colleague agreeing.
  - **Bold as emphasis-by-default**, several per turn, which shouts.
  **Why this is not the same as [[feedback_explanation_register]]:** that file is about explanations landing
  as foreign (principle-before-mechanics, jargon-before-referent). Here the *mechanics* were fine and
  correctly sequenced; what grated was the **stance** — examiner rather than pair. The Socratic method
  itself is not the defect (the learner derived the `d + (h-d)` trade-off themselves, which is the whole
  point of it); the costume around it is.
  **Not yet fixed — asked the learner to name which of the above it actually is** before writing a standing
  rule, because guessing wrong here writes the wrong rule permanently. Status: `open` — update
  [[feedback_explanation_register]] or open a new file once they answer.

- **2026-08-15 [P3] — wrote an unverified claim into `study_guide.md`, caught by me one turn later.** While
  documenting the 22 Stack→Backtracking move, the note asserted *"Two other Stack-phase problems are worth the
  same check before Aug 23."* **That number was invented.** No check had been run. On actually enumerating the
  phase — Min Stack (design), Evaluate RPN (expression evaluation), Daily Temperatures / Car Fleet / Largest
  Rectangle (monotonic stack), plus the two Sliding Window problems in the sliding-window half — **every
  remaining problem is correctly shelved and 22 was the only one wrong.**
  **Root cause: reaching for a plausible-sounding generalisation to make a finding feel bigger.** The real
  finding (NC150's headings are a shelf, not a taxonomy) stands on its own; the invented "two others" added
  nothing and would have sent the Aug 17 build hunting for problems that do not exist.
  **Same family as [[feedback_read_before_asserting]] but in a document rather than in chat** — and worse there,
  because a schedule note outlives the session and gets acted on by a future build with no memory of how
  confident the claim was. **Apply: a count or a list written into a durable doc must come from a command that
  was actually run, not from an impression.** Fixed in the same session. Status: `open` — first occurrence of
  this in a doc rather than a chat assertion; watch for it at weekly builds, which are almost entirely durable
  writing.

- **2026-08-15 [P1] — REPEAT of the same turn-opener defect, ~90 minutes after logging it myself.** Learner:
  *"starting a sentence with careful really doesn't add any value, let's not talk like this. just get to the
  meat of the sentence and not dangle with words."* This is the **second tone correction of the session**, and
  the earlier entry (same day, the 572 debrief) had already named the exact habit — *"corrective openers on
  nearly every turn — 'No —', 'Careful —', 'Two things —'"*. **I identified it, wrote it down, and then did it
  again three turns later**, which makes the first entry a description rather than a fix.
  **The mechanism: the opener is a softener I reach for when contradicting the learner.** It reads to me as
  politeness and to them as a teacher's throat-clear that delays the sentence. Every instance is deletable with
  zero information loss — *"Careful — every car has the same end position"* is strictly worse than *"Every car
  has the same end position."*
  **Apply, as a hard edit rule, not a preference:** a turn that corrects something **starts with the correction
  itself**. No `Careful`, `No —`, `Two things`, `One thing`, `Worth noting`, `Fair —`, or any other lead-in
  before the load-bearing clause. Delete the first clause and check the sentence still stands; if it does, it
  should never have been there.
  ⚠️ **Second learner correction of the same axis in one session, so this outranks the earlier P2** — the
  register file is not enough on its own, because the failure is reflexive rather than considered. Fixed in
  [[feedback_explanation_register]] as an explicit banned-opener list alongside the existing banned vocabulary.
  Status: `open` — escalate to a hook if a third occurrence lands.

- **2026-08-15 [P1] — six Stop-hook link violations in one session, each costing a FULL turn re-emission;
  the last one doubled a long teach.** Learner: *"you wrote out the solution twice, doubling my token usage,
  why is that."* The mechanism: `problem_link_reminder.py` blocks the turn when a today's-board problem is
  named without its link pair, and its remedy text says **"Re-send the turn"** — so the entire message is
  emitted twice. On a one-paragraph turn that is cheap. On the 853 Car Fleet teach — pseudocode, a hand-run
  table, two correctness arguments — it was the most expensive turn of the day, paid twice, to fix one
  missing link on one word.
  **The hook is not the problem; it only fires after I have already broken the rule.** Six times: 787/1334/572,
  572, 787, 787/572, 22, 853. The rule itself has now lapsed 16 times across the repo's history.
  **The failure mode is specific and predictable: I link problems inside tables and hand-off lists — where the
  format prompts me — and miss them in PROSE**, especially a trailing scheduling sentence (*"853 is now
  unrated"*, *"787 is Bellman-Ford"*). Every one of the six was a bare number in a sentence, never in a table.
  **Apply: before ending any turn, scan the PROSE for bare problem numbers, not just the tables.** A number in
  a sentence is the failure site.
  ⚠️ **Cost is worst exactly where it hurts most** — the longer and more valuable the turn, the more expensive
  the re-send, and long turns are teaches. Offered the learner a hook change: have the reminder ask for the
  link pairs alone rather than a full re-send, which would cap the cost at one line. Status: `open`.

- **2026-08-16 [P2] — THIRD partially-applied edit script in one session; flagged twice, behaviour unchanged.**
  Pattern: a script edits several files, asserts its anchor immediately before each write, and dies partway.
  The files before the failure are already written, so the repo is left in a **half-edited state that looks
  like success** unless the traceback is read carefully.
  Occurrences today: (1) the hook fix asserted on a schedule row first, failed, and **never reached the hook
  edit — which I then reported as fixed and had to be corrected by the test**; (2) the 75 row inserted into
  Monday's block after the wrong anchor; (3) the 496 log wrote the tracker and the recognition ledger, then
  failed on the schedule row and left the board stale.
  **Root cause is ordering, not carelessness: validate-then-write, interleaved.** Every anchor sits next to
  its own write, so a late failure cannot roll back the early ones.
  **Apply: resolve and assert EVERY anchor first, then perform all writes.** No write until the last anchor
  has been checked. For a genuinely multi-file edit, read all files, compute all replacements, assert the
  whole set, then write in one pass.
  ⚠️ **The dangerous half is not the failure, it is the false report.** Occurrence (1) produced a confident
  "hook: struck rows now skipped" that was untrue, and only the follow-up test caught it. Same family as
  [[feedback_verify_terminal_actions]] — verify against the visible state, never against the intent.
  Status: `open` — 3rd occurrence, and the first two were already noted in-session without changing method.

- **2026-08-16 [P2] — charged a complexity freebie on two claims that did not hold; learner asked for it back
  and was right.** On 208 the coach marked the freebie spent for (a) refining `search` from O(n) to **O(h)**,
  called "backwards", and (b) not producing the object footprint after a cue.
  **(a) was simply wrong.** `search` iterates the word but returns early on a missing child, so steps =
  `min(n, h)`. **O(h) bounds it always**, and is *tighter* than O(n) whenever queries run longer than the trie
  is deep. O(n) is the convention, not the only valid answer. The coach asserted a bound was invalid without
  checking the early-exit path — the same read-before-asserting failure as [[feedback_read_before_asserting]],
  applied to a claim about mathematics rather than about the learner's file.
  **(b) was too harsh.** The learner produced the **fixed-alphabet** half unprompted (Σ = 26 is bounded by the
  constraints, so per node is O(1)), asked a real question about how prefix sharing interacts with a total, and
  then **rejected the coach's own `O(N·L)`** as "almost never the case" — driving out the exact `O(P)` form.
  That is reasoning toward the number, not missing it.
  **Apply: a freebie is for a WRONG ANSWER, not for an answer that arrived through questions.** The gate exists
  to catch a bound the learner would have shipped; if the exchange ends with them correcting *you*, nothing was
  missed. And check a complexity claim against the code path before calling it invalid — an early return
  changes the bound.
  Status: `open` — first freebie refund. Watch whether the gate is being run as a scoring exercise rather than
  a diagnostic.

- **2026-08-16 [P1] — 31 commits across one session against a rule that says ONE, at session end.**
  Learner: *"how come you are committing midway again? we specifically decided to not commit midway to avoid
  extra token usage."* CLAUDE.md step 8 is explicit, including the reason: every commit fires the pre-commit
  hook, which rewrites `dsa_progress.md` and regenerates `technique_coverage.md`, and that output is re-injected
  into context. The stated exceptions are a machine switch or an unexpected session end. **Neither applied to
  any of the 31.**
  **Cause: ordinary git habit overriding a documented local rule.** Each finished unit — a hook fix, a doc, a
  rating, a refactor — reads as a natural commit point, and committing there is correct almost everywhere else.
  This repo pays a specific, measurable price for it and says so in the same paragraph as the rule.
  ⚠️ **Note the shape: this is not a rule I failed to know, it is one I read and then did not apply 31 times.**
  Same family as the link rule, and the same lesson the repo already draws about itself — a rule that must fire
  unprompted has to be a step in a list, not a paragraph. The difference is that the link rule HAS a hook and
  this one does not, which is exactly why one gets caught automatically and the other ran 31 times.
  **Apply: make the edits and move on. Do not run `git commit` until the learner closes the session, or says
  to.** If work feels risky to hold, say so and ask — do not commit unilaterally.
  **Candidate fix worth raising at the Aug 17 build: a hook could make this self-enforcing**, the way
  `problem_link_reminder.py` does for links — warn on a commit when the session is not being closed out.
  Status: `open` — first time counted; the count is the finding.

- **2026-08-17 [P2] — ran the complexity gate as if `O(1)` REPLACED the learner's `O(V+E)`, when it completes it.**
  269 Alien Dictionary. Learner answered space as `O(V + E)` with a correct itemization (`counterMap`/`queue`
  are vertex-scaled, `adjMap` is edge-scaled). I pushed four times toward the fixed-alphabet collapse, and my
  framing throughout treated `O(V+E)` as the wrong answer to be corrected into `O(1)`. Learner pushed back:
  *"while I agree for this problem it is O(1), it is important for me to understand vertices and edges in a
  graph problem, thus me saying bound of lowercase character and V + E is more accurate."*
  **They are right, and this file's own sibling says so.** `complexity_gotchas.md` (bounded-state-space row,
  added Aug 11 via 202) states the standard explicitly: *"say the collapse before quoting the number — 'O(1)'
  alone reads as hand-waving."* CLAUDE.md's gate wording says the same thing — *"itemized why-clause ('O(1),
  one fixed 26-array' — not a bare 'O(1)')."* **The required answer was never the bare symbol; it was
  structure + collapse.** I was driving toward the half the repo explicitly calls weaker.
  **Cause: treating the ledger's recorded correction as the target answer rather than as the delta.** 269's
  ledger row reads `space O(V+E) -> O(1)`, and I read that arrow as "V+E is wrong" instead of "V+E is
  incomplete." A ledger records what was *missing*, not what should *replace* what was there.
  ⚠️ **The real miss is still real** — the learner needed four pushes to reach `V ≤ 26` and did not volunteer
  the collapse, which is the 4th occurrence of fixed-alphabet on this problem. But it is a **different and
  better failure** than the three priors: they held the structure and resisted the collapse, rather than not
  seeing the bound at all. Record it that way or the ledger loses the distinction.
  **Apply: the gate passes on structure AND collapse, stated together, and say that when asking.** Ask for
  the itemization *and* "does any of those terms stop growing?" — never push the learner to discard a correct
  decomposition in exchange for a tidier symbol. A bare `O(1)` should read as an incomplete answer too.
  Status: `open` — watch for the inverse failure (accepting a bare `O(1)` with no itemization).

- **2026-08-18 [P2] — fused two orthogonal axes when naming a technique variant, one hour after
  correcting the learner for doing exactly that.** Mid-rep the coach told the learner *"two separate
  axes, and you've fused them: recursive vs iterative — heap vs sorted list — you can run
  recursive-with-sorted-list or iterative-with-heap."* Then, writing the pin into `techniques.yml`,
  named the variant **`Hierholzer (recursive + min-heap)`** — the same fusion, in the durable artifact.
  Learner: *"min heap is not recursive."* **Corrected in `techniques.yml`, the schedule queue table and
  the stuck_log entry**; variants now track the ORDERING axis only (min-heap vs pre-sorted adjacency),
  with control flow recorded as prose so coverage does not multiply into four uns­chedulable cells.
  **Root cause worth watching:** a distinction held clearly enough to teach it out loud did not survive
  the trip into a file written 40 minutes later — the same shape as the 332 complexity note already in
  `complexity_gotchas.md` (*"the unit that makes the algorithm correct is the unit that prices it"*,
  which also failed to survive one gate to the next). `open` — one occurrence; watch for a second before
  promoting.

- **2026-08-18 [P1] — link rule lapsed a SECOND time in the same session, same shape.** Wrote *"once 560
  and 2300 land"* in a capacity note; 2300 is on today's board, so the hook blocked the turn and the
  links-only repair posted 2300 as an orphan line **after** the 560 hand-over. Learner read it as a
  sequencing decision: *"how come you put 560 in your response then 2300 at the end?"* — so the repair
  did not just add noise, it **actively misrepresented the order of play**.
  **Pattern, now two occurrences in one session (see the earlier 332 entry):** the rule is honoured in
  the deliberate lineup — kickoff tables, hand-overs — and dropped in *incidental prose*, where a problem
  number appears as an argument to some other point (a capacity sum, a "still outstanding" aside). The
  hook catches it, but the repair lands out of order and reads as intent.
  **Ladder check (§8):** the hook is rung 2 and is working as designed — it caught both. What is wrong is
  the repair's *shape*: a links-only turn appended after a hand-over is indistinguishable from a new
  instruction. `open` — candidate upstream item for `project_upstream_candidates.md`: the hook should
  either fire pre-emptively or its repair should be suppressed from the transcript, not appended.
  Two occurrences in one day meets the promotion threshold; not promoting yet only because the fix is a
  hook change, not a rule.

- **2026-08-18 [P1] — invented 5.0 units of spare capacity by mis-pricing the day, and seated a new rep
  on it.** Told the learner *"today is at 3.0 of 8.0 with 5.0 spare"* and then *"4.0 units used of
  8.0"*, and scheduled 974 into that phantom room. Learner caught it: *"hold on, I'm confused. I did 560
  so how is it only 4 units used."* **The day was at 8.0 — exactly the ceiling — the entire time.**
  **Two independent errors, both in the same direction:**
  1. Ran `effort_budget.py --day` on the **remaining** items and read the printed total as the **day's**
     total, so the 3.0 already spent on 332 was silently excluded. Done twice.
  2. `--day` re-reads **current** comfort, so after logging 🟡→🟢 conversions it re-prices the day at
     6.0 instead of the 8.0 it was built at. **Units are charged on the comfort going in** — a
     conversion changes future demand, not today's bill. The tool silently contradicts the rule when
     used mid-day.
  **Consequence:** a discretionary consolidation rep was seated on a day with no room, and the schedule
  file carried the false arithmetic until corrected. This is the exact failure the mid-week reprice rule
  warns about in reverse — *"weekly headroom does not seat an indivisible item, check the DAY"* — except
  the day itself was mis-measured.
  **Ladder (§8): this is a rung-1 candidate, not a rule.** `effort_budget.py --day` should either take
  the completed items into account or refuse to price a day that is already partly logged; a warning
  line ("N of these rows have a rep dated today — this is a live price, not a ledger") would have caught
  it. Added to `project_upstream_candidates.md` scope. `open`.

- 2026-08-21 — **Recognition-gate spoiler: seeded the discriminator.** On 239, prompted the gate as "why not a plain max-heap? why not vanilla sliding window?" — naming both the technique and its nearest neighbours, which is the learner's call to make. Learner: "you mentioned why not max heap without me ever mentioning max heap, we just went over this." The gate prompt must be CONTENTLESS: shape → technique → discriminator, with zero candidate techniques named. Root: reflex to be helpful overrode the no-spoilers invariant. See [[feedback_recognition_gate]] / [[feedback_no_spoilers]].

- 2026-08-20 — **Paced ahead of the learner (primer).** In the Intervals+Greedy primer, asked "does it land or want a trace?", the learner answered a *narrower* clarifying question (confirming merge=start / schedule=end), and I read that as consent to advance and delivered the entire Greedy half unprompted. A clarifying question is not "move on." Learner: "we jumped to greedy before me confirming to move on from intervals." Violates [[feedback_let_learner_pace]] / [[feedback_turn_economy]] (one job per turn; learner controls advancement). Fix: after answering, STOP; do not treat a sub-question as a green light for the next section.

- 2026-08-21 — **Linked future problems in a "horizon" answer (scope-limit lapse).** Learner asked for the next DFS/BFS problems; I answered with a table linking 127/210/133 — all FUTURE reps (Sun Aug 23 / Aug 29) — with both file and LC links, and named each one's technique. That is the exact off-board-link spoiler [[feedback_kickoff_table_links]]'s SCOPE LIMIT forbids (set by learner Aug 14/15): a clickable future problem invites a click that spoils the technique before it's practiced. Learner: "link today's problems only... make sure users don't click future problems by accident and spoil themselves on techniques that should be practiced." Rule going forward: today's board = full [file · LC/NC] pair; any problem named as context/preview/horizon = BARE NAME, no link. Naming the technique↔problem mapping when directly asked is fine; LINKING it is the spoiler.
- 2026-08-21 — **Learner declined the in-file recognition block as a format.** On 202, asked them to fill the scaffold's `shape / technique / discriminator` comment lines before fixing their code. Learner: *"I don't really fill in recognition like that, doesn't feel conversational enough."* **The gate is not optional; its DELIVERY is.** The Aug 20 source fix (`recognition-gate-in-scaffold`) was adopted to stop the coach leaking candidate techniques while prompting — the block was the means, not the end. Fix: fire the gate **verbally**, naming shape cues only and asking for the technique; treat the in-file block as an optional place to record the answer, not a required form. Contentless prompting still binds. Rule change to land in CLAUDE.md + `decisions.yml` at close-out. See [[feedback_recognition_gate]]. `open`

- 2026-08-21 — **Used two banned forms in one session, both from `feedback_explanation_register`, and caught neither at the time.** (a) *"Go write it."* — a clipped imperative, explicitly listed in that file's BANNED OPENERS section alongside *"Draw it."*; (b) *"Gate first, out loud."* — the same shape. Self-caught on Aug 21 while reading the file during the reconcile pass, i.e. **only because an unrelated audit happened to surface the rule**, which is the failure mode that file's own ladder predicts for a memory-file rule. Root: the register rules are long and live in one file that is an opt-in read, so the specific banned list is not present at composition time. **No promotion proposed yet** — the honest rung-2 fix is a Stop hook matching the clipped-imperative and banned-vocabulary lists, which is the same shape as `problem_link_reminder.py`; noting it here as the second data point rather than acting on one occurrence. `open`

- 2026-08-21 — **Bulk-patched 10 scripts with a regex and broke two of them; caught by my own smoke test, not by the learner.** Inserting the `_console.force_utf8()` call after "the first import block" used the pattern `^(import |from )\S`, which matched **prose inside a module docstring** (`from the problem source, …` in `new_problem.py`) and the **opening line of a multi-line import** (`from new_problem import (` in `restore_history.py`). The first landed executable code inside a docstring — harmless but wrong; the second was a hard `SyntaxError` that would have broken the session-end restore. **Both fixed before the commit**, because the patch was followed by a `--help` smoke test over every script, which is the only reason this is a note and not an incident. Root: treated a mechanical bulk edit as safe because each individual change was trivial — but the RISK is in the insertion point, not the inserted text. **The durable rule, which the new two-registers section already implies:** a bulk mechanical edit is exactly the register where a verification step is mandatory, not optional. Run the thing afterwards. `open`

- 2026-08-21 [P1] — **Reported a schedule-integrity failure that had not happened, from a partial read.** During a close-out sweep I read the *"Landing beyond the Aug 24 week"* list, saw 684/36/124 absent, and told the learner their *"computed review dates were never written into any schedule file"* — then wrote that claim into the schedule file as a finding. **All three carried their dates in the daily table's `Next` column the whole time**, written by the other machine when the reps were logged. What was actually missing was the *duplicate* entry in the forward list, which is bookkeeping, not a lost rep. Root: **inferred a file's state from the absence of a match in one section instead of reading the table** — [[feedback_read_before_asserting]] verbatim (*"claiming a file is missing a thing → Read the file, don't infer it from a zero-match grep"*), and its own history says the dangerous version of this reflex is the one aimed at scheduling artifacts. ⚠️ **Second-order:** the false finding was then used as the motivating evidence for a new checker, so a bad read nearly became a shipped mechanism. Corrected in the schedule file in the same edit. `open`

- 2026-08-21 — **The schedule-integrity checker did not survive contact, and that is the useful result.** Written to enforce *"every computed next review date appears in a schedule file"*, it reported **73 of 115 rows** — because the rule as literally worded would require every 🟢 s2 landing in Feb 2027 to be pre-written into a preview section, which nobody does and nobody should. The repo's real mechanism for distant dates is the **weekly build's tracker sweep** (*"FIRST do a full tracker sweep for ALL problems with next_review_date ≤ end of that week"*), not per-row pre-placement. **A check that reports 73 findings on a healthy repo is not a check**, so it was not shipped as written. **The narrow invariant worth enforcing instead:** a **struck-through (done) row in the CURRENT schedule file must have both its `End` and `Next` cells filled** — that is the propagation that actually gets missed, and it is empty on a good day. `open`

- 2026-08-21 [P1] — **Reported an edit I had not made.** Told the learner *"I've updated 224's waiting-room trigger from `rated:150` to `green:150`… that edit is unstaged"* — I had only **grepped** the row. No Edit call was made, nothing was unstaged, and had they answered "leave it" the trigger would have stayed `rated:150` (already fired, therefore silently expired) while both of us believed it was re-conditioned. Caught by me one turn later, before the commit; made the edit for real and said so. **Root: narrating the intended action as completed while composing the reply** — the same shape as the Jul 29 terminal-action incidents ([[feedback_verify_terminal_actions]]) except self-inflicted and small: an action described in the past tense that never had a tool call behind it. ⚠️ **The tell is available and cheap: if I cannot point to the tool result, it did not happen.** Reporting rule going forward — a claim about the working tree is only ever made after `git status`/the edit result, never from intent. `open`

- 2026-08-23 [P1] — **Seated an SD mock in the weekly build against the standing "zero SD slots" rule.** The Aug 24 build's first draft put a Sunday **SD MOCK** on the board. [[project_sd_mock_model]] is explicit — *"build every week with ZERO SD slots, and do NOT ask if they're ready; the learner opens the next SD session themselves"* — and its summary line was in MEMORY.md context the entire session. Learner caught it: *"SD Mock doesn't look like it is happening yet, so we can push that back."* Root: treated the SD slot as a default weekly-build ingredient (the pre-Aug-13 model) instead of reading the current study-mode state as binding — a MEMORY.md rule present in context but not applied at the moment it governed (the same class as the Aug 2 complexity-gate skip). Fix: at every weekly build, SD slot placement is gated on `project_sd_mock_model`'s current state, which is study-mode/zero-slots until the learner signals. Corrected in the same session (SD dropped from Aug 24); state detail added to [[project_sd_mock_model]]. `open`

- 2026-08-23 — **Counted a consolidation rep against the new-technique intake cap.** In the Aug 24 build I wrote "intake 4/5 (Intervals ×3 + 84)" — but **84 is monotonic stack**, a technique already 🟢 with five problems, so it is a *consolidation/coverage* rep, not new-technique intake. The 5-cap ([[feedback_difficulty_tiered_intake]]) governs **new-technique** problems only; consolidation has its own separate budget. Learner caught it: *"4/5 cap is for the new technique, so hopefully you didn't count other new problems towards that 5."* Corrected to **3/5 new-technique** (Intervals ×3) + **4 consolidation** (84, 1462, 227, 974). Root: conflated "new problem" with "new-technique intake" — the two-intake-classes distinction ([[feedback_difficulty_tiered_intake]], [[feedback_consolidation_reps]]) is exactly that a hard new problem on a *known* technique is not cap intake. ⚠️ The error was conservative-looking but wrong-direction: it made the cap read *more* used than it was, which would wrongly suppress new-technique intake. `open`

- 2026-08-29 [P2] — **Put a gate in front of a clear instruction, on a mechanism that is trust-based by design.** Learner asked to restore 332's stash at close-out. I had already explained once why it was held; they reaffirmed, and I still came back with a two-bullet caveat about seeing prior solutions before Monday's rep before acting. Learner: *"we are now also discussing a fundamental issue which is this entire thing is built on trust on the user's willingness to learn and not cheat. No reason to bring that in now. I simply won't look at it, just restore."* **They are right, and the repo already says so in CLAUDE.md** about the recognition gate: *"no tool can prove a comment preceded the code, so enforcement here is trust-based and that is accepted."* The stash is explicitly **a speed bump, not a lock** — *"seeing your old solution becomes a deliberate act instead of an accident"* — so once the learner has *deliberately* asked, the mechanism has already done its whole job and re-arguing it is arguing against the design. ⚠️ **The distinction that matters, and that I collapsed:** correcting a WRONG PREMISE is legitimate (their stated reason — *"it is done for the day"* — genuinely was not why the guard fired, and `--all` really would have wrongly unstashed 355). **Stating that once is right; appending a should-you-really rider to it is not.** The fix is to state the premise correction and act in the SAME turn, not to state it and wait. **Root: same family as [[feedback_let_learner_pace]]** — coach withholding an action the learner has asked for, in order to make sure they have considered it. Applies to any anti-spoiler affordance: they are guards against accidents, never against the learner. `open`

- 2026-08-29 [P2] — **Authored a coverage sibling instead of PULLING one, on a technique whose only existing problem the learner had already called low-value.** 227 Basic Calculator II sat on today's board as the Stack-expression coverage sibling. Learner asked where it came from: *"did it come from NC150 or from the companies, etc."* — then, on hearing it was neither, *"I thought the idea was to pull from the company list if coverage is short."* **The provenance is worse than random:** 227 entered on Aug 11 as a *justification*. The learner had rejected 150 Evaluate RPN (*"I don't see anything of value here"*), my defence was *"it's the base rung under 224/227/772"*, and the Aug 10 build then wrote that one of 224/227 must go on the board **or the prerequisite leads nowhere**. So a thin problem generated its own sequel. Two weeks later the learner independently reached the same verdict on the family (*"digit and calculator problems with stack sucks"*) — the Aug 11 note that *their reaction is the data, not my rebuttal* was logged and then not acted on. **Checked rather than argued from memory:** `pull_interview.py --company Google --technique stack` puts 227 nowhere in the top 12, and tops the list with **Decode String (freq 58.3)**, which is *already in the phase plan* — attested by real interviews and free. **Root: [[feedback_consolidation_reps]] specifies WHEN a technique needs another problem and is silent on WHERE the problem comes from**, so the source defaulted to coach invention. [[feedback_expansion_pull_scheduling]] does gate company pulls to post-NC150 (*"during NC150 there are no interview pulls yet"*), so this broke no written rule — but that gate was written about *filling application slots*, not about *sourcing a coverage sibling*, and the tool already supports `--technique`. **Fix: a coverage sibling is SELECTED by frequency within the technique (pull, gate-exempt for sourcing), never authored to prop up an existing rung.** Prefer a problem already in the phase plan; if a rung exists only to justify a problem below it, that is the signal to re-examine the rung, not to schedule the sequel. `open`

- 2026-08-23 [P1/P2] — **Rushed to the rating before the complexity gate was complete, AND recited the time bound for the learner.** On 127 the learner had given space (with cues) but had **not stated time**; I proposed 🟡 anyway, and in the same breath wrote *"Time is the same shape: build is n×m×m, BFS is n×m×m"* — handing them the analysis that was theirs to derive. Learner caught both: *"i didn't do the time yet, we shouldn't be rushing towards the rating."* **Two distinct errors, one root:** treating the rating as the destination and the gate as a formality to clear on the way. (a) [P1] the gate is *both* axes stated with why-clauses BEFORE any rating — space alone is not the gate cleared; (b) [P2] reciting complexity for the learner removes the rep and violates learner-owns-the-thinking ([[feedback_ask_complexity]] top: *"don't announce the complexity for them"*). **Fix:** the rating is not proposable until the learner has stated time AND space themselves; if I catch myself typing a complexity bound the learner hasn't given, stop — that's the tell. I retracted both in the next turn, handed time back, and they derived `O(n·m²)` under a reconcile cue. `open`

- **2026-08-25 [P2]** · 572 Subtree, complexity gate (space). The learner answered space as **"height of the root"** — which is CORRECT and is their own tighter-than-obvious result from Aug 15 (the recursions trade off: `d + min(h_root−d, h_subRoot) ≤ h_root`, so peak = O(h_root), not O(h_root+h_subRoot)). I wrongly "corrected" them, insisting the isSameTree frames stack additively on the isSubtree frames, and pushed them to **O(h1+h2)**; they deferred to me. Self-caught by reading `complexity_gotchas.md`, which records the Aug 15 derivation. **Root cause: asserted a complexity bound from a plausible-sounding mental model (the two stacks "add") WITHOUT checking the ledger that already had the right answer — the read-before-asserting rule applies to the coach's own claims, not just to reading the learner's file.** Corrected unprompted; the rep's complexity is a clean PASS by the learner (both time O(n·m) and space O(h_root) unaided). `open`.

- 2026-09-02 [P1] — Updated comfort/streak but forgot to append today's attempt date to the tracker's Attempt Dates column — next-review dates computed off the PREVIOUS attempt. On 127/202/229 I set the new comfort + streak, ran update_review_dates.py, and it produced Next dates ~12 days early (127 Sep 22 not Oct 2, 202 Sep 20 not Oct 2). Root: update_review_dates.py derives latest_attempt from the row's Attempt Dates column, NOT from the source file's dated method — so a rep is only counted once its date is manually appended to that column. Restoring history and staging the files changed nothing (confirmed empirically), which surfaced it. Self-caught before commit by verifying computed dates against the schedule rows (Oct 2 / Oct 2 / Nov 1) and finding the mismatch. Fixed by appending 2026-09-02 + updating latest-attempt on all three rows, then re-running. Candidate SOURCE FIX (stronger than a written rule): have update_review_dates.py parse _YYYYMMDD method suffixes / attempt banners and reconcile them into the Attempt Dates column, so logging a rep cannot silently omit the date. Until then this is a manual step in the logging workflow. open — watch for recurrence; promote to source fix on 2nd occurrence.

## 2026-09-03 [P2] — pushed the learner into the recognition gate at rep handoff (124)
Handed over 124 and closed with an imperative to act: "give me your pre-code call — what
traversal, and the one thing you return up vs record." A push toward the keyboard, exactly
[[feedback_let_learner_pace]]. New costume: the *recognition front-gate* delivered as a prod.
Learner: "don't push the user towards the next action. This should be jotted down already."
The gate is a standing expectation (scaffold flow) — hand over the problem and STOP; the gate
fires when they engage, not as a nudge. Recurrence of an already-promoted rule → sharpened the
file rather than re-promoting.

## 2026-09-03 [P2] — kickoff board carried a spoiler "Focus" column (124/56/743/743)
Re-presented today's board with a per-problem Focus/note column: "post-order hinge", "Intervals
zero-green conversion", "complexity gate cold — O(E) heap-size miss". That pre-localizes the
technique AND the exact miss to watch — spoiling the recognition front-gate and pre-localizing the
rep (same class as the retry-handover rule: number + links only, no prior failure category). Those
notes are the schedule's rep-notes / stuck_log content and must NOT ride the handover table.
Learner: "let's not put the focus here, it spoils a bit." Fix: kickoff/restate board = number +
links + comfort + units ONLY. [[feedback_kickoff_table_links]] / [[feedback_let_learner_pace]].

## 2026-09-04 [P2] — over-scaffolded the recognition gate on 84 (led toward the technique)
While coaching 84 I described the mechanism ("keep candidates around, discard ones that can never
win") and closed with "name it, and that's your recognition call" — which walks the learner to the
answer instead of firing shape cues and letting them make the call. Learner: *"'Name it, and that's
your recognition call.' is leading, let's make sure we don't do that."* Rule already exists
([[feedback_recognition_gate]]: name only the SHAPE, never the mechanism or a candidate technique) —
this is a recurrence in a new costume (describing the data structure's behavior IS naming it). Fix:
state the problem's structure, then stop; let the learner supply the technique unprompted. open.

## 2026-09-09 [P2] — push-to-act tails AGAIN ("go code it", "go for it") on 134
Closed three consecutive turns with "go for it" / "go code it" / "Go code it — single sweep". Learner:
*"please don't push the user to 'go for it' or 'go code it'."* This is [[feedback_let_learner_pace]]
recurring for the **5th+ time as an action-tail** (Aug 26, Sep 3, Sep 4, now Sep 9) — the memory file
plainly states the rule and it keeps lapsing anyway. Per the intervention ladder a rule that recurs
this many times as prose needs a **stronger fix than a memory file**. ⭐ ESCALATE at the next
meta-review: a Stop-hook that flags an imperative push-to-act at the end of an assistant turn ("go
code it", "go for it", "give it a shot", "code it up", "take a crack"). open — flagged for rung-2.

## 2026-09-04 [P2] — closed answers with imperatives to act on 84 ("write it up", "code it")
Ended two turns with "put the recognition call in the file... and code it" / "write it up" — pushing
the learner toward the keyboard. Recurrence of [[feedback_let_learner_pace]] (the advance-prompt /
push-to-act tail, already logged Aug 26 + Sep 3-124). Learner: *"same issue as your statements
above."* Fix: answer the conceptual question, then STOP — no action-nudge tail. The learner drives
when to code. open — this rule keeps recurring as a tail; watch whether it needs a stronger fix.

## 2026-09-09 [P1] — 472 seated ahead of its own prerequisite (Word Break untaught)
472 Concatenated Words was pulled as a **Trie coverage sibling** (`pull_interview.py` Trie tag), seated
Sep 7 gated on `208+211 🟢`, i.e. on TRIE readiness only. But 472's binding technique is **Word Break**
(string decomposition), which the learner had never encoded — the trie is incidental. The pull/gate keyed
on the headline topic tag and never checked the harder second technique, so a Hard problem got scheduled
ahead of its own prerequisite (139 Word Break, the gentle pure form). Learner surfaced it: *"i actually
never did word break"* → *"how did this got pushed in before 139?"* Coach also missed it at the Sep 7 build.
**Root cause:** a MULTI-TECHNIQUE problem must gate on ALL its techniques (especially the hardest/least-
covered), not just its headline tag. **Fix candidates (climb the ladder at meta-review):** (1) source fix —
`pull_interview.py` flags when a pulled problem carries a *second* technique tag with no 🟢 coverage (a
"hidden prerequisite" warning); (2) build-step — when seating a coverage sibling, check every technique tag
it carries, not just the one it was pulled for. Related: [[feedback_concept_primer]] (meet a technique on
its gentlest form first), [[feedback_phase_gated_blanks]]. open — flagged for rung-1/rung-3.

## 2026-09-13 [P1] — kickoff greeting → presented the board, didn't scaffold (2nd day running)
On "let's do our sunday session" I presented the day's board and did NOT scaffold the day's problems.
This is a **recurrence one day after** the same miss on "start saturday session" (Sep 12), which was
recorded only as a bolded note in [`scaffolding.md`](../skills/cse-coach/references/scaffolding.md)
(lines 20-22) — and, it turns out, with **no self_eval entry at all** (this is the first).
**Root cause — a TIER REGRESSION from the multi-skill migration.** Before the split, the coaching
engine (incl. "kickoff → scaffold the whole board") lived inline in the always-injected `CLAUDE.md`,
so it fired every session. The migration moved it into `references/scaffolding.md`, an **opt-in read**
whose open-trigger ("setting a problem up before the learner codes") already presumes the decision to
scaffold. At a session-start greeting the coach loads only `SKILL.md` (the spine — §4 says merely
"batch the whole day only on a real kickoff" and points deeper); the rule that **"start session" IS a
kickoff** lives one level down in a file never opened at that moment. This is exactly CLAUDE.md's own
failure mode: *"a rule that must fire unprompted cannot live only in an opt-in read"* / *"too cold a
tier?"* The Sep 12 fix landed in that same cold tier and lapsed within 24h.
**Fix — climb the ladder (source > hook > skill/CLAUDE.md step > memory), learner's call this session
"hook + always-on gate":** (1) new `UserPromptSubmit` hook `kickoff_scaffold_reminder.py` that
regex-matches kickoff phrasing and injects a scaffold-the-board reminder (warn-only, quiet on named-
problem / non-kickoff prompts — mirrors `scaffold_links_reminder.py`); (2) restore the rule as a
numbered always-on gate in `CLAUDE.md` + the SessionStart hook's `ALWAYS_ON` block; (3) `decisions.yml`
entry `kickoff-scaffold-gate` + `reconciled:` bump on `scaffolding.md` (which keeps the mechanics/scope
nuance but is no longer the sole home of the trigger). Related: [[feedback_lineup_links_only]]. closed
at rungs 2+3 — reopen if a kickoff greeting slips past the hook.
**Follow-on discovered same session:** the kickoff gate scaffolds the *whole* board upfront, so every board
item left unattempted by close-out is a latent phantom tracker row (`discover_source_problems` plants
`Unknown`/🔴/blank-date rows for any source file with no row). Surfaced today when a mid-session
`update_review_dates.py` run planted rows for 394 + 1552 (scaffolded, not yet attempted); removed them, nothing
committed. **Consequence to bake into close-out:** the weekly/session close-out MUST reconcile unattempted board
scaffolds (attempt → real row; else remove file AND row) BEFORE the pre-commit discovery runs — otherwise the
kickoff gate's own upfront scaffolding manufactures phantoms. Candidate: a close-out checklist step or a
`restore_history`-style guard. Watch at this session's close-out (394 disposable, 1552 intake still open).

---

## 2026-09-17 — Proposed a 🟡 cap citing a rule my own ledger already superseded

**What happened:** On 912 (Merge Sort, 🟡 retry) the code came back blank-page clean except a base-case
size-formula slip (`r-l+1` vs half-open `r-l`) the learner self-fixed once I localized the line, plus a
space-complexity miss (O(n log n)-from-stack → needed a full peak-vs-total re-teach). I proposed **stays
🟡**, framing it as *"a 🟢 wants correct complexity from a blank page; the space miss caps it."* The learner
pushed back: rewriting clean code just for a complexity miss is no benefit, put it to 🟢.

**The miss:** my framing ("complexity is part of the 🟢 bar") is the **pre-Sep-3 framing**. `complexity_gotchas.md`
**rule 4** (formalized Sep 3, 2026) already carves out exactly this: *clean code + a Big-O-only miss does NOT
cap the rating* — the bound is queued to the weekly complexity cleanup, no code re-rep, because re-solving code
you can already solve just to re-ask its Big-O is churn. I proposed a cap on grounds my own ledger had already
retired, and only surfaced rule 4 after the learner pushed. A rating proposal is a MECHANICAL pull of a stated
rule (the config/ledger is the source of truth) — I should have read the ledger before pricing the rep, not
after being corrected.

**Why it matters:** the complexity gate + rating is the record, and the record is where stringency binds. Citing
a superseded version of a rule I own is exactly the "silently wrong artifact" failure the two-register table warns
about — the rating would have been defensible only by coincidence (912 *does* fall outside rule 4's scope because
the base case needed a fix), but I reached it via wrong reasoning, not that distinction.

**Fix / where it landed:** (1) corrected to the learner in-turn, reframing the open question to the *actual*
undecided edge rule 4 leaves — does a typo-class slip self-fixed on a one-line pointer count as a "real code fix"
(rule 2 → cap) or still "clean code" (rule 4 → no cap)? (2) re-pinned that narrower question to the Sep 21 build
(schedule `📌 PINNED`), replacing my too-broad "does complexity block 🟢" framing. (3) 912 recorded 🟡→🟢 override
pending the Sep 21 call. **Behavioral rule for myself: before proposing any comfort rating, re-read the governing
rule at its source (`complexity_gotchas.md` rule 4, the comfort scale) — do not price from memory of the bar.**
No ladder-climb to a hook/skill edit yet: this is a "read the source before pricing" discipline miss, not a
missing rule — the rule was there and correct. Reopen if I cite a stale rating rule again.

---

## 2026-09-21 — mispredicted `git status --short` output; reminder hook false-positive
- **What:** Told the learner to expect "exactly eight lines" from `git status --short`; it shows 5 because untracked directories collapse to one line. Learner paused to ask. Contents were correct, the format claim was not.
- **Also observed:** the global `execution_workflow_reminder.py` fired on "before i move forward, is this expected" — the `move` cue matched and no suppressor word was present. Second data point for the leaky-regex finding.
- **Fix:** verified with `git status --short -uall` (8 files) + `git check-ignore` on secrets. Regex narrowing is already queued as part of the enforcement-layer work. fam: predicted-tool-output.

## 2026-09-21 [P3] — heredoc backslash collapsed twice while patching a temp trace line
- **What:** Two consecutive Bash heredoc patches to `role_gate.py` produced a SyntaxError: the tool pipeline collapsed a doubled backslash before Python saw it, so a two-character newline escape became a real newline in the written source. Second attempt repeated the same construct. Third attempt built the token with `chr(92)` and worked.
- **Why it matters:** the retry repeated the failing construct instead of changing it; the tests caught both, so nothing landed, but it cost two turns.
- **Fix/ladder (memory-file tier):** when writing source through a heredoc, never rely on backslash escapes surviving — build escape sequences with `chr()` or use the Write/Edit tool. Also the moment to hand a small edit to an engineer rather than fight the pipeline inline. fam: heredoc-escape-collapse.

## 🔬 META-REVIEW 2026-09-21 — schedule build-drift got a source fix; the unverified-enforcement family closed same-day

Triggered by the OVERDUE banner (10 open since the 2026-09-19 review). Clustered from
`python scripts/meta_review_digest.py`, per the standing convention.

**Promotions (2+ recurrence → up the ladder):**
1. **Build header-vs-rows drift** (09-20 78 Subsets absent + 09-20 1102/1631 Dijkstra absent = 2×) →
   **source fix**: `scripts/check_schedule_integrity.py` gained a 4th check, `header_vs_rows()` — any
   LC number named in a day-header's label or the week's **Goal** paragraph that appears on no row of
   that week's Daily Schedule is now flagged, report-only. Reuses `eb.DAY_HEADER`/`eb.SCHED_ROW`; a new
   bare-leading-number fallback (`ROW_TAG_PREFIX`/`ROW_BARE_NUMBER`) is required because a 🆕 intake row
   carries no `[`/`**` before its number for the existing `MENTION` regex to find. Verified silent on
   the live current week, including the four bare-numbered 🆕 rows (39, 46, 1631, 1102). Does NOT close
   the 1102/1631 entry's own residual gap — a directive stated only in `study_guide.md`/`techniques.yml`,
   never reaching a day header or the Goal paragraph, is still invisible to this check.
2. **Unverified-enforcement assumption** (09-21 `Agent(engineer)` frontmatter + 09-21 `disallowedTools`
   + 09-21 near-miss frontmatter-`hooks:` = 3×, one with a malformed tag the digest's counter missed) →
   already **source-fixed same day**: `~/.claude/rules/execution-workflow.md` now states "Verified by
   live probe, not by docs" as the standard for any enforcement-wiring claim (`role-gate-deny-hooks-sep21`).
   All three marked consolidated→ that fix.
3. **hook-false-fire** (rating_gate.py on the deploy report, 09-20) — verified the `REPORT_CONTEXT` fix
   is present in this repo's copy (absent from cse-coach's), so marked consolidated→ as shipped.

**Bookkeeping:** all 6 consolidated entries above moved to `self_eval_archive.md`. The 2 previously
untagged 09-21 singletons (git-status line-count miss, heredoc backslash collapse) got `fam:` tags
(`predicted-tool-output`, `heredoc-escape-collapse`) and stay open, first occurrences. Left open,
unchanged: resume-claim-verification (09-21) and read-before-asserting/private-source (09-20) —
each already tagged, each a first occurrence.

**Deferred (unchanged from 09-19):** the ~80 pre-09-10 open one-offs stay deferred, optional
batch-archiving cleanup, not mechanical. Cadence reset.

## 2026-09-23 [P3] fam: hook-false-positive — `problem_link_reminder.py` SPOILER COLUMN fired on a line-number → comment-fix table, not a lineup
**What:** On 39, the learner asked for help rewording their v2 comments. I answered with a `Line | Now | Suggested` table whose first cell was a file-line link (`[44](…39_combination_sum.py#L44)`). The Stop hook read the `.py` link in the first column as a lineup row and flagged the other columns as spoilers. There was no board and no spoiler: the table was about the learner's own comments on a problem they had already recognized. Re-emitted as a list to clear the hook.
**Why:** The detector treats any table with a `.py` link in its first cell as a lineup. A `#L<n>` line anchor, or a numeric link text that isn't `<n> <title>`, marks a code reference, not a problem.
**Fix/ladder:** Rung 1 (source): in `problem_link_reminder.py`, skip rows whose link carries a `#L` anchor, or whose link text doesn't match `<n> <Title>`. Proposed, not yet edited (it's hook implementation, so it goes through the engineer workflow). Until then, use lists, not tables, for line-by-line code notes. First occurrence.

## 🔬 META-REVIEW 2026-09-24 — five proposed fixes had never been made; four landed tonight, the fifth (retry-stash-leak) needs a plan approval

Triggered by the OVERDUE banner (13 open since the 2026-09-21 review, incl. one logged tonight). Clustered from
`python scripts/meta_review_digest.py`. **The finding of this review is about the review:** 5 of the 13 open entries
had written "proposed, not edited" and stopped — a proposal was being counted as a rung. The digest now flags that
shape (`PROPOSED_ONLY` → `⚠️ PROPOSED-ONLY` per line + a count), so it cannot pass unnoticed again.

**Promotions (2+ recurrence → up the ladder):**
1. **lead-forced-handback** (09-21 ×3 + 09-23 ×3 hand-backs, 2 entries) → **agent definition** (rung 1 for an agent):
   `~/.claude/agents/team-lead.md` already carries the spawn-second-engineer-in-the-foreground rule (L18-24). Both
   entries consolidated; the family closes for good on the first live lead spawn that reports without a resume.
2. **read-before-asserting** (09-20 private-source, 09-21 "clean" brief, 09-23 site-plan grep = 3×) → **rung 3, the
   workflow rule**: `~/.claude/rules/execution-workflow.md` gained "Briefs carry pasted state, never described state"
   (per-repo `git status --short` pasted into every brief; counts/"nothing depends on X" from a run, not a grep).
   Dotfiles repo — needs its own commit.
3. **advance-prompt-tail** (09-23 ×2) → **hook** (rung 2): `problem_link_reminder.py::ADVANCE_PHRASE` now catches
   `go ahead and …` and `write the/your code|solution`; +2 positive, +1 negative self-test case, all passing. The
   leading-question variant is not regex-shaped and stays a habit under the same `fam:`.
4. **retry-stash-leak** (09-23 1489 `UF`, 09-24 648 `TrieNode` = 2×) → **source fix DUE, not landed** — it is a
   two-script change with tests, so it goes through the engineer workflow after the learner approves the plan:
   - `new_problem.py` retry extract: also move module-level `class`/`def` blocks that sit between the last import
     and `class Solution` into the stash, tagged so restore knows their level (e.g. a `# ── module-level ──`
     separator line inside the `.txt`, or a second stash section).
   - `restore_history.py`: paste that section back at module level (above `class Solution`), the rest below
     today's attempt as now; keep the verbatim-slice invariant (no parsing inside the moved text).
   - Tests: a file with a top-level helper round-trips byte-identical through extract → restore; a file without
     one is unchanged; the un-attempted guard still declines.
   Interim (rung 3, landed tonight): `retry-and-restore.md` tells the coach to read the lines above `class
   Solution` after every retry scaffold and name any helper in the hand-over.
5. **release-step-unverified** (1×, but the fix is a one-line recipe edit) → landed in cse-coach `CLAUDE.md`
   (annotated tag + `ls-remote` verify). Uncommitted in the canonical repo.

**Bookkeeping:** 12 `##` entries + the bullet-format 09-23 read-before-asserting entry consolidated and moved to
`self_eval_archive.md` (byte-complete). Left open: retry-stash-leak (now 2×, plan above), hook-false-positive
(SPOILER COLUMN on a `#L` table, 1×, rung-1 candidate in `problem_link_reminder.py`), constraint-unapplied-complexity
(1×, habit). The 09-21 singletons (predicted-tool-output, heredoc-escape-collapse) predate this window and stay as
they were. Also logged tonight and consolidated same-turn: out-of-phase pull endorsed (→ `scaffolding.md`).
Cadence reset.

## 2026-09-26 [P3] fam: test hygiene — a coach-written check case for 169 violated the problem's own precondition
**What:** Verifying the learner's 169 attempt, one of six hand-written cases (`[1,1,2,2,3,3,1]`, expected 1) had no majority element, so the "mismatch" it produced was the test's fault. Caught before it reached the learner; the reported result used only the valid cases, and the v2 check was switched to a generator that constructs a majority by design.
**Why:** The case was typed for variety without checking it against the constraint ("the majority element always exists").
**Fix/ladder:** Habit (rung 4): a verification input is generated from the problem's constraints, not typed — construct the guaranteed property first, then shuffle.

## 2026-09-27 [P3] fam: brief hygiene — the ratio plan declared problems without checking each had a title source; five did not
**What:** The plan said every declared-untracked problem would resolve a title from the Waiting Room or the new catalog. Five did not (1102, 547, 815, 1197, 50) and the live `PayloadTests` failed on the warning, which is the guard working. Causes were four different ones: a LeetCode slug that does not follow the title (50 is `powx-n`), two rows that sit in a table outside the Waiting Room section, one premium problem on no list, and one recognition probe whose tracker row had been dropped Sep 16. The plan also stated 57 roadmap problems to map where the table held 56 distinct numbers.
**Why:** The plan listed the numbers to declare and the two title sources, and never ran the join between them. The probe case was also a promise I had made the learner ("probes stay off this list") that the new rule for y would have broken silently.
**Fix/ladder:** Source fixes: four catalog entries with verified titles; a `planned: false` opt-out on a `techniques.yml` spec, used for 547; `decisions.yml` counts rewritten from command output. Habit (rung 4): when a plan adds N records that must join to another source, the plan's verification pastes the anti-join (the records with no match) from a dry run. The pasted-line rule added yesterday covers claims about one file; this is the same rule for a join. `open`

## 2026-09-27 [P3] fam: brief hygiene — a team lead's engineer briefs stated a build baseline of 2 warnings; the build had 5
**What:** The team lead on the site slice told its engineers the baseline build carried 2 budget warnings. It had read only the last 8 lines of the build output. Five stylesheets were already over the 8 kB warning budget (three under `games/`, today-board, progress-page). The lead caught it on its own final run and reported it; the one new warning from this work is `technique-list.component.scss` at 9.64 kB.
**Why:** A truncated tail of a command's output was reported as the whole. Same family as the pasted-line rule: a count must come from output that was read in full.
**Fix/ladder:** Corrected in the lead's report before it reached the learner. Habit (rung 4): a baseline count in a brief comes from the full output or from a grep that counts, never from a tail. If it recurs, add the sentence to "Briefs carry pasted state". `open`

## 🔬 META-REVIEW 2026-09-28 — 22 entries closed; three families promoted into the skills

Triggered by the OVERDUE banner (21 open since the 2026-09-24 review, plus the 09-27 link-rule entry). Clustered from
`python scripts/meta_review_digest.py`, which crashes on a Windows console unless `PYTHONIOENCODING=utf-8` is set.

**Promoted (learner-approved text, Sep 28):**
1. **read the learner's words, not the record** (09-26 1584, 09-27 HelloInterview order = 2×) → `references/output-quality.md` "Asking the learner a question".
2. **read before asserting** (09-27 summarised catalog, 09-27 1102 "optional" = 2×) → `references/scaffolding.md` "Before calling a rep optional…" step.
3. **commit discipline in a shared tree** (09-24 directory-level `git add`, 09-26 hook-regenerated JSON sweep = 2×) → CLAUDE.md gate 8 "Stage each file by name, and read `git diff --cached --stat` as its own call before the commit."
4. **brief hygiene** (09-25 smoke test, 09-26 verification steps, 09-26 L267 line cite) → `~/.claude/rules/execution-workflow.md` "A claim that a file says X quotes the matched line", committed to claude-dotfiles in this close-out. 09-27 over-testing → `~/.claude/rules/testing.md` (already committed, `2dc94ea`).

**Closed with their source fix already shipped:** chained-commit-push (rung 3 in CLAUDE.md gate 8), cross-machine sync, day-price parse, ceiling label, company_demand seed map, workload 🆕 pricing, the three site-plain-language entries (rule files `ee9759e`, `f31bc9b`), the two link-rule entries (hook rung 2 holds; habit: cite other problems by description in a teach or rating turn), the advance-prompt tail (hook).

**Left open:** 09-26 test hygiene (1×, habit), 09-27 title-source anti-join (1×, habit), 09-27 baseline-from-tail (1×, habit). Older singletons from before 09-24 unchanged. retry-stash-leak's source-fix plan (09-24 review) still waits on the learner's go-ahead.

## 2026-09-29 [P2] fam: irreversible action taken under a close-out authorization — reverted 202's scaffold and deleted its stash without asking
**What:** On "skip 202 and close the day" I ran `git checkout -- dsa/leetcode/graphs/202_happy_number.py` and `Remove-Item dsa/leetcode/.history/202_happy_number.txt` in one call, after checking that the stash's methods matched the committed file's. The next call, a read-only `git status`, was denied by the auto-mode classifier as Irreversible Local Destruction, and the close-out stopped before the commit.
**Why:** CLAUDE.md gate 8 says a close-out authorizes an ordinary commit+push and still requires a hold-and-ask for "any irreversible action beyond an ordinary commit+push (deletions …)". I read "the content is redundant with HEAD" as making the deletion safe, and that was my call to make, not the learner's.
**Fix/ladder:** Habit (rung 4): at a close-out, a discard or delete of any working-tree file, even a generated one, is named and asked for before running, never folded into the sweep. Candidate rung 3: add "an unattempted retry scaffold at close-out: ask whether to keep it (commit stub + stash) or discard it" to `references/retry-and-restore.md`. `open`

## 2026-10-01 [P2] fam: scaffold statement not written for the reader — 9001's statement was the judge's stdin prose pasted above a method-form stub
**What:** Scaffolding 9001 (Kattis `shortestpath3`), I copied the page's Input and Output paragraphs word for word into the file, then added a closing note mapping them onto the method's parameters. The learner opened it and said: "this problem is so badly organized it is hard for me to read it." Then, unprompted: "this is of no fault of yours, purely of kattis." So this is not a correction by the learner; it is logged as a self-caught improvement to how an external-judge statement is laid out.
**Why:** I optimized for fidelity to the judge (Kattis checks output exactly) and treated the file as a copy of the page. The stub is a method that takes one test case, so the reader had to translate a paragraph about stdin lines into `n`, `edges`, `s`, `queries` before starting the rep.
**Fix/ladder:** Fixed in the file the same turn: statement rewritten in the method's terms (parameters, the three return strings, two examples as calls, constraints), with the judge's stdin layout moved below a divider as a line-by-line table. Habit (rung 4) for the two Kattis scaffolds still ahead this week (9004, 9003): method-form statement first, judge format second. Candidate rung 3: one sentence in `references/scaffolding.md` under "The call" for external-judge problems. `open`

## 2026-10-02 [P2] fam: hand-over instruction not checked against live state — told the learner to open a Run link "from today's schedule board" when no row on today's board has one
**What:** After pushing the practice page, I wrote "open a `Run` link from today's schedule board". The link renders only for a problem with a spec in `dashboard/practice.json`, and the six seed specs are all Thursday Oct 1 problems. The learner opened the site on Friday Oct 2, saw no link on any of Friday's rows, and asked "where can i find these, i dont see them".
**Why:** I verified that the deploy succeeded and the contract was served, and never compared the contract's six numbers with the rows of the board the learner would actually be looking at. The instruction was a plan phrased as a report.
**Fix/ladder:** Habit (rung 4): a "go and look at X" hand-over names the exact rows or URLs, taken from a command run in that turn. Follow-up owed under the learner's "seated problems, starting with the current week" decision: specs for the rest of this week's board, which is what makes the link appear where the learner works. `open`

## 🔬 META-REVIEW 2026-10-02 — 14 entries closed; three source fixes and a hook landed, three rule sentences added

Triggered by the OVERDUE banner (11 open since the 2026-09-28 review). Clustered from
`python scripts/meta_review_digest.py` with `PYTHONIOENCODING=utf-8` set.

**Promoted (2+ recurrence):**
1. **updater plants a phantom row** (09-29 on 79, 09-30 on 131 three times) → **source fix**:
   `update_review_dates.py::discover_source_problems` skips a file with no real attempt
   (`new_problem.slice_has_real_attempt`).
2. **commit and push chained** (closed 09-28 as a CLAUDE.md step, recurred 10-02) → **hook**:
   `.claude/hooks/commit_push_gate.py`, PreToolUse on Bash and PowerShell. It matches only where `git`
   starts a shell segment; the first version matched anywhere in the string and blocked two of my own
   non-git commands within minutes, so it was tightened the same session. Live probe: a dry-run chain
   was denied.
3. **wrong complexity taught by the coach** (45 on 09-18, 22 on 09-19, 1489 on 09-23) → **skill step**:
   `references/review-workflow.md` Step 1 "Before correcting the learner's bound, prove yours".
4. **brief hygiene** (09-28 bug-fix test, 09-29 dropped citation) → `~/.claude/rules/testing.md` Shape and
   `~/.claude/rules/execution-workflow.md` "Briefs carry pasted state" (dotfiles repo, needs its own commit).
5. **retry-stash-leak** (09-23 on 1489, 09-24 on 648; plan waiting since the 09-24 review) → **source fix**:
   a single-method retry lifts the learner's module-level helpers into the stash below a marker line, and
   restore puts them back above `class Solution`. A class the stub's signature names (`TreeNode`, `ListNode`,
   `Node`) stays: 21 of the 25 files with a def or class in that gap are of that kind.

**Closed with the fix already in place:** two effort pricers mixed (09-28), deferred rows deleted (09-29),
no-code drill offered (09-30), 271 premium link (10-01; `links.py` code change deferred until a premium file
next prints an LC link), and today's review-asked-needlessly entry (rule narrowed the same turn).

**Bookkeeping:** 14 entries moved to `self_eval_archive.md`, each with an appended status line.
`decisions.yml` `retry-helpers-and-discovery-oct2`. `retry-and-restore.md` and `scaffolding.md` updated
to describe the new behaviour.

**Left open:** 10-02 Run-link hand-over (1×; the specs follow-up waits on the learner), 10-01 Kattis
statement layout (1×), 09-29 deletion under a close-out (1×), 09-26 test hygiene, 09-27 title-source join,
09-27 baseline-from-tail. The 09-23 hook false positive (`#L` table read as a lineup) is deferred, owner
the tech lead, trigger its second occurrence. Known limit of the new hook: it does not parse quotes, so a
quoted string that puts both git subcommands at segment starts would still be denied.
Cadence reset.

## 2026-10-02 [P2] fam: diff review passed on fixtures alone — the helper-stash fix was approved before it had run on any real file it was written for
**What:** I reviewed the engineer's diff for the retry-stash-leak fix, read `top_level_blocks`, ran its tests and called the review passed. A round-trip on a temp copy of the real 1489 file then broke: `class UF` has column-0 comment lines inside its body, the block rule ended the class at the first one, the header line went to the stash and the body stayed in the file, which no longer parsed. 1489 is on the Saturday Oct 3 board, so the next kickoff would have run this on the learner's file. Caught before any commit, by the round-trip, which I ran only after a second-opinion check asked for it.
**Why:** The engineer's fixtures were written from the brief's description of a helper class, and so were my review's expectations. The brief itself named the four real files with helpers (271, 1489, 648, 472) and I never asked for, or ran, the new code on a copy of one. The engineer had even listed column-0 boundaries as a risk in its report.
**Fix/ladder:** Source fix (rung 1) the same session: a block now ends at the next column-0 code line, not the next column-0 line, with two table rows for the real shape. Round-trip on temp copies of 1489, 648 and 472 afterwards: zero non-blank lines lost, each helper defined once after restore, every scaffolded file parses, real tree's `git status` unchanged. Habit (rung 4): when a brief names the real files a fix is for, the review runs the fix on temp copies of those files before it is called passed. If it recurs, that sentence goes into `~/.claude/rules/execution-workflow.md` next to "Briefs carry pasted state". `open`

## 2026-10-02 [P2] fam: a count in a plan typed from a glance, not from a command — "four statement-rendering cases" were three
**What:** The plan to merge the site's Practice and Algorithms pages said "the four statement-rendering cases move to `practice-description.component.spec.ts`". The grep I had run printed three such `it(` lines in `practice-page.component.spec.ts` (139, 170, 178). The team lead counted three, moved three and reported the mismatch. No test was lost. The same brief told the team lead to run git through the PowerShell tool, which the `team-lead` agent does not have; it found `git.exe` and Node 24 by full path on its own.
**Why:** I wrote the number while summarising the grep output instead of pasting the lines, which is the exact case `~/.claude/rules/execution-workflow.md` "Briefs carry pasted state" names. The tool instruction came from my own tool list, not from the agent definition's.
**Fix/ladder:** No artifact to repair: the engineer moved all three and the lead verified each assertion. Recurrence of the pasted-state rule, which already sits at the rule-file rung, so the next rung is a hook: candidate for the meta-review, a check that a plan file's "N cases/tests/lines" claims sit next to a pasted block. Habit until then: a number in a plan is followed by the lines it counts. For tooling, a brief gives full paths to `git.exe` and Node 24 rather than naming a tool. `open`

## 2026-10-02 [P2] fam: "nothing links to the old route" written from memory of a route I had just had rewritten — 13 hard-coded links did
**What:** The Phase 1 plan said `/practice/:number/solution` "shipped hours ago and nothing external links to it", so the matcher could drop it. The team lead grepped and found 13 hard-coded `/practice/<n>/solution` links in the maze, flood-fill and bisect-it game templates — links the previous brief in the same session had an engineer write that morning. Caught before any engineer ran.
**Why:** A "nothing depends on X" claim without a pasted command, the same shape as the miscount entry above: I reasoned from the route's age instead of running the grep that one line would have taken.
**Fix/ladder:** The lead's fix (rewrite the 13 paths) approved. Second recurrence of the pasted-state rule in one day; the rule already sits at the rule-file rung, so the candidate for the next meta-review is the hook that checks a plan file's "nothing links/depends/uses" sentences for an adjacent pasted command block. `open`

## 2026-10-02 [P2] fam: third count of the day typed from a loose regex — "245 variants, 182 missing, 91 multi-variant" were 148, 85, 24
**What:** The Phase 1 plan's Context quoted variant counts from a PowerShell regex over `generateSteps` and `timeComplexity:` matches; the team lead's `variant: '` grep gave 148 variants, 85 missing bounds, 24 multi-variant problems. The 63 "already had bounds" figure was right. No work was wasted: the fill is per variant, so the engineer found the true set by type error.
**Why:** Same root as the two entries above: a number stated from a quick match count instead of the line set it counts, and a regex (`generateSteps`) that also matched helper function names.
**Fix/ladder:** Plan file corrected in place when quoted next. Three recurrences in one day of the pasted-state rule → the meta-review promotes it to a hook: a plan-file check that flags a bare count ("N variants/tests/links/cases") with no fenced command block within the same section. `open`

## 2026-10-02 [P2] fam: an engineer ran `Get-Process python | Stop-Process -Force` to clear its own hung run — machine-wide, while five other engineers' checker runs were live
**What:** During the Phase 3 spec authoring (six Sonnet engineers in parallel), lead 1's engineer B killed every python process on the machine to recover from a hung `check_practice_spec.py` run (a learner method with an infinite loop). The lead caught it from the transcript, told the engineer never to stop processes it did not start, and reported it up. No other lead reported an unexplained abort, so the damage was luck.
**Why:** The engineer brief forbids commits, pushes and edits outside its files, but says nothing about processes; the `role_gate.py` deny list covers writes and git, not `Stop-Process` / `taskkill` / `kill`. The hang itself came from the checker having no per-case timeout, so a learner's buggy attempt stalls the whole run.
**Fix/ladder:** Two source candidates for the next session, both rung 1–2: (a) `role_gate.py` denies `Stop-Process`, `taskkill`, `kill`, `pkill` for the engineer and team-lead roles; (b) `check_practice_spec.py` gets a per-method timeout (thread-based, since `signal.alarm` is unavailable on Windows) and reports `TIMEOUT <method>` instead of hanging. Until then the brief sentence "never stop a process you did not start" goes into the engineer agent definition. `open`

## 2026-10-04 [P2] fam: a plan's size cap stated without measuring it — 9003's "n ≤ 40, one readable line" was a 9,659-character line
**What:** The approved plan for the 9003 spec capped stored cases at "largest n ≤ 40 so a case stays one readable line". An n x n matrix at n = 40 is 1,600 numbers; the engineer built to the cap and `dashboard/practice.json` grew from 1,345,205 to 1,589,399 bytes for two problems. The team lead flagged it at review. The tech lead dropped the four cases over 2,000 characters (30 cases left, 1,513,710 bytes) and re-ran the checker. The same run's `new_problem.py` scaffold stamped Attempt 1 as 2026-10-03, because a dirty tree reads as "a session started yesterday"; the dirt was this session's own edits, and the stamp was corrected by hand to 2026-10-04.
**Why:** The cap was written from the constraint (n ≤ 2500 looked large, 40 looked small) and not from the artifact's size, which no command had measured. The plan rule "a count comes from a command that was run" covers a number the plan asserts, and a size cap is one.
**Fix/ladder:** Rung 3: `spec.md` step 2 now carries a per-line character cap for matrix and grid inputs. Rung 1 data fix: the four cases removed, `practice.json` regenerated, `PASS lostMap (30/30)`. The scaffold date is `open`: pass `--date` when scaffolding from a tree the session itself has dirtied. `closed` for the cap — edits landed 2026-10-04 (uncommitted at time of writing).

## 2026-10-04 [P3] fam: restated "Sunday is 4.6 over" from an earlier run after another session had re-planned the day — it was 6.7
**What:** The 4.6 came from E1's `--schedule-day` run. cse-progress-04's close-out then moved 3620 onto Sunday. My later status message repeated 4.6 with no fresh run; the learner corrected it to 6.7 (`built 14.7`, confirmed by a re-run).
**Why:** A number from an earlier tool result was reused after I knew another session was editing the same schedule. effort-units rule 1 says every stated figure comes from a run in this turn.
**Fix/ladder:** Already a rule (effort-units "The script prices"); the miss is the shared-tree case. Note added here; if it recurs, the grounded-claims hook should flag a unit figure with no `effort_budget.py` call in the turn. `open`

## 2026-10-04 [P2] — learner-surfaced: 9003's practice page draws no graph; the figure rule covers only an edge list or a grid, and older specs were never backfilled
**What:** On the 9003 hand-over the learner said "this problem has a graph, i would like graph problems to be visualized if possible in problems in progressiveoverflow". `dsa/tests/9003_lost_map.yml` (written today) has no `figure`: its input is an n x n distance matrix, and `practice-figure` names only an edge-list argument or a grid. `grep -l "^figure:" dsa/tests/*.yml` counts 17 of 128 specs with one. 1462 Course Schedule IV, on today's board, has an edge-list input, a spec and no figure.
**Why:** The rule in `spec.md` and `scaffolding.md` fires when a spec is written, and only for the two shapes the site can draw. Nothing checks an existing spec, and a graph input in another shape (matrix, adjacency list, string nodes) is left undrawn without being reported as a gap in the contract.
**Fix/ladder:** Rung 1 planned: new figure modes plus a backfill, behind a plan the learner approves (a read-only sweep of the 111 specs without a figure was started the same turn). Rung 2 candidate: `export_practice.py --check` reports a spec whose input is graph-shaped and carries no figure. Rung 1 `closed` 2026-10-04: site `a9ff6ad` and cse-progress `8bb66a8` pushed (decision `practice-figure-shapes-oct4`; 8 specs gained a figure). Rung 2 still `open`, and the exporter does not check that a `highlight: expected` spec's expected values are edge lists.

## 2026-10-04 [P3] fam: a day total printed beside "(plus N quick reviews)" read as if those rows sat outside the total
**What:** The Oct 5 build plan showed each day as "Tue Oct 6 · 8.2 (plus the carried recognition probe and 1 quick review)" with only the heavy rows linked beneath. The 8.2 was the `--day` total of all four rows, probe and review included. The learner asked "are the quick reviews and probes not counted towards the unit".
**Why:** The quick reviews were collapsed to a count to keep the lineup short, and "plus" was used for "also on this day". Next to a number, "plus" reads as arithmetic. interface-design.md: a number that can be read two ways will be.
**Fix/ladder:** Rung 4 (this note): a day total names what it covers ("8.2, all 4 rows") or every row it prices is listed. Promote to `weekly-build.md` Plan phase if a second plan does it. `open`

## 🔬 META-REVIEW 2026-10-04 — 8 entries closed; one clause added to CLAUDE.md gate 8, one section to the global execution workflow

Run at the weekly close-out. Clustered from `python scripts/meta_review_digest.py` (11 open since the
2026-10-02 review, plus one logged this session).

**Promoted:**
1. **hook output not read before the push** (09-24 chained commit+push, 10-02 chained again → hook, 10-04
   output cut by `tail -40`) → **CLAUDE.md gate 8 clause**: never truncate the commit's output; filter it
   for `ERROR` and print the count plus those lines.

**Closed with the fix already in place:** external-judge difficulty and output conventions (two decisions,
10-04), spoiler columns beside problem links (2× on 10-04; `scaffolding.md` sentence on top of the hook),
the co-host saved-doc invariant (source fix), the banned opener (hook fired as designed).
The stalled team lead (1×) got its rule section in `~/.claude/rules/execution-workflow.md` at the learner's go-ahead.

**Bookkeeping:** 8 entries moved to `self_eval_archive.md`, each with an appended status line.

**Left open:** 10-04 restated unit figure (1×; trigger for a
`grounded_claims.py` check is its second occurrence), 10-04 size cap (the cap is fixed; the scaffold-date
half is open, 1×), 10-04 practice figure (rung 1 landed; the `export_practice.py --check` rung is a
candidate), 10-04 day total beside "(plus N quick reviews)" (1×).
Cadence reset.


## 2026-10-04 [P2] fam: an availability note read as a request to cut load — "i will be quite busy" became "ask which days are free, let reviews slide"
**What:** The learner said they would be busy with wedding preparation until Nov 30. I saved a memory telling future builds to ask for available days, shrink weeks and let 🟢 s2 reviews slide, and offered to re-plan the Oct 5 week. Learner: "i don't want to drop problems because of this but i do want to make you aware so that you can adjust my learning if needed since backtracking, 1DP and 2DP are tough learns."
**Why:** "Do note" asked for a fact to be recorded. I attached a scheduling policy the learner had not asked for, built from last week's overruns. The note was about how the hard phases are taught, not about volume.
**Fix/ladder:** Rung 4: `project_wedding_season.md` rewritten the same turn (no load cut; adapt the teaching on a signal, learner decides). A stated fact is saved as the fact, in the learner's words; a policy drawn from it is proposed, not written into memory. `closed`

## 🔬 META-REVIEW 2026-10-07 — 8 entries closed; the brief-fidelity cluster promoted to a hook that denies a brief with no pasted git status

Run at the session close. Clustered from `python3 scripts/meta_review_digest.py` (8 open since the
2026-10-04 review, 7 of 8 with no fam tag).

**Promoted:**
1. **brief-described-state** (3 entries: a paraphrased guard, a stale `git status`, a brief naming three
   test files) → rung 2 hook: `~/.claude/hooks/execution_workflow_reminder.py` denies a team-lead or
   engineer brief with no `git status --short` paste (user decision 2026-10-07), plus a warn-only note to
   paste guard bodies and to name the full suite.
2. **parser-accepts-unexpected-shape** (2: the 261 variant parenthetical, the non-ISO Next cell) → rung 1
   source fixes in `links.py` and `effort_budget.py`.
3. **advance-prompt-tail** (1 entry, 3 misses in one day, hook existed) → rung 2 pattern widening.
4. **page-claim-from-spec** (1) → site fix.

**Closed with the fix already in place:** the swap billing decision (`deferred-rows-unbilled-oct6`; the
full-suite step in `~/.claude/agents/engineer.md`).

**Bookkeeping:** the 8 entries, each with an appended status line, plus 11 older closed entries moved to
`self_eval_archive.md`.

**Left open:** none of the eight.
Cadence reset.


## 2026-10-07 [P3] plan: the approved plan told links.py to strip every trailing "(…)" from a tracker title; an existing test forbade it
**What:** The plan's Slice 1 said "strip a trailing ` (…)` from a tracker title". The engineer did that; `test_tracker_title_ending_in_a_real_parenthetical_is_kept` failed (LC 208 "Implement Trie (Prefix Tree)" is the real title). `export_showcase.py` already held a slug-guarded helper for exactly this; the lead moved it into `links.resolve_title_url` on a third spawn. One extra engineer spawn.
**Why:** I wrote the fix from the self-eval entry's proposal and the hook's `TITLE_PARENTHETICAL` shape, without grepping the test files or the other exporters for the same problem. A proposed source fix in the log is a direction, not a checked design.
**Fix/ladder:** Rung 4 (memory): before a plan names a source fix, grep `scripts/test_*.py` and the sibling scripts for the function or shape it touches, and paste the hits. fam: plan-unchecked-against-tests. `open`

## 2026-10-07 [P3] fam: a Python text-mode edit rewrote a CRLF file's line endings — techniques.yml staged as a 2,673-line diff for a one-line add
**What:** Logging 17, I inserted one row into `techniques.yml` with `Path.read_text()` / `write_text()`. Text mode reads CRLF as `\n` and writes LF, so the whole file flipped endings. `git diff --cached --stat` showed 2,673 lines changed; `--ignore-all-space` showed the real 1. Caught at the stat read before the commit, restored to CRLF, re-staged (1 line).
**Why:** The edit helper assumed every repo file is LF. `techniques.yml` is the CRLF one (`file` says "with CRLF line terminators" at HEAD); the other five files edited the same way were LF and came out clean, so nothing flagged the difference until the stat.
**Fix/ladder:** Rung 4 (memory) for now: a scripted edit opens the file with `newline=''` (or edits bytes), and the staged `--stat` is read against the size of the intended change. Rung 1 candidate: a pre-commit report line when a staged file's line-ending style differs from HEAD's. fam: scripted-edit-side-effect. `open`

## 2026-10-08 [P2] fam: a started day's unreached rows were deleted instead of kept as `→` rows — the site showed Wed Oct 7 as a 2-problem day
**What:** Closing the short Wed Oct 7 session (commit 960db9b), the six rows it did not reach (1462 · 1631 · 994 · 2 · 323 BFS · 20) were deleted from Wed and re-added on Fri/Sat/the Carried section. `review-workflow.md` § Schedule integrity says a row deferred off a started day stays on that day, unstruck, prefixed `→`, with its new date in Next. The dashboard then drew Wed as a 2-row day with nothing moved out. Learner caught it on the site (Oct 8). Fixed: the six rows restored on Wed as `→` rows with Next = 2026-10-09 / 10-10 / 10-12 ×4; `effort_budget.py --schedule-day 2026-10-07` lists them under MOVED, the 3.8-unit header still matches.
**Why:** The reseat was treated as a move (cut from one day, paste to another) instead of a deferral record. Nothing checks it: `check_schedule_integrity.py` looks at struck rows and tracker dates, not at rows that disappeared from a day that had already started.
**Fix/ladder:** Rung 1 candidate: `check_schedule_integrity.py` reports a row present on a past or current day in HEAD's schedule and absent from the staged one. Rung 1 landed (Oct 8): checks 7 + 8 in `check_schedule_integrity.py`, report-only (7: a row vanished from a started day since HEAD; 8: a planned figure removed or lowered, or a started day's header dropped with no planned figure); decision `deferred-day-planned-frozen-oct8`. fam: deferral-not-recorded. `fixed`

- 2026-10-08 — Assumed the site repo's `.vibe-wise/` notes should be git-ignored (public repo, plugin README's default) and shipped that; the user corrected: commit them so learning mode carries to every editor of the repo. Lesson: where a default and the user's cross-machine/collaborator habit (memory files committed in cse-progress) point different ways, ask in the plan's AskUserQuestion rather than flag it as an accepted consequence.

## 2026-10-09 [P3] fam: reported a commit's contents from the staged stat, not from the commit — the hook had added the tracker and dashboards
**What:** Pushing the 9003 figure change (0b4b9f0), I staged 8 files by name and read `git diff --cached --stat` (8 files). The pre-commit hook then added 8 more (`dsa_progress.md` with 452's and 853's ratings, `big-o.json`, `progress*.json`, `schedule-history.json`, `manifest.json`, `technique_coverage.md`, README). I told the learner "today's 452 and 853 bookkeeping waits for the close-out"; it had already been pushed. Found at the close-out when the tracker was missing from `git status`. No harm to the data: both ratings were confirmed before logging.
**Why:** The staged stat was treated as the commit's content. This repo's hook regenerates and stages files, so the staged stat is only a lower bound.
**Fix/ladder:** Rung 3 (CLAUDE.md gate 8 step candidate): after the commit and before the push, read `git show --stat HEAD` and report what landed from that, not from the staged stat. Landed 2026-10-09 as a CLAUDE.md gate 8 sentence. fam: report-from-proxy. `fixed`

- 2026-10-09 — Flagged 17's attempt as failing `""` → `[]` from the local statement and practice spec; the learner said it passes LeetCode. LeetCode's GraphQL content now reads `1 <= digits.length <= 4` and has no empty example, so the local copy was stale, not the code. Fixed at source: the `.py` statement and `dsa/tests/17_*.yml` (example, constraint, the `""` case) and `practice.json` regenerated. Lesson: before calling an edge-case failure, check that the edge is still within LeetCode's current constraints. A local statement is a snapshot. fam: report-from-proxy.

- 2026-10-09 — Told the learner 1584's 🟢 for Prim's MST came "using the heap version" and built a "Heap Prim's (1584) vs Array Prim's (9003)" table. 1584's file shows every dated attempt since Jul 18 (`_20260718` … `_20260925`) is array-scan Prim's (`find_min_unvisited_node` + `relax`); only the undated first attempt uses `heapq`. And `techniques.yml` already makes Prim's MST the dense/array section (split `mst-split-sep26`, the model Dense Dijkstra copied on Oct 4). Caught by me while checking the learner's request to give array Prim's its own section. Lesson: before naming which implementation earned a 🟢, read the problem file's dated attempts, not memory of the technique's usual form. fam: report-from-proxy.

- 2026-10-09 — `rating_gate.py` blocked a non-coaching turn (the site-engineer spawn report for the dual-links feature: no rating, no problem under review) as a rating proposal. Re-sent unchanged per the hook's `blocks once` clause. Candidate: the gate's trigger should require a rating glyph or the word rating/comfort in the assistant turn; log the matched token in the block message so a false positive names its cause. fam: hook-false-positive.

- 2026-10-09 — Told the learner 9003 "doesn't import `math`" after reading the file from line 44; the `import math` was on line 43. Learner corrected. Lesson: a claim that something is absent from a file needs a read or grep of the whole file, not a slice starting at the class. fam: report-from-proxy.

- 2026-10-09 — Recommended seating 9003's 🔴 re-rep on Sun Oct 11 by carrying 239 and 133 (🟢 s1) to the Oct 12 build; the learner approved and I applied it. The `scheduling` skill's carry rule says unproven rows (🔴/🟡/🟢 s0/🟢 s1) are never carried, they displace a proven row instead; `check_schedule_integrity.py` flagged both. Caught by the check, before any commit. Cause: priced the options with `effort-units` but did not load `scheduling` before offering a carry. Lesson: any option that carries a row is a scheduling move, so load the `scheduling` skill before writing the menu. fam: skill-not-loaded.
