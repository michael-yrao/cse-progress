"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.169_majority_element

Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

 

Example 1:

Input: nums = [3,2,3]
Output: 3

Example 2:

Input: nums = [2,2,1,1,1,2,2]
Output: 2

 

Constraints:

    n == nums.length
    1 <= n <= 5 * 104
    -109 <= nums[i] <= 109
    The input is generated such that a majority element will exist in the array.

 
Follow-up: Could you solve the problem in linear time and in O(1) space?

"""

from typing import List
import unittest


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        freqMap = {}
        # not sure if we need both result and maxCount, TBD
        result, maxCount = 0, 0

        for n in nums:
            freqMap[n] = 1 + freqMap.get(n,0)
            result = n if freqMap[n] > maxCount else result
            maxCount = max(maxCount, freqMap[n])

        return result

    def majorityElementBoyerMoore(self, nums: List[int]) -> int:
        # boyer-moore algorithm assumes a single max exists
        # keep track of max and a counter
        # increment if sees max, decrement if not
        # set max to current element if counter = 0
        # also set counter = 1
        # return max
        maxElement, counter = nums[0], 0
        
        for n in nums:
            if maxElement == n:
                counter += 1
            else:
                counter -=1
                if counter == 0:
                    maxElement = n
                    counter = 1
        
        return maxElement
    
    def majorityElementBoyerMooreAlternative(self, nums: List[int]) -> int:
        # boyer-moore algorithm assumes a single max exists
        # keep track of max and a counter
        # increment if sees max, decrement if not
        # set max to current element if counter = 0
        # also set counter = 1
        # return max
        maxElement, counter = 0, 0
        
        for n in nums:
            if counter == 0:
                maxElement = n
            counter += (1 if maxElement == n else -1)

        return maxElement

class UnitTest(unittest.TestCase):
    input1 = [3,2,3]
    output1 = 3
    input2 = [2,2,1,1,1,2,2]
    output2 = 2

    def testMajorityElement1(self):
        result = Solution().majorityElement(self.input1)
        self.assertEqual(result, self.output1)

    
    def testMajorityElement2(self):
        result = Solution().majorityElement(self.input2)
        self.assertEqual(result, self.output2)

    def testMajorityElementBoyerMoore1(self):
        result = Solution().majorityElementBoyerMoore(self.input1)
        self.assertEqual(result, self.output1)

    
    def testMajorityElementBoyerMoore2(self):
        result = Solution().majorityElementBoyerMoore(self.input2)
        self.assertEqual(result, self.output2)

    def testMajorityElementBoyerMooreAlternative1(self):
        result = Solution().majorityElementBoyerMooreAlternative(self.input1)
        self.assertEqual(result, self.output1)

    
    def testMajorityElementBoyerMooreAlternative2(self):
        result = Solution().majorityElementBoyerMooreAlternative(self.input2)
        self.assertEqual(result, self.output2)

unittest.main()