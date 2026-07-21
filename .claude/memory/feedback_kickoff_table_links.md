---
name: feedback_kickoff_table_links
description: start-of-day kickoff table should hyperlink each problem to its local solution file AND its LeetCode page
metadata:
  type: feedback
---

When presenting the start-of-day (or any problem-lineup) table, make each problem a
clickable link. Provide **two** links per problem: the **local solution file** (relative
path, e.g. `[206 Reverse LL](dsa/leetcode/linked_list/206_reverse_linked_list.py)`) and
the **LeetCode page** (e.g. a separate `LC` link to `https://leetcode.com/problems/...`).

**Why:** the learner explicitly asked for it (Jul 20) — the file link opens the scaffold
in one click; the LC link is the canonical problem reference. Plain-text problem names cost
them a manual file hunt.

**How to apply:** in the kickoff table, render the problem cell as a markdown link to the
repo-relative `.py` path, and add an `LC` column (or inline `· [LC](url)`) to the LeetCode
URL. Applies to §2a kickoff and any lineup/preview table. Related: [[feedback_proactive_scheduling]].

**CAVEAT — a retry's file link is a spoiler until scaffolded.** File links are safe in the
**kickoff** table because those items are scaffolded first (blank stub, prior attempts
stashed). In a **selection/candidate menu** where the learner hasn't picked yet, the retry
files are NOT scaffolded — opening one shows the old solution. So in a menu link **LC only**;
surface the local file link **only after** the pick is scaffolded. (Learned Jul 20 — linked
five unscaffolded retries and the learner opened one to their prior solution.) See
[[feedback_no_spoilers]].
