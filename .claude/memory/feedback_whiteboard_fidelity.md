---
name: feedback_whiteboard_fidelity
description: Write the full solution from scratch every time, including ListNode/TreeNode/TrieNode definitions — no shared data-model module to import
metadata:
  type: feedback
---

Every solution is written in full from a blank page, including any data-structure definitions it needs (`ListNode`, `TreeNode`, `TrieNode`, `Node`, …). There is **no shared `datamodel` / boilerplate module to import** — re-deriving the scaffolding is part of the rep, exactly as on an interview whiteboard.

**Why:** The user wanted the rules tightened to match cse-coach's whiteboard-fidelity lock. Importing boilerplate skips reps you should be able to reproduce cold under interview conditions.

**How to apply:** Don't introduce or suggest a shared data-model module. When the user solves a linked-list/tree/trie problem, they define the node class inline in that file. The agent still never writes solution logic or data-structure definitions — the learner writes every line. Relates to [[feedback_coding_for_clean]] and [[feedback_no_code_edits]].
