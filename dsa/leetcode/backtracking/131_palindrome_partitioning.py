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

    # ── Attempt · 2026-10-04 ──────────────
    def partition_20261004(self, s: str) -> List[List[str]]:
        # if we use abba as an example, we cant build on a path incrementally
        # since abb is not a palindrome but abba is
        # what this means is we need a start index and end index to track, we also should determine if we want to do inclusive or exclusive for end index. let's do exclusive
        # path: current list of palindrome for this string
        # state: start index of potential palindrome, end index of potential palindrome
        # decision: choose vs not choose
        # validity: choose only if substr[start:end] is palindrome
        #   choose: add substr[start:end] to path and go down the tree via end -> end + 1
        #   not choose: path unchanged, go breadth via start -> end + 1
        # base case: end+1 tells us that we looked at all the strings but start tells us whether or not we added it to a result yet. so if start >= len(s) then we add as a result, if end > len(s) and it did not hit the start case, there is no palindrome possible this route

        result = []

        def isPalindrome(string):
            return string==string[::-1]

        def backtrack(path, start, end):
            # base case
            if start >= len(s):
                result.append(path.copy())
                return
            
            # since we don't include end, we need to check if end > len(s)
            if end > len(s):
                return
            
            # validity and decision #1
            if isPalindrome(s[start:end]):
                path.append(s[start:end])
                backtrack(path, end, end + 1)
                # backtrack
                path.pop()
            # decision #2
            backtrack(path, start, end + 1)
        
        backtrack([],0,1)

        return result

    # ── Attempt · 2026-10-02 ──────────────
    def partition_20261002(self, s: str) -> List[List[str]]:
        # substring, so that means everything has a start and an end
        # so we can't just pick randomly, we need to do substring[start:end]
        # path: list of palindromes
        # state: start and end indices for the substring
        # validity: if substring[start:end] is a palindrome
        # decision: if palindrome, pick and do backtrack of end:end+1. if not palindrome, just move end+1
        # base case: if start >= len(s), add array. when this is true, that means we covered all chars.
        # if end > len(s), it means we are now passed all chars, do a return

        result = []

        def isPalindrome(string):
            return string==string[::-1]

        def backtrack(path, start_index, end_index):
            if start_index >= len(s):
                result.append(path.copy())
                return
            if end_index > len(s):
                return

            # validity
            # decision #1: pick
            if isPalindrome(s[start_index:end_index]):
                path.append(s[start_index:end_index])
                backtrack(path, end_index, end_index + 1)
                path.pop()
            
            # decision #2: do not pick
            backtrack(path, start_index, end_index + 1)
            
        backtrack([], 0, 1)
        return result

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
