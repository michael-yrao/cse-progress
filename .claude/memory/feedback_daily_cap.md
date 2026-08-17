---
name: feedback_daily_cap
description: SUPERSEDED Aug 7, 2026 — the daily problem COUNT was replaced by the effort budget (units). Do not schedule from this file.
metadata:
  type: feedback
reconciled: 2026-08-17
---

# ⚠️ SUPERSEDED — do not schedule from this file

**A day is budgeted in UNITS, not problems.** `units = comfort_base × difficulty`, against a ceiling.
**The rule is in `CLAUDE.md` ("Daily load is an EFFORT BUDGET, not a problem count"); the numbers are
in `cse.config.yml` under `effort_budget:` and nowhere else.** Price a day with:

```sh
python scripts/effort_budget.py --day 560 912 235 88 100 20
```

**Why this file is retired rather than deleted:** other memory files still link `[[feedback_daily_cap]]`,
and a dangling link that silently resolves to nothing is worse than a redirect. What it used to say —
*"never more than 5 problems a day"* — is not merely out of date, it is **actively wrong in three ways**
and would produce bad schedules if followed:

- **A count cannot tell a five-minute 🟢 Easy from a 🔴 Hard.** That is the whole reason the budget
  replaced it: three consecutive weeks were each "7 problems" and measured 5.5, 8.0 and 10.5 units.
- **It routed overflow to "Sunday's system-design sprint"**, which was retired Aug 13, 2026. SD is now
  a mock interview, lives in a separate repo, and since Aug 16 is **not priced against the day at all**.
- **It named a hard number (5)** while `cse.config.yml` said 7 and the effort budget said neither —
  three live answers, which is exactly the failure the *Single source of truth* rule now forbids.

**The one idea worth keeping**, and it survives in CLAUDE.md's schedule-integrity rule: *an item pushed
off a day must land on a named future slot in the same edit* — never dropped, never left dateless.

⚠️ **Never raise the ceiling to catch up on a backlog.** A rep rushed into a 🟡 costs far more, forever,
than the slot it saved. Demand sets the floor; the ceiling is a quality judgment and stays put.
