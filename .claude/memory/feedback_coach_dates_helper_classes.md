---
name: feedback_coach_dates_helper_classes
description: The learner writes helper classes with natural names; the COACH dates them (TrieNode → TrieNode_20260822) at rating time, never the learner
metadata:
  type: feedback
reconciled: 2026-08-30
---

**The learner writes helper classes (`TrieNode`, `Node`, `ListNode`) with their natural names —
the names they'd write on LeetCode or in an interview. The COACH renames them to the dated form
(`TrieNode_20260822`) at rating/close-out time, before `restore_history.py` runs.** Never ask the
learner to date a helper.

**Why:** The dated-helper requirement exists only to stop today's helper from colliding with a
prior attempt's same-named helper when `restore_history.py` merges the stash back (Python keeps the
*last* definition, so today's code silently picks up the wrong class — the 208 TrieNode incident).
That is a **repo-tooling artifact**, not real practice. Forcing it onto the learner's code trains an
unnatural habit: *"the user shouldn't have to rename since I wouldn't name it like that when I am
practicing and writing on LC or in an interview"* (learner, Aug 22, 2026, on 211).

**How to apply:**
- At rating time, if today's attempt defines an undated top-level helper class, **rename it +
  every reference** to `<Name>_<YYYYMMDD>` yourself (one `replace_all` — but check it didn't also
  hit illustrative text in the scaffold banner, e.g. `(Node, TrieNode, …)`, and revert that).
- Do this **before** `restore_history.py` at close-out, or the merge collides and the restore warns.
- The scaffold banner still *asks* for the dated name — that's a belt-and-suspenders reminder, now
  addressed to the coach rather than the learner.

⚠️ **Upstream angle ([[project_upstream_candidates]]):** the real fix is source-side — restore could
auto-namespace an undated helper in today's attempt. But restore's load-bearing invariant is that it
**never parses the prior-attempt slice**, and auto-renaming reaches into an attempt, so this is not a
trivial change. Until then, the coach-renames policy above is the pragmatic fix.
