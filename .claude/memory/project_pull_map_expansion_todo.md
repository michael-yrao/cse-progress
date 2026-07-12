---
name: project_pull_map_expansion_todo
description: Pending — extend pull_interview.py's pattern map to expansion techniques once the learner starts retiring them (segment tree, KMP, etc.)
metadata:
  type: project
---

**Pending task, triggered by the expansion phase.** `scripts/pull_interview.py` gates the interview pull pool by learned patterns, but its `CATEGORY_TO_TOPICS` / `FOLDER_TO_CATEGORY` maps currently cover only **NC150 categories**. Post-NC150 the pool is already wide (all NC150 topics), so this doesn't bite immediately — but once the learner begins **retiring expansion techniques** (segment tree, Fenwick/BIT, KMP, suffix structures, Tarjan's, etc.), those newly-learned techniques won't widen the pull pool until the maps are extended.

**Trigger:** when the learner starts logging/retiring problems in an expansion technique (Tier 1 or Tier 2 of the Knowledge Expansion Queue).

**How to apply:** extend the two maps in `pull_interview.py` (there's a pre-staged TODO block with the exact technique → LeetCode-topic entries): add the expansion solution-folder slugs to `FOLDER_TO_CATEGORY`, and the technique → topic tags to `CATEGORY_TO_TOPICS` (e.g. Segment Tree → "Segment Tree", KMP → "String Matching", Suffix → "Suffix Array"). Then a retired expansion technique automatically starts pulling matching interview problems. Relates to [[feedback_expansion_pull_scheduling]].
