---
name: reference_hellointerview_premium
description: problem link order is LeetCode (free) → NeetCode (free) → HelloInterview (premium, the learner subscribes); each step is checked against that site's own list, never guessed; planned problems only
metadata:
  type: reference
reconciled: 2026-09-27
---

**Link order for a problem, set by the learner Sep 27, 2026:**
*"leetcode (free) -> neetcode (free) -> hellointerview (premium) in that order"*

Extended the same day, when 1102 had none of the three: *"leetcode (free) -> neetcode (free) -> hellointerview
(premium) -> others"*. The learner wants every rep submitted somewhere; the paywalled LeetCode page is the last resort.

| Step | Use it when | How it is checked |
|---|---|---|
| 1. LeetCode | the problem is free there | LeetCode's GraphQL lookup: `isPaidOnly` is false |
| 2. NeetCode | LeetCode paywalls it AND NeetCode lists it | NeetCode's public problem list (`neetcode-gh/leetcode`, `.problemSiteData.json`) |
| 3. HelloInterview | neither of the above, AND its catalog has it | `hellointerview.yml`, built by crawling the catalog |
| 4. others | none of the three carries it | another judge that carries the same problem (Kattis, CSES, LintCode…), found by search and named in the file's header link; say plainly if it could not be confirmed free |
| none of the four | | SKIP the problem for now and look for a free problem of the same shape (learner, Sep 27: *"if nowhere available to practice it, we can skip it for now"*); a tracked problem keeps LeetCode's page, stated as paywalled |

**The learner holds HelloInterview premium for coding**, not only system design (*"i have premium there so if a
problem is available there on premium, i can do it there"*). It is still the LAST resort, after both free sites.

⚠️ **This corrects what I first built the same day.** An hour earlier the learner picked "only when LeetCode is
paywalled" from a menu I wrote, and I implemented HelloInterview AHEAD of the NeetCode mirror. The learner then
stated the order outright. The menu never offered "NeetCode first", so the first answer was the nearest option,
not the rule. See `self_eval_log.md` 2026-09-27.

**Scope: planned problems and future scaffolds only.** A tracked problem keeps the link it was solved against.

**How to apply:**
- **Never guess a mirror URL.** NeetCode's site answers 200 for any slug, so a NeetCode link for a problem
  NeetCode does not list is a dead link that looks alive. Check the list. Same for HelloInterview: a page
  counts only if it returns 200 AND links the same LeetCode slug.
- **NeetCode renames some problems** (Alien Dictionary → `foreign-dictionary`); `new_problem.py`'s
  `NEETCODE_RENAMES` holds the known ones. The list's `link` field is the LeetCode slug, not NeetCode's URL.
- **HelloInterview's slugs are not LeetCode's** (Meeting Rooms is `intervals/can-attend-meetings`). Join on the
  LeetCode slug the page links, never on the title. A summary of the catalog page is not evidence — a first
  summarised read reported Meeting Rooms as absent.
- As of Sep 27, 2026 the planned LeetCode-premium problems resolve as:

  | Problem | NeetCode lists it | HelloInterview has it | Link |
  |---|---|---|---|
  | 252 Meeting Rooms | yes | yes | NeetCode |
  | 253 Meeting Rooms II | yes | no | NeetCode |
  | 1197 Minimum Knight Moves | no | yes | HelloInterview |
  | 1102 Path With Maximum Minimum Value | no | no | none free (LintCode 1418 is premium too) → skipped |
  | 1135 Connecting Cities With Minimum Cost | no | no | LeetCode, paywalled |

- On the site, a link's label is the judge's name in full ("HelloInterview"), per
  [[feedback_site_plain_language]].

Related: [[feedback_site_plain_language]], [[project_sd_mock_model]] (the learner's other use of the same
subscription).
