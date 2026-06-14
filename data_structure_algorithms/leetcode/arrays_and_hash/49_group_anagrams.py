"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.49_group_anagrams

Given an array of strings strs, group the

together. You can return the answer in any order.

 

Example 1:

Input: strs = ["eat","tea","tan","ate","nat","bat"]

Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Explanation:

    There is no string in strs that can be rearranged to form "bat".
    The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.
    The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.

Example 2:

Input: strs = [""]

Output: [[""]]

Example 3:

Input: strs = ["a"]

Output: [["a"]]

 

Constraints:

    1 <= strs.length <= 104
    0 <= strs[i].length <= 100
    strs[i] consists of lowercase English letters.

"""

from collections import defaultdict
from typing import List
import unittest

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagramMap = {}
        for str in strs:
            sortedStr = ''.join(sorted(str))
            # need to initialize key if we use default map
            # otherwise, we run into KeyError issue
            if sortedStr not in anagramMap:
                anagramMap[sortedStr] = []
            anagramMap[sortedStr].append(str)
        return list(anagramMap.values())
    
    def groupAnagramsAlternative(self, strs: List[str]) -> List[List[str]]:
        # preferred concise and idiomatic code since 
        # defaultdict stores default empty list for non-existing keys
        anagramMap = defaultdict(list)
        for str in strs:
            sortedStr = ''.join(sorted(str))
            anagramMap[sortedStr].append(str)
        return list(anagramMap.values())

class UnitTest(unittest.TestCase):
    input1 = ["eat","tea","tan","ate","nat","bat"]
    output1 = [["bat"],["nat","tan"],["ate","eat","tea"]]
    input2 = [""]
    output2 = [[""]]
    input3 = ["a"]
    output3 = [["a"]]

    def testGroupAnagrams1(self):
        result = Solution().groupAnagrams(self.input1)
        self.assertEqual(result, self.output1)
    
    def testGroupAnagrams2(self):
        result = Solution().groupAnagrams(self.input2)
        self.assertEqual(result, self.output2)

    def testGroupAnagrams3(self):
        result = Solution().groupAnagrams(self.input3)
        self.assertEqual(result, self.output3)

    def testGroupAnagramsAlternative1(self):
        result = Solution().groupAnagramsAlternative(self.input1)
        self.assertEqual(result, self.output1)
    
    def testGroupAnagramsAlternative2(self):
        result = Solution().groupAnagramsAlternative(self.input2)
        self.assertEqual(result, self.output2)

    def testGroupAnagramsAlternative3(self):
        result = Solution().groupAnagramsAlternative(self.input3)
        self.assertEqual(result, self.output3)

unittest.main()