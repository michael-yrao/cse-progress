"""
Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

Example 1:

Input: piles = [3,6,7,11], h = 8
Output: 4

Example 2:

Input: piles = [30,11,23,4,20], h = 5
Output: 30

Example 3:

Input: piles = [30,11,23,4,20], h = 6
Output: 23

Constraints:

    1 <= piles.length <= 104
    piles.length <= h <= 109
    1 <= piles[i] <= 109
"""

import math
from typing import List

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # we are looking for the value k
        # using a bit of math, we can tell we are looking for where math.ceil(piles[i] / k) = h
        # we also know the max this k should be is the max(piles)
        # knowing the list is not sorted, we should just go through the list to find the max giving us O(n) minimum
        # brute force solution is trying k from 1 to max(piles), giving us a time complexity of O(n*max(piles))
        # what we can do is actually just do the same thing but with binary search
        # l = 1, r = max(piles)

        l, r = 1, max(piles)

        # we are not sure what we are looking for just yet
        # thus we want to use l < r
        while l < r:
            mid = (l + r) // 2
            currentHours = 0
            for pile in piles:
                currentHours += math.ceil(pile / mid)

            # can't finish the bananas in mid eating speed
            # exclude mid from further searches
            if currentHours > h:
                l = mid + 1
            else:
            # can finish in mid eating speed, keep it as a candidate
                r = mid
        return l
    def minEatingSpeed_20260703(self, piles: List[int], h: int) -> int:
        # so we can assume max eating speed needed is max(piles)
        # we are also told h >= len(piles) so don't need to worry about that case
        # basically we are looking for the smallest eating speedy possible
        # min boundary binary search, but what is our lower boundary
        # i guess we can just say 1

        def canFinish(m):
            timeTaken = 0
            for bananas in piles:
                # eat bananas
                timeTaken+=math.ceil(bananas/m)
            return timeTaken <= h

        def minBoundaryBinarySearch(l,r):
            while l < r:
                m = (l+r)//2
                # now we determine whether m can finish in h hours
                # m is still a possible answer, so we set r to m
                if canFinish(m):
                    r = m
                else:
                    l = m + 1
            return l
        
        return minBoundaryBinarySearch(1,max(piles))