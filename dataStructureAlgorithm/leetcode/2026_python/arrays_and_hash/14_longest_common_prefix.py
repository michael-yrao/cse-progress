"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.14_longest_common_prefix

You are given an array of strings strs. Return the longest common prefix of all the strings.

If there is no longest common prefix, return an empty string "".

Example 1:

Input: strs = ["bat","bag","bank","band"]

Output: "ba"

Example 2:

Input: strs = ["dance","dag","danger","damage"]

Output: "da"

Example 3:

Input: strs = ["neet","feet"]

Output: ""

Constraints:

    1 <= strs.length <= 200
    0 <= strs[i].length <= 200
    strs[i] is made up of lowercase English letters if it is non-empty.


"""

from typing import List
import unittest

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        prefix = ""

        # use one of the strings for us to iterate through
        # we'll use 0
        # compare char at index i for every string in the list
        # if we pass length of current string, we return prefix
        # if we find a char that is not equal to strs[0][i], we return

        for i in range(len(strs[0])):
            for string in strs:
                if i == len(string) or string[i] != strs[0][i]: 
                    return prefix
            prefix += strs[0][i]
        return prefix
    
    def longestCommonPrefixGreedy(self, strs: List[str]) -> str:
                
        # instead of using strs[0], we can also be greedy by using the shortest word
        # then iterate through the list checking against the shortestWord
        
        prefix = ""
        shortestWord = min(strs, key=len)

        for i, char in enumerate(shortestWord):
            for string in strs:
                if char != string[i]:
                    return prefix
            prefix += char

        return prefix
    
    def longestCommonPrefixGreedyPython(self, strs: List[str]) -> str:
        
        # instead of using strs[0], we can also be greedy by using the shortest word
        # then iterate through the list checking against the shortestWord
        
        shortestWord = min(strs, key=len)

        for i, char in enumerate(shortestWord):
            for string in strs:
                if char != string[i]:
                    # return shortestWord from index 0 to i (exclusive of i)
                    return shortestWord[:i]

        # if we are here, that means we matched all so we return the full word        
        return shortestWord

    def minLengthStr(self, strs: List[str]) -> str:
        shortestString = strs[0]

        for string in strs:
            if len(string) < shortestString:
                shortestString = string
        
        return shortestString


class UnitTest(unittest.TestCase):

    test1 = ["bat","bag","bank","band"]
    output1 = "ba"
    test2 = ["dance","dag","danger","damage"]
    output2 = "da"
    test3 = ["neet","feet"]
    output3 = ""

    def testLongestCommonPrefix1(self):
        result = Solution().longestCommonPrefix(self.test1)
        self.assertEqual(self.output1,result)

    
    def testLongestCommonPrefix2(self):
        result = Solution().longestCommonPrefix(self.test2)
        self.assertEqual(self.output2,result)    

    def testLongestCommonPrefixGreedy1(self):
        result = Solution().longestCommonPrefixGreedy(self.test1)
        self.assertEqual(self.output1,result)

    
    def testLongestCommonPrefixGreedy2(self):
        result = Solution().longestCommonPrefixGreedy(self.test2)
        self.assertEqual(self.output2,result) 

    def testLongestCommonPrefixGreedyPython1(self):
        result = Solution().longestCommonPrefixGreedyPython(self.test1)
        self.assertEqual(self.output1,result)

    
    def testLongestCommonPrefixGreedyPython2(self):
        result = Solution().longestCommonPrefixGreedyPython(self.test2)
        self.assertEqual(self.output2,result) 

unittest.main()