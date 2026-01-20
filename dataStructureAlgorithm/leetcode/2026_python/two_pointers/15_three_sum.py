"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.two_pointers.15_three_sum
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

 

Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.

Constraints:

    3 <= nums.length <= 3000
    -105 <= nums[i] <= 105
"""

from typing import List

class Solution:
    def threeSumSet(self, nums: List[int]) -> List[List[int]]:
        # sort the list
        # use two sum 2 solution to solve subproblem
        # a + b + c = 0
        # loop through such that we are looking for -a = b + c

        nums.sort()
        solutionSet = set()
        for i in range(len(nums)):
            j, k = i+1, len(nums) - 1
            while j < k:
                total = nums[i] + nums[j] + nums[k]
                # if > 0, too high, move k down
                # if < 0, too low, move j up
                # if = 0, add to set
                if total == 0:
                    solution = (nums[i], nums[j], nums[k])
                    solutionSet.add(solution)
                    # have to increment both here since j and k are now used
                    j+=1
                    k-=1
                elif total > 0:
                    k-=1
                else:
                    j+=1
        
        return list(solutionSet)
    
    def threeSumWithoutSet(self, nums: List[int]) -> List[List[int]]:
        # Without using set, we have to keep track ourselves
        # so we only add solutions when they are different
        solution = []
        nums.sort()
        for i in range(len(nums)):
            # don't need to check same number multiple times
            # loop til we see the next unique value
            if i > 0 and nums[i] == nums[i-1]:
                 continue
            j, k = i+1, len(nums) - 1
            while j<k:
                total = nums[i] + nums[j] + nums[k]
                # if > 0, too high, move k down
                # if < 0, too low, move j up
                # if = 0, add to set
                if total == 0:
                    oneSolution = (nums[i], nums[j], nums[k])
                    solution.add(oneSolution)
                    # have to increment both here since j and k are now used
                    j+=1
                    k-=1
                    # continue to avoid duplicates
                    while nums[j] == nums[j-1] and j<k:
                        j+=1
                    while nums[k] == nums[k+1] and j<k:
                        k+=1
                elif total > 0:
                    k-=1
                else:
                    j+=1
        
        return solution