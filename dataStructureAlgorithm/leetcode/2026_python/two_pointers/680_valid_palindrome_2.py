"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.two_pointers.680_valid_palindrome_2

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
    def validPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            # if not equal, check substr of each side
            # but we have to consider 
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