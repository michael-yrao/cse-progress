from typing import List
import heapq
import unittest
import sys

class Solution:
    def minimumDifferenceTwoPointers(self, nums: List[int], k: int) -> int:
        nums.sort()
        l,r=0,k-1
        minDiff = sys.maxsize
        length=len(nums)
        while r < length:
            minDiff = min(minDiff,nums[r]-nums[l])
            r+=1
            l+=1
        return minDiff

    def minimumDifferenceHeap(self, nums: List[int], k: int) -> int:
        # First thought was to use a max or min heap 
        # A silly solution can just be to create 2 heaps, one max, one min, both of size k
        # We can then return min from the two, result would be O(n)
        # But this is prob the worst type of O(n) you can do
        # For some reason, it doesn't even work on LC, might need to understand heaps in python more
        # A pretty obvious solution is just sort and do two pointer

        # minheap holds the k largest
        # maxheap holds the k smallest
        maxHeap,minHeap=[],[]

        for x in nums:
            heapq.heappush(minHeap,x)
            heapq.heappush(maxHeap,x * -1)
            while len(minHeap) > k:
                heapq.heappop(minHeap)
            while len(maxHeap) > k:
                heapq.heappop(maxHeap)

        # This doesn't work since heap only guarantees first element as min/max
        # Thus we actually need to go through both heaps
        # return min(minHeap[k-1] - minHeap[0], (maxHeap[0] * -1) - (maxHeap[k-1] * -1))

        # Retrieve first and last element from each heap
        minheapv2,minheapv1=minHeap[0],0
        maxheapv1,maxheapv2=maxHeap[0] * -1,0
        while len(minHeap) > 1:
            heapq.heappop(minHeap)
            heapq.heappop(maxHeap)
        minheapv1,maxheapv2=minHeap[0],maxHeap[0] * -1
        return min(minheapv1-minheapv2,maxheapv1-maxheapv2)
    
class UnitTest(unittest.TestCase):
    def testminDiffHeap(self):
        input = [87063,61094,44530,21297,95857,93551,9918]
        expectedAnswer = 74560
        result = Solution().minimumDifferenceHeap(input,6)
        self.assertEqual(expectedAnswer,result)

unittest.main()