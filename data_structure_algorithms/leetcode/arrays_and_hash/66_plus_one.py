"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.66_plus_one

You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading 0's.

Increment the large integer by one and return the resulting array of digits.

 

Example 1:

Input: digits = [1,2,3]
Output: [1,2,4]
Explanation: The array represents the integer 123.
Incrementing by one gives 123 + 1 = 124.
Thus, the result should be [1,2,4].

Example 2:

Input: digits = [4,3,2,1]
Output: [4,3,2,2]
Explanation: The array represents the integer 4321.
Incrementing by one gives 4321 + 1 = 4322.
Thus, the result should be [4,3,2,2].

Example 3:

Input: digits = [9]
Output: [1,0]
Explanation: The array represents the integer 9.
Incrementing by one gives 9 + 1 = 10.
Thus, the result should be [1,0].

 

Constraints:

    1 <= digits.length <= 100
    0 <= digits[i] <= 9
    digits does not contain any leading 0's.

"""

from typing import List
import unittest

class Solution:
    def plusOneSolution1(self, digits: List[int]) -> List[int]:
        # iterate from last number in list
        # if digit is 9, set to 0 and continue
        # otherwise, add 1 and return
        # if we are out of loop without returning, it means it was all 9s
        # thus we add 1 in front of list

        # range(start, end, increment)
        for i in range(len(digits)-1,-1,-1):
            if digits[i] != 9:
                digits[i] += 1
                return digits
            digits[i] = 0

        return [1] + digits

class UnitTest(unittest.TestCase):
    test1 = [4,3,2,1]
    output1 = [4,3,2,2]
    test2 = [1,2,3]
    output2 = [1,2,4]

    def test1PlusOneSolution1(self):
        result = Solution().plusOneSolution1(self.test1)
        self.assertEqual(self.output1, result)
        
unittest.main()