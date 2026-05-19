"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.347_top_k_frequent_elements
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

 

Example 1:

Input: nums = [1,1,1,2,2,3], k = 2

Output: [1,2]

Example 2:

Input: nums = [1], k = 1

Output: [1]

Example 3:

Input: nums = [1,2,1,2,1,2,3,1,3,2], k = 2

Output: [1,2]

Constraints:

    1 <= nums.length <= 105
    -104 <= nums[i] <= 104
    k is in the range [1, the number of unique elements in the array].
    It is guaranteed that the answer is unique.

Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
"""

import heapq
from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # We can have create a frequency map first
        # After which, we can use a min heap
        # pop until we get the kth element

        freqMap = {}
        for n in nums:
            freqMap[n] = 1 + freqMap.get(n,0)
        
        heap = []
        for num in freqMap.keys():
            # default heap from heapq is a min heap
            heapq.heappush(heap, (freqMap[num],num))
            # since we only want the top k most frequent
            # we just pop if we have more than k since pop removes min
            if len(heap) > k:
                heapq.heappop(heap)
        
        result = []
        # put heap onto result
        for freq, value in heap:
            result.append(value)

        return result