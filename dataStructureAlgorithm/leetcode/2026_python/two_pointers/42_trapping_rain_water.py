"""
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example 1:

Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:

Input: height = [4,2,0,3,2,5]
Output: 9

Constraints:

    n == height.length
    1 <= n <= 2 * 104
    0 <= height[i] <= 105

"""

from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        # knowing water at each index = min(leftMax, rightMax) - height[i]
        # we need to keep track of leftMax and rightMax of each index
        # leftMax and rightMax stands for the walls for which this current index
        # can trap water

        # height   = [0,1,0,2,1,0,1,3,2,1,2,1]
        # leftMax  = [0,0,1,1,2,2,2,2,3,3,3,3]
        # rightMax = [3,3,3,3,3,3,3,2,2,2,1,0]
        # water    = [0,0,1,0,1,2,1,0,0,1,0,0]

        leftMax = [0] * len(height)
        rightMax = [0] * len(height)
        totalWater = 0

        for i in range(1,len(height)):
            leftMax[i] = max(leftMax[i-1], height[i-1])
        
        for i in range(len(height)-2,-1,-1):
            rightMax[i] = max(rightMax[i+1],height[i+1])

        for i in range(len(height)):
            currentWater = max(0, min(leftMax[i],rightMax[i])-height[i])
            totalWater += currentWater

        return totalWater
    
    def trapTwoPointer(self, height: List[int]) -> int:

        # height   = [0,1,0,2,1,0,1,3,2,1,2,1]
        # leftMax  = [0,0,1,1,2,2,2,2,3,3,3,3]
        # rightMax = [3,3,3,3,3,3,3,2,2,2,1,0]
        # water    = [0,0,1,0,1,2,1,0,0,1,0,0]

        # following this, we can find the intuition that we don't really need to store
        # all of the leftMax and rightMax
        # we can just update it as we go
        # therefore we can try to use something like two pointers
        # we use two pointers specifically to find left and right max
        # if we remember the formula for water at current index
        # water[i] = min(leftMax[i],rightMax[i]) - height[i]
        # min(leftMax[i],rightMax[i]) stands for potential water
        # thus true formula is as such:
        # water[i] = (potential water) - height[i]
        # so we start l and r at opposite sides of the array
        # min(l,r) tells us the potential amount of water we can have
        # we can sub min(l,r) with an if l < r ... else ...
        # since these are the only 2 scenarios of min(l,r)
        # knowing which side is the min allows us to assume it is the potential water
        # from there, we can just do (potential water - height[i]) as before

        if not height:
            return 0

        l, r = 0, len(height) - 1
        leftMax, rightMax = height[l], height[r]
        res = 0
        while l < r:
            if leftMax < rightMax:
                # boundaries don't trap water, so we increment first
                l += 1
                # this gets us the potential water we can store
                leftMax = max(leftMax, height[l])
                # add (potential water - height[i]) to result
                res += leftMax - height[l]
            else:
                # boundaries don't trap water, so we decrement first
                r -= 1
                # this gets us the potential water we can store
                rightMax = max(rightMax, height[r])
                # add (potential water - height[i]) to result
                res += rightMax - height[r]
        return res