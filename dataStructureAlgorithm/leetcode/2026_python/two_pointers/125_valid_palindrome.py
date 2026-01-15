"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.two_pointers.125_valid_palindrome
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

 

Example 1:

Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Example 3:

Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

Constraints:

    1 <= s.length <= 2 * 105
    s consists only of printable ASCII characters.
"""

import re


class Solution:
    def isPalindrome(self, s: str) -> bool:
        # clean string to alphabet only
        # also make it lowercase
        regex = re.compile('[^a-zA-Z]')
        cleanString = regex.sub('', s).lower()
        
        l,r=0,len(cleanString)-1
        while r>=l:
            if cleanString[l] != cleanString[r]:
                return False
            l+=1
            r-=1
        return True

    def isPalindromeNoCleaning(self, s: str) -> bool:
        
        def alphaNumeric(character):
            return ((ord('A') <= ord(character) <= ord('Z')) or
                    (ord('a') <= ord(character) <= ord('z')) or
                    (ord('0') <= ord(character) <= ord('9'))
                    )
        
        l, r = 0, len(s) - 1

        while r >= l:
            # get to alphanumeric for both l and r
            while l < r and not alphaNumeric(s[l]):
                l+=1
            while r > l and not alphaNumeric(s[r]):
                r-=1
            if s[r].lower() != s[l].lower():
                return False
            r-=1
            l+=1
        return True