---
name: project_pending_oct14
description: Two learner-deferred tasks from the Oct 13, 2026 session, to pick up Oct 14 — interval coverage bar of 5 per flavour, and a one-key LeetCode copy tool
metadata:
  type: project
---

Deferred by the learner on Oct 13, 2026 ("let's tackle this tomorrow"). Neither has started; no file was edited for either.

1. **Interval coverage → 5 per flavour.** Learner wants each of the four interval techniques in
   `techniques.yml` at 5 problems. Mechanism: a `min_problems: 5` override per technique (it replaces
   the `coverage_threshold` floor) plus queued `surplus>=1` declarations to reach 5. Declared counts on
   Oct 13 (incl. queued): Merge & Insert 4 · Interval Scheduling 1 · Sweep Line 2 · Intersection 1.
   **Open question to the learner:** Intersection has only ~3 genuine problems (two LC-premium); cap it
   at 3, or 5 with filler? Never show the learner which new problem maps to which flavour (spoils the
   recognition call on a new problem). Needs a `decisions.yml` entry in the same edit.

2. **One-key LeetCode copy (`scripts/lc_copy.py`).** The pain: a dated attempt plus a module-level
   helper (`class UF_<stamp>`) must be copied as two blocks and renamed before pasting into LeetCode
   (1489). Plan awaiting approval: take the newest dated method in `class Solution`, add same-stamp
   module helpers plus undated helpers it references, strip `_YYYYMMDD`, prepend the file's imports +
   `class Solution:`, copy to clipboard (Windows: `clip` with UTF-16 input). Run from a committed
   `.vscode/tasks.json` task on `${file}`, bound to Ctrl+Alt+L in the user keybindings. One table-driven
   test. Proposed CLI line: `Copied 1489 · attempt 2026-10-13 (method + 1 helper) — paste into LeetCode.`
   Interim workaround offered: nest the helper class inside the method.

**Why:** the learner asked for both, then deferred them to the next session.
**How to apply:** raise both once at the Oct 14 kickoff (after the board), take the learner's answers,
then route the implementation through the execution workflow. Delete this file once both are settled.
