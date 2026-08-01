---
name: feedback_kickoff_table_links
description: hyperlink each problem to its local solution file AND its LeetCode page — fires when new_problem.py runs, at kickoff, and on every problem/set transition
metadata:
  type: feedback
---

**PRIMARY TRIGGER — a scaffold is a link event. Every `new_problem.py` run ends with the
links, in the same reply, unprompted.** If the script wrote a file, the reply reporting that
names the file as a clickable link + its LC link. No exceptions, no waiting to be asked, and
not deferred to a later lineup table. *(Set by the learner Jul 31: "when anything is scaffolded,
we should be given the link so we can start the work on them.")*

**ENFORCED BY HOOK (Jul 31, 2026).** `.claude/hooks/scaffold_links_reminder.py` fires as a
`PostToolUse`/`Bash` hook on any command containing `new_problem.py` and injects this reminder.
Wired in `.claude/settings.json`, version-controlled, so it travels across machines. This rule no
longer depends on my recall — but keep the prose: the hook fires the reminder, it can't write the
links for me, and it cannot fire on the *hand-over* and *lineup-table* cases below.

Why this is the trigger and the table is not: the rule was written against the **kickoff table**
and has now lapsed five times (Jul 20, 21, 23, 30, 31) — every time the output format stopped
being a table. A rule anchored to an *artifact* decays when the artifact changes; a rule anchored
to a *tool invocation* cannot. Scaffolding is also the exact moment the file link becomes **safe**
(see caveat below), so the trigger and the safety condition are the same event.

Beyond the scaffold, the same two links apply when presenting the start-of-day (or any
problem-lineup) table. Provide **two** links per problem: the **local solution file** (relative
path, e.g. `[206 Reverse LL](dsa/leetcode/linked_list/206_reverse_linked_list.py)`) and
the **LeetCode page** (e.g. a separate `LC` link to `https://leetcode.com/problems/...`).

**Why:** the learner explicitly asked for it (Jul 20) — the file link opens the scaffold
in one click; the LC link is the canonical problem reference. Plain-text problem names cost
them a manual file hunt.

**How to apply:** in the kickoff table, render the problem cell as a markdown link to the
repo-relative `.py` path, and add an `LC` column (or inline `· [LC](url)`) to the LeetCode
URL. Applies to §2a kickoff and any lineup/preview table. **Also link on every transition:**
whenever moving on to the next problem or starting a new set mid-session, restate the
problem(s) with both links — don't make the learner scroll back to the kickoff table
(reaffirmed Jul 21). Related: [[feedback_proactive_scheduling]].

**CAVEAT — a retry's file link is a spoiler until scaffolded.** File links are safe in the
**kickoff** table because those items are scaffolded first (blank stub, prior attempts
stashed). In a **selection/candidate menu** where the learner hasn't picked yet, the retry
files are NOT scaffolded — opening one shows the old solution. So in a menu link **LC only**;
surface the local file link **only after** the pick is scaffolded. (Learned Jul 20 — linked
five unscaffolded retries and the learner opened one to their prior solution.) See
[[feedback_no_spoilers]].
