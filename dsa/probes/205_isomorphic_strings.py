"""
205. Isomorphic Strings   ·   https://leetcode.com/problems/isomorphic-strings/
Pattern: 🎯 RECOGNITION PROBE — you name it. Do not look it up.

Given two strings `s` and `t`, determine if they are isomorphic.

Two strings are isomorphic if the characters in `s` can be replaced to get `t`:
every occurrence of a character must be replaced with the same character, order
preserved. No two characters may map to the same character, but a character may
map to itself.

    s = "egg",   t = "add"     ->  True
    s = "foo",   t = "bar"     ->  False    (o would have to map to both a and r)
    s = "paper", t = "title"   ->  True

Constraints:
    1 <= s.length <= 5 * 10^4
    t.length == s.length
    s and t consist of any valid ascii character

Before you write code, state: shape -> technique -> the ONE feature that picks it
over the nearest alternative.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        # f11 and b23 fail because 1 is already in map and value is not equal
        # what this means is also that they must be same length and that seems to be given
        # it is the same the other way as well, so we will just double map
        sToTMap = {}
        tToSMap = {}

        for i in range(len(s)):
            if s[i] in sToTMap and sToTMap[s[i]] != t[i]:
                return False
            if t[i] in tToSMap and tToSMap[t[i]] != s[i]:
                return False
            sToTMap[s[i]] = t[i]
            tToSMap[t[i]] = s[i]
        
        return True
