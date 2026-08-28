"""
269. Alien Dictionary   ·   https://neetcode.io/problems/foreign-dictionary
Pattern: graphs

There is a new alien language that uses the English alphabet, but the ORDER of the
letters is unknown to you. You are given a list `words` of words from the alien
language's dictionary, and the words are sorted lexicographically by the rules of
this new language.

Return a string of the unique letters in the new language, sorted in the new
language's order. If there is no solution, return "". If there are multiple
solutions, return any of them.

Note: a string `a` is lexicographically smaller than a string `b` if, at the first
position where they differ, `a`'s letter comes before `b`'s in the alien order. If
the first `min(len(a), len(b))` characters are equal, then `a` is smaller iff
`len(a) < len(b)`.

Example 1:
    Input:  words = ["wrt","wrf","er","ett","rftt"]
    Output: "wertf"

Example 2:
    Input:  words = ["z","x"]
    Output: "zx"

Example 3:
    Input:  words = ["z","x","z"]
    Output: ""          # the ordering is invalid — no valid alien order exists

Constraints:
    1 <= words.length <= 100
    1 <= words[i].length <= 100
    words[i] consists of only lowercase English letters.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-08-27 ──────────────
    def alienOrder_20260827(self, words: List[str]) -> str:
        pass

# ⤵ prior attempts stashed in dsa/leetcode/.history/269_alien_dictionary.txt — restored at session end (python scripts/restore_history.py)
