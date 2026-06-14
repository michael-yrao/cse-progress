from typing import List

class Solution:
    def numSubseqEfficient(self, nums: List[int], target: int) -> int:
        result = 0
        nums.sort()
        mod = (10**9 + 7)
    
        l,r=0,len(nums)-1

        # We do inclusive here since we can use same value as min and max
        while l <= r:
            # If we found a valid l and r combination
            # Add to result and increment left
            if nums[l] + nums[r] <= target:
                result += pow(2,r-l,mod)
                l+=1
            # Otherwise, keep moving right until we do
            else:
                r-=1
        
        return result%mod

    def numSubseq(self, nums: List[int], target: int) -> int:
        # First thought is actually just to use backtracking but don't recall how to pull it off
        # When we look at the problem, its pretty important to sort since we need both min/max
        # We can use Two Pointers with left being min and right being max
        # At each step, we can consider whether to take the value or not take the value
        # What this means is each value gives us 2^x choices where 2 is the 2 choices we have
        # And x is the number of values
        # e.g. [3,4,6,8] -> L=3;R=6, L is mandatory since it is the determining factor for R position
        # We have 2 values thus 2^2 for this iteration
        
        nums.sort()
        result = 0
        mod = (10**9 + 7)
        right = len(nums) - 1
        for i, left in enumerate(nums):
            while (left + nums[right]) > target and i <= right:
                right -= 1
            if i <= right:
                # right is the largest we can have with this left value
                # number of subsequences for this l,r set is then 2^(r - i)
                result += (2**(right - i))
                result %= mod
        
        return result