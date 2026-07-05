"""
The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.

You are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2.

For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater element of nums2[j] in nums2. If there is no next greater element, then the answer for this query is -1.

Return an array ans of length nums1.length such that ans[i] is the next greater element as described above.

Example 1:

Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
Output: [-1,3,-1]
Explanation: The next greater element for each value of nums1 is as follows:
- 4 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
- 1 is underlined in nums2 = [1,3,4,2]. The next greater element is 3.
- 2 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.

Example 2:

Input: nums1 = [2,4], nums2 = [1,2,3,4]
Output: [3,-1]
Explanation: The next greater element for each value of nums1 is as follows:
- 2 is underlined in nums2 = [1,2,3,4]. The next greater element is 3.
- 4 is underlined in nums2 = [1,2,3,4]. There is no next greater element, so the answer is -1.

Constraints:

    1 <= nums1.length <= nums2.length <= 1000
    0 <= nums1[i], nums2[i] <= 104
    All integers in nums1 and nums2 are unique.
    All the integers of nums1 also appear in nums2.

Follow up: Could you find an O(nums1.length + nums2.length) solution?
"""
from typing import List

class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # brute force is to double for loop, when we see the nums1[i] in nums2, we look further right until we find a bigger number giving us O(n^2)
        # What we should do instead of go through nums2 first and map all next greater element. This is done through a monotonic stack
        # then all we need to do in nums1 is do a look up

        # we keep track of indices in the monotonic stack
        increasingStack = []
        increasingMap = {}
        for i in range(len(nums2)):
            # if adding value makes the stack no longer increasing
            # we pop until we resastisfy the condition
            while increasingStack and nums2[increasingStack[-1]] < nums2[i]:
                index = increasingStack.pop()
                # since nums[index] < nums[i], that means nums[i] is the next greater compared to nums[index]
                increasingMap[nums2[index]] = nums2[i]
            increasingStack.append(i)
        
        result = []
        # now we have increasingMap, we just need to go through nums1 once
        for i in range(len(nums1)):
            nextGreater = increasingMap.get(nums1[i],-1)
            result.append(nextGreater)
        return result