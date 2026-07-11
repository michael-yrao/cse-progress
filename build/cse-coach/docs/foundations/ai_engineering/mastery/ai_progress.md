# AI System Engineering Progress

<!--
Notes for the coach / future agents:
- SAME 7-column format and SAME interval engine as dsa_progress.md / design_progress.md.
  - "Difficulty" column -> the ROI-line **Tier** (Tier 1 practitioner core / Tier 2 depth).
  - "Problem" column     -> the **capability / build**, linked to its filled build doc
                            or component note (e.g. ../case_studies/rag_chat.md).
- The **unit** is a capability/build; the **rep** is filling a build template; the
  **review** is a BLIND REBUILD — design/rebuild the capability cold from memory,
  then compare. Score it 🟢/🟡/🔴 exactly like a DSA problem.
- Next Review Date is COMPUTED (Clean +30/+60, Retired +180, Shaky +10, Blank +2).
  No source-file discovery here — update rows by hand, then run:
      python scripts/update_review_dates.py --tracker \
          docs/foundations/ai_engineering/mastery/ai_progress.md
  (the pre-commit hook does this for you when this file is staged).
- Retire at streak 3 (🏆), spot-check every 180 days — same as the other pillars.
- Prerequisite: start this pillar only once System Design Tier 1 is largely retired.
- Replace the example row once you log your first blind rebuild.
-->

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Attempt Date | Attempt Dates |
|---|---|---|---|---|---|---|
| Tier 1 | [RAG Chat over a Private Corpus](../case_studies/rag_chat.md) | 🔴 | 0 |  |  |  |
