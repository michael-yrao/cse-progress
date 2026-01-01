from typing import List

class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        # ! This Algorithm is likely to be useful for Progressive Overflow
        # * k is the maximum distance between i and j
        # * So first thought is a map of value to indices
        # * Then we can go through the keys where size of values is >= 2 and check from there
        # * But seems there is an easier way, we don't really care as longas it is <= k
        # * Therefore, we should assume a static window size of k and use sliding window
        # * We will use a Set to indicate all the values in our current window
        # * If a duplicate appear, it means we already finished the problem and can return True
        # * Otherwise, just increment r and add the value into the set
        # * If r-l becomes bigger than k, we want to remove nums[l] from window and shift l until it isn't
        
        window = set()

        l,r=0,0

        while r < len(nums):
            if nums[r] in window:
                return True
            window.add(nums[r])
            r+=1
            while r-l > k:
                window.remove(nums[l])
                l+=1
        
        return False