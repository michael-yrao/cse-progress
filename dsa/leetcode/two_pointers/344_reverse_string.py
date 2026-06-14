"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.two_pointers.344_reverse_string
344. Reverse String
Solved
N/A
Topics
premium lock iconCompanies
Hint

Write a function that reverses a string. The input string is given as an array of characters s.

You must do this by modifying the input array in-place with O(1) extra memory.

Example 1:

Input: s = ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]

Example 2:

Input: s = ["H","a","n","n","a","h"]
Output: ["h","a","n","n","a","H"]

Constraints:

    1 <= s.length <= 105
    s[i] is a printable ascii character.

"""

from typing import List

class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        l, r = 0, len(s) - 1
        while r>l:
            s[l], s[r] = s[r], s[l]
            r-=1
            l+=1