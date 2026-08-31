---
name: feedback_kickoff_table_links
description: hyperlink each problem to its local solution file AND its problem page (LC, or the NeetCode mirror if premium) — fires when new_problem.py runs, at kickoff, and on every problem/set transition
metadata:
  type: feedback
reconciled: 2026-08-30
---

**PRIMARY TRIGGER — a scaffold is a link event. Every `new_problem.py` run ends with the
links, in the same reply, unprompted.** If the script wrote a file, the reply reporting that
names the file as a clickable link + its LC link. No exceptions, no waiting to be asked, and
not deferred to a later lineup table. *(Set by the learner Jul 31: "when anything is scaffolded,
we should be given the link so we can start the work on them.")*

**ENFORCED AT SOURCE (Aug 3, 2026).** `new_problem.py` now ends every run with a `LINKS:` line
carrying both links (`report_links()` / `docstring_url()`). The links arrive as **tool output** —
nothing to remember, no config to install. This is the top rung of the intervention ladder in
[[feedback_self_evaluation]] and it supersedes the hook below as the primary enforcement.

The **problem-page link is `LC` or `NC`**: a premium problem links the free NeetCode mirror, never
the paywalled LeetCode page. The script picks the label from the URL host, and reads the URL out of
the **file's own docstring header** in preference to deriving it — the header is the only place that
knows a problem is premium, and the only place with the true slug when the filename disagrees
(`229_majority_element_2.py` derives `majority-element-2`; LeetCode says `majority-element-ii`).
**A legacy file with no URL in its header falls back to the derived guess** — when you spot one,
write the `<number>. <title>   ·   <url>` header line into it, as was done for 219/229/994 on Aug 3.

**Hook, now the backup (Jul 31, 2026).** `.claude/hooks/scaffold_links_reminder.py` fires as a
`PostToolUse` hook on a command invoking `new_problem.py … --number` and injects this reminder.
⚠️ Its matcher was `"Bash"` alone until Aug 3, so a scaffold run through the **PowerShell tool**
skipped it in silence — that is the 6th lapse, and it was mechanical, not recall. Matcher widened to
`"Bash|PowerShell"`. Keep the hook and keep the prose anyway: neither fires on the *hand-over* and
*lineup-table* cases below, which the script cannot reach.

Why this is the trigger and the table is not: the rule was written against the **kickoff table**
and has now lapsed five times (Jul 20, 21, 23, 30, 31) — every time the output format stopped
being a table. A rule anchored to an *artifact* decays when the artifact changes; a rule anchored
to a *tool invocation* cannot. Scaffolding is also the exact moment the file link becomes **safe**
(see caveat below), so the trigger and the safety condition are the same event.

Beyond the scaffold, the same two links apply when presenting the start-of-day (or any
problem-lineup) table. Provide **two** links per problem: the **local solution file** (relative
path, e.g. `[206 Reverse LL](dsa/leetcode/linked_list/206_reverse_linked_list.py)`) and the
**problem page** as a separate short link — `LC` → `https://leetcode.com/problems/...`, or `NC` →
`https://neetcode.io/problems/...` **when the problem is LC-premium** (the LeetCode statement is
paywalled; the NeetCode mirror is free). Same rule the `--premium` flag encodes.

**Why:** the learner explicitly asked for it (Jul 20) — the file link opens the scaffold
in one click; the LC link is the canonical problem reference. Plain-text problem names cost
them a manual file hunt.

**How to apply:** in the kickoff table, render **both links INSIDE the Problem cell** —
`[<number> <title>](<repo-relative .py path>) · [LC](<url>)`, exactly the convention the weekly
schedule file already uses. Applies to §2a kickoff and any lineup/preview table.

⚠️ **NEVER give the links their own column** (set by the learner Aug 25, 2026: *"my screen on this
computer is quite small and i couldn't see the link just now. Can we add hyperlink to the problems
under the problem column so it takes less horizontal space?"*). A separate `File` / `LC` column widens
the table past a small terminal, and the column that gets pushed off-screen is **the link itself** —
so the rule above is satisfied on paper while the learner cannot see or click a single link. The
earlier wording here offered "an `LC` column (or inline)" as equals; they are not. **Inline is the
only correct form.** Keep the whole table to ~3 columns and put anything long in the Note cell.

**Same rule when NOT in a table.** A narrow screen argues for a bulleted list over a table whenever
there are more than about three columns' worth to say — the pair travels with the problem name either
way. **Also link on every transition:**
whenever moving on to the next problem or starting a new set mid-session, restate the
problem(s) with both links — don't make the learner scroll back to the kickoff table
(reaffirmed Jul 21). Related: [[feedback_proactive_scheduling]].

**⚠️ 7th lapse, Aug 5, 2026 — "provide LC link" was answered with LC only.** The learner
asked explicitly for the LC link after a scaffold; the reply gave the bare LC URL and dropped
the file link. **A request for one link is NOT a waiver of the other** — the standing pair is
`[file] · [LC/NC]`, and "give me the LC link" means *surface the link block*, both rungs, not
"omit the file link." This is the hand-over case the source fix can't reach (no `new_problem.py`
run), so it's recall-bound: any time a single link is requested mid-session, answer with the
full pair.

**⚠️ 8th lapse, Aug 6, 2026 — the un-scaffolded mid-session restate.** Ended a turn with the
remaining board as bare names ("261 (DFS) 🟢 warmup, 496 & 27 🟢 active, and SD ②") — no file
links, no LC/NC. The learner: *"3rd or 4th time I've had to remind the agent."* This is the
recall-bound restate case (no `new_problem.py` run → source fix can't reach it), and it is the
**dominant remaining failure mode**: kickoff table, "still on the board", "your call on what's
next". **Rule of thumb: any turn that names a problem number — restate, hand-over, or "what's
next" — carries the full `[file] · [LC/NC]` pair.** Silence is not lighter, it's a lapse.
~~Candidate rung-2 fix (raise at meta-review): a Stop-hook flagging an assistant turn with a bare
LC number outside a markdown link.~~ **BUILT — Aug 12, 2026 (see below).** Occurrence dates:
Jul 20/21/23/30/31, Aug 3, Aug 5, **Aug 6**, **Aug 12**, **Aug 14**.

⚠️ **Aug 14 is the 10th, and it got past the Stop hook because the hook was shipped `DISABLED`** — written and disabled the same day (Aug 12) over a transcript-parsing bug, with its own fix left in a comment. Rebuilt and re-enabled Aug 14; run `python .claude/hooks/problem_link_reminder.py --selftest <a real transcript .jsonl>` before trusting it again.

**⚠️ ~11th lapse, Aug 21, 2026 — the mid-session hand-over, AND the built hook was not loaded.**
Kicked off 239 (on today's board, scaffolded) and named it three turns running with no link —
recognition-gate prompt included. Learner, visibly frustrated: *"where is the link to the problem.
This has happened so many times, what is the issue"* — the sharpest signal yet. **Root cause was
two-layer:** (1) my chat behavior lapsed as before, but also (2) **the `Stop` hook was not active
this session.** `.claude/settings.json` is gitignored and does not sync between machines (per CLAUDE.md
SETUP); it was only *un-gitignored* in a pull run mid-session (commit e5cb291, "the hooks it never
wired"), and hooks load at *session start* — so this session began with no Stop hook. **But the deeper, durable cause was worse:** every hook in
`.claude/settings.json` invoked bare **`python`**, which does not exist on this macOS machine (only
`python3` does — Python 3.14 framework; `/bin/sh -c 'command -v python'` → nothing). So even once the
Stop hook loaded, it would have **failed silently on every fire** — as would the SessionStart memory
hook (the one that injects MEMORY.md + the five gates). The git pre-commit hook escaped this only
because it already does `if python3 … elif python …`. **Fixed Aug 21: rewrote all three settings.json
hook commands to the same `python3`-first, `python`-fallback form**, verified each runs exit-0 under the
configured command. The hook logic itself is sound: `--selftest` passed 17/17 detector + 4/4 board and
computed the live board as `['239']`. **Two lessons:** (1) a hook that lives in a gitignored, per-machine
file is one bad clone away from being prose again — the un-gitignore fixed that; (2) a hook that names a
bare interpreter is dead on any machine that spells it differently — hooks must probe `python3`/`python`
like the pre-commit hook does. Both are silent-failure classes; nothing surfaced them until the rule
lapsed in front of the learner.

**⚠️ 9th lapse, Aug 12, 2026 — the "what's next" hand-over, and the candidate fix had been sitting
unbuilt for six days.** Closed a turn with *"Next on the board is **778 Swim in Rising Water**… Want
it now, or 271 first?"* — two bare numbers, no pair on either. Learner: *"this is the 5th+ time I've
had to remind the agent."* Same restate case as Aug 6.

**ENFORCED AT SOURCE (Aug 12, 2026) — `.claude/hooks/problem_link_reminder.py`, a `Stop` hook.**
Reads the last assistant message; blocks once, naming the offending numbers, if a problem-looking
number appears outside any markdown link. Setup: [`docs/SETUP.md`](../../docs/SETUP.md) §3.

**The lesson is not "remember harder", it is about where the fix lived.** The Aug 6 entry identified
the correct fix precisely and filed it as a *candidate to raise at the meta-review* — so the remedy
for a prose rule that keeps failing was itself parked in prose, and the rule lapsed once more while it
waited. **A named rung-2 fix should be built when it is named, not scheduled.** Compare the scaffold
case: moved into `new_problem.py` on Aug 3 and it has not lapsed since.

**What this hook still cannot do**, stated so nobody assumes it away: it fires at *Stop*, so it
catches the turn after it is written rather than preventing it, and it is deliberately quiet — it
needs a problem cue word in the turn, so a terse *"778 next?"* with no surrounding context slips
through. That is the accepted trade against crying wolf. And in a **selection menu** the file link is
a spoiler (see the caveat below), so the block's own message says to answer by *stating that*, never
by adding file links.

**⚠️ SCOPE LIMIT — set by the learner Aug 14/15, 2026: "if they are not in today's todo list,
don't populate the links."** The pair is for **actionable items on today's board** — kickoff,
hand-over, restate, "what's next". It is **not** for problems named as *context*: coverage lists
("Monotonic Stack now holds 496/503/901/739"), regression comparisons, technique roll-ups, waiting-room
mentions. Those stay as bare names.

**Why it is a correctness rule and not a formatting preference.** Linking an off-board problem does two
harmful things at once: it **advertises** a problem that is not due — and on the same night this was
set, that is exactly how 503 (🟢, due Sep 9) got pulled 26 days early while a 🟡 and a
🔴 sat undone — and, for an unscaffolded retry, the file link is the **spoiler** the caveat
below already forbids. A link is an invitation. Reserve it for what you are actually inviting them to do.

**How to apply:** before adding a pair, ask *is this problem on today's list?* If no, name it plainly with
no link, or better, ask whether it should be raised at all. Corollary: **a debrief that quotes another
problem's pre-code call has spoiled that problem's next rep** — see the Aug 14 entry in
`self_eval_log.md`.

✅ **RESOLVED — the hook was taught the day's board (confirmed at the Aug 30, 2026 reconcile).** This
paragraph used to warn that `problem_link_reminder.py` blocked on *any* problem-looking number
regardless of the board, and filed the fix as a meta-review item. The fix shipped: the hook resolves
the day's board from the tracker's due dates (`_tracker_numbers`, matching **exactly** today, not
`<=`) plus today's row of the current schedule file (`_todays_schedule_numbers`), and its block
message now states outright that *only problems on today's board are flagged* and that an off-board
mention must NOT be linked. So the scope limit above is enforced, not merely asked for. The
selection-menu escape is also in the block message. **What remains coach-side and unmechanised:** the
hook still cannot tell a recommendation from a dismissal — see
[[feedback_recommend_by_number_steer_by_description]].

**⚠️ NEVER WRITE A BARE PROBLEM NUMBER — the orphan-re-emit fix (Aug 23, 2026).** The Stop hook
gathers *all* assistant text since the last human message, so a number written bare in **narration**
("901 is a design problem — needs its interface named") trips it exactly like a hand-over, even when
the same problem is properly linked in a table two lines later. The forced re-emit then produces a
*context-free* link line, which the learner reads as a directive: *"are you linking 901 because you
want me to do it first?"* (Aug 23). **Two-part fix:**
- **On the agent (the real fix — removes the trigger):** in prose, refer to a problem **by name or
  role, never by loose number** ("the design problem", "the sliding-window retry"). A number appears
  *only* inside its `[file] · [LC]` pair, never loose. Then the hook never fires mid-turn and there is
  no orphan to misread. This is stronger than labeling the orphan — it prevents it.
- **On the hook (backup):** when an orphan is still owed, the block message now permits the fixed tag
  `(links owed, order unchanged)` on the re-emitted line, so a debt-payment can't be read as a pick.

**⚠️ 12th lapse, Aug 27, 2026 — a PRESENT link that was DEAD on click.** Asked "what problems are
left today", answered with a table whose file links were markdown-correct but pointed at
`../../../dsa/...` — copied verbatim from the schedule row, where that prefix is right (relative to a
file three folders deep) but dead in chat, which resolves relative to the **repo root**. Learner:
*"clicking the link does nothing."* This is a new failure *shape*: every prior lapse was a **missing**
link; this was a **wrong-path** link, which the presence-only Stop hook waves through. **Two-rung fix,
both built the same day:**
- **Source (primary) — `scripts/links.py <number> ...`.** Prints the `[file] · [LC/NC]` pair per number,
  reading the path from disk (glob `<root>/*/<number>_*.py`) and title/URL from the file header (tracker
  fallback). The agent runs it and pastes the output — transcription is removed, so the path cannot be
  wrong. Same top-of-ladder move as `new_problem.py`'s `report_links()`, which is why the scaffold case
  never lapses. **Use it for any kickoff / restate / hand-over / "what's next" link.**
- **Hook (backup) — `broken_file_links()` in `problem_link_reminder.py`.** Now also resolves every `.py`
  link target against `REPO_ROOT` and blocks a dead one, naming the offending path and pointing at
  `links.py`. Scoped to `.py` targets so doc/URL links are never second-guessed; complements the
  unlinked-number check (that flags a *missing* link, this a *broken* one — no double-report).
  Selftest: `broken: 6/6`.

**CAVEAT — a retry's file link is a spoiler until scaffolded.** File links are safe in the
**kickoff** table because those items are scaffolded first (blank stub, prior attempts
stashed). In a **selection/candidate menu** where the learner hasn't picked yet, the retry
files are NOT scaffolded — opening one shows the old solution. So in a menu link **LC only**;
surface the local file link **only after** the pick is scaffolded. (Learned Jul 20 — linked
five unscaffolded retries and the learner opened one to their prior solution.) See
[[feedback_no_spoilers]].
