"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.75_sort_colors

Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function. 

Example 1:

Input: nums = [2,0,2,1,1,0]
Output: [0,0,1,1,2,2]

Example 2:

Input: nums = [2,0,1]
Output: [0,1,2]

 

Constraints:

    n == nums.length
    1 <= n <= 300
    nums[i] is either 0, 1, or 2.

"""

from typing import List


class Solution:
    def sortColorsBucketSort(self, nums: List[int]) -> None:
        # since there's only 3 colors, we can just do count/bucket sort
        # and then loop through and replace
        countMap = {}
        for num in nums:
            countMap[num] = 1 + countMap.get(num,0)
        
        index = 0
        for color in range(3):
            while countMap.get(color):
                nums[index] = color
                countMap[color] = countMap.get(color) - 1
                index+=1

    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # quicksort partition
        # use pointers to swap and increment
        # use a left pointer and a increment pointer to swap whenever it finds a 0
        # use a right pointer and the same increment pointer to swap whenever it finds a 2
        # left and right pointers are there to help faciliate where to put the values, 
        # thus increment/decrement when swapping. only increment increment counter when left moves
        # reason we are doing this is to fulfill the one pass requirement

        left, right = 0, len(nums) - 1
        increment = 0

        def swap(i,j):
            tmp = nums[i]
            nums[i] = nums[j]
            nums[j] = tmp
            
        while increment <= right:
            if nums[increment] == 0:
                swap(left, increment)
                left+=1
            elif nums[increment] == 2:
                swap(right, increment)
                right-=1
                increment-=1
            increment+=1
