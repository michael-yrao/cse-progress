---
name: reference_hellointerview_premium
description: problem link order is LeetCode (free) → NeetCode (free) → HelloInterview (premium, the learner subscribes) → progressiveoverflow (a spec is written so the page exists); each of the first three is checked against that site's own list, never guessed; nothing is skipped
metadata:
  type: reference
reconciled: 2026-10-04
---

**Link order for a problem, set by the learner Sep 27, 2026:**
*"leetcode (free) -> neetcode (free) -> hellointerview (premium) in that order"*

Extended the same day, when 1102 had none of the three: *"leetcode (free) -> neetcode (free) -> hellointerview
(premium) -> others"*. The learner wants every rep submitted somewhere; the paywalled LeetCode page is the last resort.

Replaced the fourth step Oct 4, 2026: *"new priority for problem links: leetcode (free) -> neetcode (free) -> hellointerview (premium) -> progressiveoverflow. if something doesn't exist in any of the above, make it available in progressiveoverflow"* (decision `problem-link-order-oct04`).

| Step | Use it when | How it is checked |
|---|---|---|
| 1. LeetCode | the problem is free there | LeetCode's GraphQL lookup: `isPaidOnly` is false |
| 2. NeetCode | LeetCode paywalls it AND NeetCode lists it | NeetCode's public problem list (`neetcode-gh/leetcode`, `.problemSiteData.json`) |
| 3. HelloInterview | neither of the above, AND its catalog has it | `hellointerview.yml`, built by crawling the catalog |
| 4. progressiveoverflow | none of the three carries it. (Oct 9 amendment, `problem-link-order-oct09`: in schedule rows and site lists the site link is ALSO a standing second link `[PO]` beside the external one whenever a spec exists; this row is then the external link only.) | `https://progressiveoverflow.com/practice/<n>`, label `PO`; a practice spec is written so the page exists. The spec's own `url:` keeps the problem's source page. Nothing is skipped. |

**The learner holds HelloInterview premium for coding**, not only system design (*"i have premium there so if a
problem is available there on premium, i can do it there"*). It is still the LAST resort, after both free sites.

⚠️ **This corrects what I first built the same day.** An hour earlier the learner picked "only when LeetCode is
paywalled" from a menu I wrote, and I implemented HelloInterview AHEAD of the NeetCode mirror. The learner then
stated the order outright. The menu never offered "NeetCode first", so the first answer was the nearest option,
not the rule. See `self_eval_log.md` 2026-09-27.

**Scope, as of Oct 4, 2026:** the learner had existing Kattis-linked rows relinked too: 9001 (after its rep), 9002, 9003 and 9004.

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
  | 1102 Path With Maximum Minimum Value | no | no | restored Oct 4 → progressiveoverflow (spec pending); was none free (LintCode 1418 is premium too) → skipped |
  | 1135 Connecting Cities With Minimum Cost | no | no | restored Oct 4 → progressiveoverflow (spec pending); was LeetCode, paywalled |

- On the site, a link's label is the judge's name in full ("HelloInterview"), per
  [[feedback_site_plain_language]].

Related: [[feedback_site_plain_language]], [[project_sd_mock_model]] (the learner's other use of the same
subscription).
