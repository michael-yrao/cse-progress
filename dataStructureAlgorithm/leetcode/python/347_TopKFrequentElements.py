from typing import List
import heapq

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 1. Create a map where we keep track of frequency of each distinct number in the list
        # 2. From this map, we want to use a min heap of size k to keep track of the k top frequent elements
        # 3. Return heap.toList()

        freq = {}

        for n in nums:
            freq[n] = freq.get(n,0) + 1
        
        # In Python, Min Heap is just a List

        minHeap = []

        for key, value in freq.items():
            heapq.heappush(minHeap, (value, key))
            if len(minHeap)>k: heapq.heappop(minHeap)

        result = []

        for frq,key in minHeap:
            result.append(key)

        return result