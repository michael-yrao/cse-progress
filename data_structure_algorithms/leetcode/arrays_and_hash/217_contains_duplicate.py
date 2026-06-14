"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.217_contains_duplicate

Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

 

Example 1:

Input: nums = [1,2,3,1]

Output: true

Explanation:

The element 1 occurs at the indices 0 and 3.

Example 2:

Input: nums = [1,2,3,4]

Output: false

Explanation:

All elements are distinct.

Example 3:

Input: nums = [1,1,1,3,3,4,3,2,4,2]

Output: true

 

Constraints:

    1 <= nums.length <= 105
    -109 <= nums[i] <= 109

"""

from typing import List
import unittest

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # since we only care about if it contains duplicates
        # what we can do is just iterate til we see a duplicate
        # question is how do we keep track of duplicates or if we need to
        numsSet = set()

        for integer in nums:
            if integer in numsSet:
                return True
            else:
                numsSet.add(integer)

        return False
    
    def containsDuplicateAlternative(self, nums: List[int]) -> bool:
        # since we only care about if it contains duplicates
        # we can check if when we convert this list to a set
        # whether or not the lengths are equal
        # this solution is still O(n) in both space and time
        # since python is still creating the set

        # returns true if len of the set is shorter than the length of the original list
        return len(set(nums)) < len(nums)

class UnitTest(unittest.TestCase):

    test1 = [1,2,3,1]
    test2 = [1,2,3,4]
    test3 = [1,1,1,3,3,4,3,2,4,2]
    expectedOutput1 = True
    expectedOutput2 = False
    expectedOutput3 = True

    def testContainsDuplicate1(self):
        result1 = Solution().containsDuplicate(self.test1)
        self.assertEqual(self.expectedOutput1, result1)
    
    def testContainsDuplicate2(self):
        result2 = Solution().containsDuplicate(self.test2)
        self.assertEqual(self.expectedOutput2, result2)

    def testContainsDuplicate3(self):
        result3 = Solution().containsDuplicate(self.test3)
        self.assertEqual(self.expectedOutput3, result3)

    def testContainsDuplicateAlternative1(self):
        result1 = Solution().containsDuplicateAlternative(self.test1)
        self.assertEqual(self.expectedOutput1, result1)
    
    def testContainsDuplicateAlternative2(self):
        result2 = Solution().containsDuplicateAlternative(self.test2)
        self.assertEqual(self.expectedOutput2, result2)

    def testContainsDuplicateAlternative3(self):
        result3 = Solution().containsDuplicateAlternative(self.test3)
        self.assertEqual(self.expectedOutput3, result3)
                         
unittest.main()