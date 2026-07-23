"""
Docstring for dsa.leetcode.arrays_and_hash.242_valid_anagram

Given two strings s and t, return true if t is an

of s, and false otherwise.

 

Example 1:

Input: s = "anagram", t = "nagaram"

Output: true

Example 2:

Input: s = "rat", t = "car"

Output: false

 

Constraints:

    1 <= s.length, t.length <= 5 * 104
    s and t consist of lowercase English letters.
"""

import unittest


class Solution:

    # ── Attempt · 2026-07-22 ──────────────
    def isAnagram_20260722(self, s: str, t: str) -> bool:
        sArray = [0] * 26
        tArray = [0] * 26

        for char in s:
            index = ord(char) - ord('a')
            sArray[index]+=1
        
        for char in t:
            index = ord(char) - ord('a')
            tArray[index]+=1
        
        return sArray==tArray

    def isAnagram(self, s: str, t: str) -> bool:
        # anagrams are same length
        # anagrams are the same if sorted
        # anagrams also have the same # of each char, so hashmap
        sMap, tMap = {}, {}

        if len(s) != len(t): 
            return False
        
        for i in range(len(s)):
            sMap[s[i]] = 1 + sMap.get(s[i],0)
            tMap[t[i]] = 1 + tMap.get(t[i],0)

        return sMap == tMap

    def isAnagramPython(self, s: str, t: str) -> bool:
        return ''.join(sorted(s)) == ''.join(sorted(t))
    
    def isAnagram_20260622(self, s: str, t: str) -> bool:
        sMap, tMap = {}, {}

        for char in s:
            sMap[char] = sMap.get(char,0) + 1
        
        for char in t:
            tMap[char] = tMap.get(char,0) + 1
        
        return sMap == tMap
    
class UnitTest(unittest.TestCase):
    test1A = "anagram"
    test1B = "nagaram"
    test1Result = True

    test2A = "rat"
    test2B = "car"
    test2Result = False

    def testIsAnagram1(self):
        result = Solution().isAnagramPython(self.test1A, self.test1B)
        self.assertEqual(self.test1Result, result)
    
    def testIsAnagram2(self):
        result = Solution().isAnagramPython(self.test2A, self.test2B)
        self.assertEqual(self.test2Result, result)

    def testIsAnagram3(self):
        result = Solution().isAnagram(self.test1A, self.test1B)
        self.assertEqual(self.test1Result, result)
    
    def testIsAnagram4(self):
        result = Solution().isAnagram(self.test2A, self.test2B)
        self.assertEqual(self.test2Result, result)

unittest.main()
