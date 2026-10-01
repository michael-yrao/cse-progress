"""
131. Palindrome Partitioning   ·   https://leetcode.com/problems/palindrome-partitioning/
Pattern: backtracking

Given a string `s`, partition `s` such that every substring of the partition is a
palindrome. Return all possible palindrome partitionings of `s`.

Example 1:
    Input:  s = "aab"
    Output: [["a","a","b"],["aa","b"]]

Example 2:
    Input:  s = "a"
    Output: [["a"]]

Constraints:
    1 <= s.length <= 16
    s contains only lowercase English letters.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:
    # ── Attempt 1 · 2026-09-30 ────────────────────────────────────────────
    def partition(self, s: str) -> List[List[str]]:
        # all possible palindrome is obviously backtracking
        # one thing we have to notice here is for "abba", abba is a palindrome but the nodes leading to it is not so we just need to add and check at base case
        # we would never skip a character, so we wouldn't necessarily loop and jump around
        # path: current palindrome string
        # state: starting index
        # validity: if this substring starting at start and end at end makes a palindrome
        # choice: whether or not to end the string at current index in loop
        # base case: if current path is palindrome, add into result and return; if current index >= len(s), return

        result = []

        def isPalindrome(string):
            if not string or string == '':
                return False
            l = 0
            r = len(string) - 1
            while l < r:
                if string[l] != string[r]:
                    return False
                l+=1
                r-=1
            return True
        
        def backtrack(path, start_index):
            if start_index >= len(s):
                result.append(path.copy())
                return
            
            for end in range(start_index, len(s)):
                substring = s[start_index:end+1]
                if isPalindrome(substring):
                    # backtrack with start being end + 1
                    backtrack(path + [substring], end + 1)
                    
        backtrack([], 0)
        return result