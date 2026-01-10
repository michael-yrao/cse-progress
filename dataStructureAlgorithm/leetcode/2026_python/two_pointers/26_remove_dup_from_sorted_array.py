"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.two_pointers.26_remove_dup_from_sorted_array
Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same.

Consider the number of unique elements in nums to be k​​​​​​​​​​​​​​. After removing duplicates, return the number of unique elements k.

The first k elements of nums should contain the unique numbers in sorted order. The remaining elements beyond index k - 1 can be ignored.

Custom Judge:

The judge will test your solution with the following code:

int[] nums = [...]; // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}

If all assertions pass, then your solution will be accepted.

Example 1:

Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).

Example 2:

Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).

Constraints:

    1 <= nums.length <= 3 * 104
    -100 <= nums[i] <= 100
    nums is sorted in non-decreasing order.

"""

from typing import List
import unittest

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # two pointer
        # l to keep track current duplicate index to be replaced
        # l-1 as a way to keep track of the most recent unique element
        # skip index 0 since we know it's unique and sorted

        if len(nums) == 1:
            return 1

        l = r = 1

        while r < len(nums):
            if nums[l-1] != nums[r]:
                nums[l] = nums[r]
                l+=1
            r+=1

        return l
    
class UnitTest(unittest.TestCase):
    
    input1 = [1,1,2]
    output1 = 2
    output1_array = [1,2]
    input2 = [0,0,1,1,1,2,2,3,3,4]
    output2 = 5
    output2_array = [0,1,2,3,4]

    def testremoveDuplicate1(self):
        result = Solution().removeDuplicates(self.input1)
        self.assertEqual(result, self.output1)

    def testremoveDuplicate2(self):
        result = Solution().removeDuplicates(self.input2)
        self.assertEqual(result, self.output2)

unittest.main()