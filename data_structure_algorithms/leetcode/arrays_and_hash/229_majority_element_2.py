"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.229_majority_element_2
Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.

Example 1:
Input: nums = [3,2,3]
Output: [3]

Example 2:
Input: nums = [1]
Output: [1]

Example 3:
Input: nums = [1,2]
Output: [1,2]

Constraints:

    1 <= nums.length <= 5 * 104
    -109 <= nums[i] <= 109

Follow up: Could you solve the problem in linear time and in O(1) space?
"""
from collections import defaultdict
from typing import List
import unittest

class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        # all return keys must have size bigger than minSize
        # double / for int, single / for float
        minSize = len(nums)//3
        
        # map of n -> freq(n)

        freqMap = defaultdict(int)

        for n in nums:
            freqMap[n] += 1
        
        returnList = []

        for key, value in freqMap.items():
            if value > minSize:
                returnList.append(key)
        
        return returnList
    
    def majorityElementBoyerMoore(self, nums: List[int]) -> List[int]:
        # all return keys must have size bigger than minSize
        minSize = len(nums)//3
        
        # map of n -> freq(n)
        freqMap = defaultdict(int)
        
        for n in nums:
            freqMap[n] += 1
            # we want to keep size of map to 2 or less
            # reason being there can only be 2 values in nums having freq > n/3
            if len(freqMap) <= 2:
                continue
            
            # we have 3 elements in freqMap
            # so let's decrement and clean out the map

            for n, count in freqMap.items():
                freqMap[n] = count - 1

            # cannot iterate over a map while popping
            # thus we convert the key of the map to a list and use that to pop
            # since map is at most O(3), this is still O(1) space
            for n in list(freqMap):
                if freqMap[n] == 0:
                    freqMap.pop(n)
            
        result = []

        # we can't just check the map for the frequency here
        # since we have been decrementing, their true size might be bigger than minSize

        for n in freqMap:
            # nums.count(n) is an O(n) operation but since freqMap is O(2), O(2*n) is still O(n)
            if nums.count(n) > minSize: 
                result.append(n)
        
        return result
    
class UnitTest(unittest.TestCase):
    input = [1,1,2,2,3,3,1,2]
    output = [1,2]

    def testBoyerMoore(self):
        result = Solution().majorityElementBoyerMoore(self.input)
        self.assertEqual(result, self.output)

unittest.main()