"""
Given an integer array nums of length n, you want to create an array ans of length 2n where ans[i] == nums[i] and ans[i + n] == nums[i] for 0 <= i < n (0-indexed).

Specifically, ans is the concatenation of two nums arrays.

Return the array ans.

 

Example 1:

Input: nums = [1,2,1]
Output: [1,2,1,1,2,1]
Explanation: The array ans is formed as follows:
- ans = [nums[0],nums[1],nums[2],nums[0],nums[1],nums[2]]
- ans = [1,2,1,1,2,1]

Example 2:

Input: nums = [1,3,2,1]
Output: [1,3,2,1,1,3,2,1]
Explanation: The array ans is formed as follows:
- ans = [nums[0],nums[1],nums[2],nums[3],nums[0],nums[1],nums[2],nums[3]]
- ans = [1,3,2,1,1,3,2,1]

 

Constraints:

    n == nums.length
    1 <= n <= 1000
    1 <= nums[i] <= 1000
"""

from typing import List
import unittest

class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        # python solution
        return nums * 2
    
    def getConcatenationAlternative(self, nums: List[int]) -> List[int]:
        # python solution
        return nums + nums

    def getConcatenationNonPython(self, nums: List[int]) -> List[int]:
        # create a list of size len(nums)*2
        # loop through new list, insert nums
        ans = []
        ansIterator = 0 
        while ansIterator < len(nums)*2:
            ans.append(nums[ansIterator%len(nums)])
            ansIterator+=1
        return ans
    
class UnitTest(unittest.TestCase):
    
    inputArray = [1,2,1]
    expectedAnswer = [1,2,1,1,2,1]

    def testConcatenationArrays(self):
        result = Solution().getConcatenation(self.inputArray)
        self.assertEqual(self.expectedAnswer, result)

    def testAlternativeSolution(self):
        result = Solution().getConcatenationAlternative(self.inputArray)
        self.assertEqual(self.expectedAnswer, result)

    def testNonPythonSolution(self):
        result = Solution().getConcatenationNonPython(self.inputArray)
        self.assertEqual(self.expectedAnswer, result)

unittest.main()