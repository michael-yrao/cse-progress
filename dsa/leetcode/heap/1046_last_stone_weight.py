"""
You are given an array of integers stones where stones[i] is the weight of the ith stone.

We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. The result of this smash is:

    If x == y, both stones are destroyed, and
    If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.

At the end of the game, there is at most one stone left.

Return the weight of the last remaining stone. If there are no stones left, return 0.

Example 1:

Input: stones = [2,7,4,1,8,1]
Output: 1
Explanation: 
We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

Example 2:

Input: stones = [1]
Output: 1

Constraints:

    1 <= stones.length <= 30
    1 <= stones[i] <= 1000
"""
import heapq
from typing import List

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        # go through the list and heapify the array as a max heap
        # pop twice to smash, if diff is not zero, insert diff into heap
        # continue until we are left with heap of size 1 or less
        
        maxHeap = []

        for stone in stones:
            # must push negative since python heap is minHeap by default
            heapq.heappush(maxHeap, -stone)
        
        # we want to stop the loop when we only have 1 stone or 0 stone left
        while len(maxHeap) > 1:
            firstStone = -heapq.heappop(maxHeap)
            secondStone = 0
            if len(maxHeap) > 0:
                secondStone = -heapq.heappop(maxHeap)
            diff = firstStone - secondStone
            if diff != 0:
                heapq.heappush(maxHeap, -diff)
        
        if len(maxHeap) == 1:
            return -maxHeap[0]
        return 0