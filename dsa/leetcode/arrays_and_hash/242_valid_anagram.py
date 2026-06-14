"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.242_valid_anagram

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