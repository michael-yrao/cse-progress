"""
Docstring for dsa.leetcode.two_pointers.680_valid_palindrome_2

Given a string s, return true if the s can be palindrome after deleting at most one character from it.

Example 1:

Input: s = "aba"
Output: true

Example 2:

Input: s = "abca"
Output: true
Explanation: You could delete the character 'c'.

Example 3:

Input: s = "abc"
Output: false

 

Constraints:

    1 <= s.length <= 105
    s consists of lowercase English letters.
"""

class Solution:

    # ── Attempt · 2026-08-13 ──────────────
    def validPalindrome_20260813(self, s: str) -> bool:
        # deleting single element just means we check again after skipping this current unmatched
        # so standard valid palindrome, but if its false, check both sides
        l, r = 0, len(s) - 1

        def isPalindrome(left,right):
            while left < right:
                if s[left] != s[right]:
                    return False
                left+=1
                right-=1
            return True

        while l < r:
            if s[l] != s[r]:
                return isPalindrome(l+1,r) or isPalindrome(l,r-1)
            l+=1
            r-=1
        return True

    def validPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            # if not equal, check string if we skipped
            # either the left side OR the right side
            if s[l] != s[r]:
                # left skip
                leftSkip = s[l+1:r+1]
                # right skip
                rightSkip = s[l:r]
                return leftSkip == leftSkip[::-1] or rightSkip == rightSkip[::-1]
            # if s[l] == s[r], we just increment
            l+=1
            r-=1
        return True
    
    def validPalindromeVariation(self, s: str) -> bool:
        # main scenarios that come to mind are these
        # abca -> True
        # abcbda -> True
        # two pointer but do a skip ahead check for both sides

        def skippable(l,r):
            while l < r:
                if s[l] == s[r]:
                    # continue
                    l+=1
                    r-=1
                else:
                    return False
            return True

        l, r = 0, len(s)-1
        while l < r:
            if s[l] == s[r]:
                # continue
                l+=1
                r-=1
            else:
                # otherwise, we check if we can skip either sides
                return skippable(l+1, r) or skippable(l,r-1)
        return True
