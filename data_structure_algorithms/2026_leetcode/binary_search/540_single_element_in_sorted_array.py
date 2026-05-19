"""
You are given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once.

Return the single element that appears only once.

Your solution must run in O(log n) time and O(1) space.

Example 1:

Input: nums = [1,1,2,3,3,4,4,8,8]
Output: 2

Example 2:

Input: nums = [3,3,7,7,10,11,11]
Output: 10

Constraints:

    1 <= nums.length <= 105
    0 <= nums[i] <= 105
"""
from typing import List

class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        # logn time and O(1) space means has to be binary search and no extra space
        # we don't know what we are looking for, thus we need a way to identify which half it is in
        # since all elements appear twice except for the target, we know len(nums) is odd
        # return condition: mid != mid + 1 and mid != mid - 1
        # [1,1,2,3,3,4,4,8,8]
        #  l       m       r
        # since we know the side with the answer is odd, we can look at length of both sides without current element
        # if m=m-1, then len(left)=m-1, if len(left)%2==0, then we move l=m+1 else r=m-1 
        # if m!=m-1, then len(left)=m

        l,r = 0,len(nums) - 1

        while l <= r:
            mid = (l+r)//2

            # since we are doing mid - 1 and mid + 1 here
            # we need to make sure they are inbound
            # if mid -1 is out of bounds or if nums[mid - 1] != nums[mid], left side check is good
            # if mid + 1 is out of bounds or if nums[mid + 1] != nums[mid], right side check is good
            if (mid - 1 < 0 or nums[mid - 1] != nums[mid]) and (mid + 1 >= len(nums) or nums[mid] != nums[mid + 1]):
                return nums[mid]
            # no answers found yet
            # check which side is odd
            lenLeft = 0
            if nums[mid] == nums[mid - 1]:
                lenLeft = mid - 1
            else:
                lenLeft = mid
            if lenLeft%2==0:
                l=mid+1
            else:
                r=mid-1
            
        return -1
