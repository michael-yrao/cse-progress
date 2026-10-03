"""
1552. Magnetic Force Between Two Balls   ·   https://leetcode.com/problems/magnetic-force-between-two-balls/
Pattern: binary_search

Given `position[]` (positions of baskets on a line) and `m` balls, place the m balls
into baskets so the MINIMUM distance between any two balls is as LARGE as possible.
Return that maximum-possible minimum distance.

Example: position=[1,2,3,4,7], m=3 -> 3  (place at 1, 4, 7 -> gaps 3,3 -> min 3).
Example: position=[5,4,3,2,1,1000000000], m=2 -> 999999999.

Constraints: 1 <= position[i] <= 1e9, 2 <= m <= len(position) <= 1e5.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-10-02 ──────────────
    def maxDistance_20261002(self, position: List[int], m: int) -> int:
        # if we ignore the fact that we have only n number of buckets, we would be just placing based on position[0] to position[-1], e.g. one at each end and repeat by cutting by half dependent on how many balls, which means this is a solution based binary search
        # and that we need to sort
        # so the maximum force we can possibly get is position[-1] - position[0], this is our upper bound
        # min bound, we'll say it is 1 since position is given to be min of 2
        # we are trying to maximize the the force, so this is max boundary

        position.sort()

        l, r = 1, position[-1] - position[0]

        def can_achieve(force):
            # we always place a ball at the beginning since that is the best min boundary
            latest_ball = position[0]
            ball_counter = 1
            # we can then just loop through and just place balls to get force
            # if we can't, we return false
            for i in range(1,len(position)):
                # if we can place ball here to achieve force, place it
                if position[i] - latest_ball >= force:
                    latest_ball = position[i]
                    ball_counter+=1
            # we can means we can put m balls to achieve this force
            return ball_counter>=m

        while l < r:
            # mid is the force we are seeing if we can achieve
            mid = (l + r + 1) // 2
            
            if can_achieve(mid):
                l = mid
            else:
                r = mid - 1
        
        return l

    # ── Attempt · 2026-09-22 ──────────────
    def maxDistance_20260922(self, position: List[int], m: int) -> int:
        # the entire array's position is kinda irrelevant
        # the picture in example 1 is what we'd like to visualize, which means we need to sort first
        # now with this sorted, we are trying to maximize the min magnetic force after placing m balls
        # so let's ignore the baskets for now
        # if we can put balls anywhere, this would just be binary search based on wherever we lock down m
        # so we try to do the same thing still, but since we can't place m just anywhere, we ask if it is possible to get this result. we want to maximize so we want to do max boundary binary search
        # if we look at example 1, it actually uses the positions, not the indices, so we do binary search on the answer

        position.sort()

        l, r = 1, position[-1] - position[0]

        # in order to see if we can achieve this force
        # we need to place m number of balls here
        # we always place a node on the bottom because this is the smallest we can do
        # then from here, we check if placing a ball in the next index can give us force
        # if yes, place it, otherwise, move on
        # we do need to keep track of how many balls we placed
        def canAchieve(force):
            lastBallPosition = position[0]
            ballsPlaced = 1
            # position[-1] + 1, so we include position[-1]
            for i in range(1, len(position)):
                if position[i] - lastBallPosition >= force:
                    lastBallPosition = position[i]
                    ballsPlaced+=1
            
            return ballsPlaced >= m
        

        while l < r:
            mid = (l + r + 1) // 2
            # if we are able to place all balls and achieve mid, keep as result
            if canAchieve(mid):
                l = mid
            else:
                r = mid - 1
        
        return l

    # ── Attempt 1 · 2026-09-20 ────────────────────────────────────────────
    def maxDistance(self, position: List[int], m: int) -> int:
        # so we want to maximize the force that we can get from placing m balls in these positions
        # so binary search on the result, so 1 is our lower bound given that n and m are both 2 at the smallest possible and position[len(position) - 1] - position[0] is our upperbound
        # since we are looking for the max force we can get, this is max boundary
        
        # it seems like the number in each index holds no significance
        # other than to say where the buckets are, so we just sort
        
        position.sort()
        
        left = 1
        right = position[-1] - position[0]

        def canAchieveForce(force):
            # example 1 gives us 3 off the bat as the first force that calls this
            # we always place a ball at the start
            # now we have to go through the entire array to check if this force is achievable
            latestBasket = position[0]
            ballCounter = 1
            incr = 1
            while incr < len(position) and ballCounter < m:
                currentBasket = position[incr]
                # if magnetic force between currentBasket and latestBasket is >= force
                # we can place a ball here
                if currentBasket - latestBasket >= force:
                    latestBasket = currentBasket
                    ballCounter+=1
                incr+=1
            
            return ballCounter == m

        while left < right:
            middle = (left + right + 1) // 2
            # if we can achieve this, keep as result and try to go higher
            if canAchieveForce(middle):
                left = middle
            else:
                right = middle - 1
        
        return left
