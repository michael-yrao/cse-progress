from typing import List

class Solution:   
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        # We are going to solve k sum instead of 4sum
        # Since the solution of 3sum,4sum,5sum,etc are all the same but with 1 extra loop each
        # Thus, we can just rely on recursion instead
        # This will be similar to a backtracking solution

        nums.sort()
        result, curSolution = [],[]

        # We pass in target since it will be changing constantly
        # Other variables can be accessed without being passed in
        def kSum(k,startIndex,target):
            # Base case is TwoSumSorted
            # Taking care of non-base case first to reduce code clustering
            if k != 2:
                # We are only picking one element per call
                # e.g. if k==4 and start == 0 where we want a+b+c+d=target
                # This iteration would be filling in the "a" slot
                for i in range(startIndex,len(nums) - k + 1):
                    # Skip duplicates
                    if i > startIndex and nums[i] == nums[i-1]:
                        continue
                    curSolution.append(nums[i])
                    # We filled in the "a" slot, we will go forward to the next
                    kSum(k-1,i+1,target - nums[i])
                    curSolution.pop()
                return
            # Base case Two Sum Sorted
            l,r = startIndex, len(nums) - 1
            while l<r:
                if nums[l] + nums[r] < target:
                    l+=1
                elif nums[l] + nums[r] > target:
                    r-=1
                else:
                    # curSolution currently don't have l and r, append both
                    result.append(curSolution + [nums[l],nums[r]])
                    l+=1
                    r-=1
                    while l < r and nums[l] == nums[l-1]: l+=1
                    while l < r and nums[r] == nums[r+1]: r-=1
        
        kSum(4,0,target)
        return result

    def fourSumNaiveSolution(self, nums: List[int], target: int) -> List[List[int]]:
        # Input: nums = [1,0,-1,0,-2,2], target = 0
        # Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
        # Similar to 3sum, we should try sorting first which will make it easier to traverse
        # What we can do is literally wrap 3sum with an additional loop
        # Giving us a final solution of O(n^3)
        nums.sort()
        result = []

        for i in range(len(nums)):
            firstTarget = target - nums[i]
            for j in range(i,len(nums),1):
                secondTarget = firstTarget - nums[j]
                l,r=j+1,len(nums)-1
                while r > l:
                    if nums[l] + nums[r] > secondTarget:
                        r-=1
                    elif nums[l] + nums[r] < secondTarget:
                        l+=1
                    else:
                        result.append([i,j,l,r])
                        l+=1
                        r-=1
                        while l < r and nums[l] == nums[l-1]: l+=1
                        while l < r and nums[r] == nums[r+1]: r-=1
        return result