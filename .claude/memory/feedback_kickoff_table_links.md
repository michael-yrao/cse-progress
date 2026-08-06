---
name: feedback_kickoff_table_links
description: hyperlink each problem to its local solution file AND its problem page (LC, or the NeetCode mirror if premium) — fires when new_problem.py runs, at kickoff, and on every problem/set transition
metadata:
  type: feedback
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

**How to apply:** in the kickoff table, render the problem cell as a markdown link to the
repo-relative `.py` path, and add an `LC` column (or inline `· [LC](url)`) to the LeetCode
URL. Applies to §2a kickoff and any lineup/preview table. **Also link on every transition:**
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

**CAVEAT — a retry's file link is a spoiler until scaffolded.** File links are safe in the
**kickoff** table because those items are scaffolded first (blank stub, prior attempts
stashed). In a **selection/candidate menu** where the learner hasn't picked yet, the retry
files are NOT scaffolded — opening one shows the old solution. So in a menu link **LC only**;
surface the local file link **only after** the pick is scaffolded. (Learned Jul 20 — linked
five unscaffolded retries and the learner opened one to their prior solution.) See
[[feedback_no_spoilers]].
