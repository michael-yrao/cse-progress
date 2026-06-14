"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.11_container_with_most_water
You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.
Example 1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

Example 2:
Input: height = [1,1]
Output: 1
"""
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        # height = min(height[l], height[r])
        # width = r - l
        # currentMaxArea = (r - l) * min(height[l], height[r])
        # start l = 0, r = len(height) - 1
        # increment min(height[l], height[r])
        # update maxArea = max(maxArea, currentMaxArea) each iteration
        # return maxArea
        maxArea = 0
        l = 0
        r = len(height) - 1
        while l < r:
            areaHeight = min(height[l], height[r])
            areaWidth = r - l
            currentMaxArea = areaHeight * areaWidth
            maxArea = max(maxArea, currentMaxArea)
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return maxArea