from typing import List
import heapq

class Solution:
    # There are a few approaches to this problem
    # Solution #1: We can do a sliding window technique and a max heap assisted by Tuples/Pairs
    #   where we keep track of the index and value and the heap will be sorted by value.
    #   This solution would be O(nlogk)
    # Solution #2: The more efficient solution would be to use a monotone stack/queue,
    #   This solution would be O(n)

    def maxSlidingWindowHeap(self, nums: List[int], k: int) -> List[int]:
        # heapq in Python is implemented as a min heap
        # thus we will just invert all values to simulate a max heap
        # 1. Create a heap, we will keep this heap's size at k,
        #    similarly, we will want r - l + 1 to be equal to k at all times,
        #    thus we will do a simple loop through to get current min in first k values
        # 2. for each number in nums, we want both the index and value
        
        minHeap = []
        result = []

        # Push first k numbers into the heap and set our window pointers accordingly

        for i in range(0,k,1):
            heapq.heappush(minHeap, (nums[i] * -1, i))

        l,r=0,k-1
        while r < len(nums):
            result.append(minHeap[0][0] * -1)
            # Just realized this solution doesn't work in Python
            # Since we can't just remove an element from the Heap like we can in Java
            # Our workaround here can be as bad as O(n) which totals to a worst case of O(n^2)
            minHeap.remove((nums[l]*-1,l))
            heapq.heapify(minHeap)
            l+=1
            r+=1
            if r < len(nums): heapq.heappush(minHeap,(nums[r] * -1, r))

        return result


    def maxSlidingWindowMono(self, nums: List[int], k: int) -> List[int]:
        monostack = []