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
import math
from typing import List

class Solution:

    # ── Attempt · 2026-08-14 ──────────────
    def nextGreaterElements_20260814(self, nums: List[int]) -> List[int]:
        # next greater = monotonically decreasing stack
        # so we keep the index in the stack so we can set the next greater for prior index
        # circular means we need to through twice, store only real indices

        decreasingStack = []
        result = [-1] * len(nums)

        for i in range(len(nums)*2):
            actualIndex = i % len(nums)
            # when we hit something that breaks the decreasing stack
            # we mark it on our result
            while decreasingStack and nums[actualIndex] > nums[decreasingStack[-1]]:
                priorIndex = decreasingStack.pop()
                # if we haven't filled in next greater yet
                if result[priorIndex] == -1:
                    result[priorIndex] = nums[actualIndex]
            # now we add actual index to the stack
            decreasingStack.append(actualIndex)
        
        return result

    # ── Attempt · 2026-08-10 ──────────────
    def nextGreaterElements_20260810(self, nums: List[int]) -> List[int]:
        # next greater element = monotonic stack
        # stack should be decreasing so when something is increasing, it is the next greater
        # we will store the index in the stack
        # circular = go through the array twice
        # initialize our nextGreater with -1 to indicate no next greater
        nextGreater = [-1] * len(nums)
        decreasingStack = []

        for i in range(len(nums)*2):
            actualIndex = i%(len(nums))
            # check if current element is bigger than prior element
            while decreasingStack and nums[actualIndex] > nums[decreasingStack[-1]]:
                # actualIndex is bigger, so this is prior element's next greater
                nextGreaterNumber = nums[actualIndex]
                priorIndex = decreasingStack.pop()
                # we do have to check if this element already has a next greater since we are looping through twice. If it does, skip it, otherwise, assign it
                if nextGreater[priorIndex] == -1:
                    nextGreater[priorIndex] = nextGreaterNumber
            # insert index into stack
            decreasingStack.append(actualIndex)
        
        return nextGreater

    # ── Attempt · 2026-07-31 ──────────────
    def nextGreaterElements_20260731(self, nums: List[int]) -> List[int]:
        # next greater is classic monotonic stack things
        # twist here is that we have a circular array, so the way we simulate that
        # is that we go through the array twice via modular arithmetic
        # we start with a next greater array of size -math.inf
        # keep a monotonically decreasing array so that when we get the next greater element
        # we mark it for all prior nodes
        # we store the index in the stack, not the value so we can track where it was

        decreasingStack = []
        greater = [-math.inf] * len(nums)

        for i in range(len(nums)*2):
            actualIndex = i%len(nums)
            currentNumber = nums[actualIndex]
            while decreasingStack and currentNumber > nums[decreasingStack[-1]]:
                prevNode = decreasingStack.pop()
                # if we have not calculated it yet, mark it
                if greater[prevNode] == -math.inf:
                    greater[prevNode] = currentNumber
            # now that we are no longer greater, add i%2 in there
            decreasingStack.append(actualIndex)
        
        # we will have -inf leftover that had no greater elements
        for i in range(len(greater)):
            if greater[i] == -math.inf:
                greater[i] = -1

        return greater # type: ignore

    # ── Attempt · 2026-07-21 ──────────────
    def nextGreaterElements_20260721(self, nums: List[int]) -> List[int]:
        # so in the first variation of this problem
        # we just go through the array and set next value accordingly using a stack
        # if we are circular, we just need to circle back by duplicating the data
        # and we just fill result[index%len]
        # [1,2,1,1,2,1]
        # if currentNumber > minStack, put it as minStack.pop's next biggest
        # so we need to put (value, index) in minStack
        length = len(nums)
        decreasingStack = []
        result = [-1] * length

        # simulate circular by looping through twice
        for i in range(length*2):
            # if stack is not empty and nums[i] > decreasingStack[-1], pop it
            # and assign if not assigned
            while decreasingStack and nums[i%length] > decreasingStack[-1][0]:
                priorNode = decreasingStack.pop()
                priorValue, priorIndex = priorNode[0], priorNode[1]
                if result[priorIndex%length] == -1:
                    result[priorIndex%length] = nums[i%length]
            # now that we are no longer increasing, add nums[i] to the stack
            decreasingStack.append((nums[i%length],i%length))
        
        return result

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
