"""
399. Evaluate Division   ·   https://leetcode.com/problems/evaluate-division/
Pattern: graphs

You are given `equations` like ["a","b"] with `values` like 2.0, meaning a / b = 2.0.
Each variable is a string; all values are positive.

Answer each query ["c","d"] with the value of c / d, using the known equations
(chaining them as needed). If the answer can't be determined — an unknown variable,
or two variables not connected by any chain — return -1.0 for that query.

Return a list of answers, one per query, in order.

Example: equations = [["a","b"],["b","c"]], values = [2.0, 3.0],
queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
→ [6.0, 0.5, -1.0, 1.0, -1.0]
Constraints: 1 ≤ equations.length ≤ 20; 1 ≤ queries.length ≤ 20; variable names 1–5 lowercase letters.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-10 ────────────────────────────────────────────
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        pass
