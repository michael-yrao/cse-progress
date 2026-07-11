"""
Given a circular integer array nums (i.e., the next element of nums[nums.length - 1] is nums[0]), return the next greater number for every element in nums.

The next greater number of a number x is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, return -1 for this number.

Example 1:

Input: nums = [1,2,1]
Output: [2,-1,2]
Explanation: The first 1's next greater number is 2; 
The number 2 can't find next greater number. 
The second 1's next greater number needs to search circularly, which is also 2.

Example 2:

Input: nums = [1,2,3,4,3]
Output: [2,3,4,-1,4]

Constraints:

    1 <= nums.length <= 104
    -109 <= nums[i] <= 109
"""
from typing import List

class Solution:
    def nextGreaterElements_20260711(self, nums: List[int]) -> List[int]:
        # circular array, what does this mean exactly?
        # looking at the example, index 2's next greater is index 1
        # initial idea is to double nums so we can simulate going through it twice
        # but a better idea is to actually just do i in range(len(nums)*2)
        # and then use modular arithmetic to get the mapping
        # so like other next greater problems, we use a map to map num -> next greater
        # and do a monotonic decreasing stack so when we see a greater number, we know that is the next greater

        result = [-1] * len(nums)
        decreasingStack = []
        numSize = len(nums)

        for i in range(2*numSize):
            currentNumberIndex = i%numSize
            while decreasingStack and nums[currentNumberIndex] > nums[decreasingStack[-1]]:
                priorNumberIndex = decreasingStack.pop()
                if result[priorNumberIndex] == -1:
                    result[priorNumberIndex] = nums[currentNumberIndex]
            # now that we are decreasing, insert current number into stack
            decreasingStack.append(currentNumberIndex)
        
        return result
        