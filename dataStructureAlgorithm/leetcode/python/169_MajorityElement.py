from typing import List

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # Pretty basic problem if we use a frequency mapping
        # But the followup asks if we can do this in O(n) time and O(1) space
        # This is literally just asking us to implement the Boyer-Moore Majority Vote Algorithm
        # This algorithm works iff there is a majority element in the input list
        # 1. Create a counter and result variable
        # 2. Loop through the list, if counter is zero, set result to nums[i] and set counter to 1
        # 3. If nums[i] = result, increment counter, otherwise decrement

        result,counter = 0,0

        for n in nums:
            if counter == 0:
                result = n
            counter += (1 if n == result else -1)
        return result

    # Another way to tackle this if just sort and return middle element
    # Since we know for sure there is a majority element, this will always work
    # Strangely this is actually faster than Boyer-Moore on LC, likely due to size of list
    def majorityElementSorting(self, nums: List[int]) -> int:
        nums.sort()
        # Double slash means integer division and disregard the additional modular
        return nums[len(nums)//2]
        
    def majorityElementBasic(self, nums: List[int]) -> int:
        map = {}
        result,maxCounter = 0,0
        for i,v in enumerate(nums):
            map[v] = 1 + map.get(v,0)
            result = v if map[v] > maxCounter else maxCounter
            maxCounter = max(map[v], maxCounter)
        return result
    