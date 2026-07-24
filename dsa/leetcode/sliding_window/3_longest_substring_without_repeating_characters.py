"""
3. Longest Substring Without Repeating Characters   ·   https://leetcode.com/problems/longest-substring-without-repeating-characters/
Pattern: sliding_window

Given a string s, return the length of the longest substring without repeating
characters. A substring is a contiguous, non-empty run of characters.

Examples:
  s = "abcabcbb" -> 3   ("abc")
  s = "bbbbb"    -> 1   ("b")
  s = "pwwkew"   -> 3   ("wke"; "pwke" is a subsequence, not a substring)

Constraints: 0 <= len(s) <= 5*10^4; s may contain letters, digits, symbols, spaces.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import math
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-07-23 ────────────────────────────────────────────
    def lengthOfLongestSubstring(self, s: str) -> int:
        # no repeating characters = set
        # longest substring = dynamic sliding window
        
        if not s:
            return 0
        
        maxLength = -math.inf
        l, r = 0, 0
        charSet = set()

        while r < len(s):
            while s[r] in charSet:
                charSet.remove(s[l])
                l+=1
            # now that we know r is unique, we add it in
            charSet.add(s[r])
            # compare max size to maxLength
            maxLength = max(maxLength, r - l + 1)
            r+=1
        
        return maxLength