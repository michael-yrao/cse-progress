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

    # ── Attempt · 2026-07-17 ──────────────
    def singleNonDuplicate_20260717(self, nums: List[int]) -> int:
        # so the annoying thing here is the duplication
        # so we need to make sure we are always on the first number of duplicates
        # also knowing all numbers except one is a dup
        # it means that one side has odd, and one side has even numbers
        # [1,1,2,3,3,4,4,8,8] ; m = 3 ; 3%2 != 0, therefore we go left
        #  l     m         r
        # since we are not looking for the exact number, this is another boundary search
        
        l, r = 0, len(nums) - 1

        while l < r:
            m = (l+r)//2
            # we need to check if nums[m] is the first occurence of the number
            if m-1 >= 0 and nums[m] == nums[m-1]:
                m-=1
            # now we know m is the first number of the dups, we can do the mod check
            # if m%2 is true, then answer is definitely not in the left side
            if m%2 == 0 and nums[m] == nums[m+1]:
                l = m + 2
            else:
                r = m
        
        return nums[l]

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

    def singleNonDuplicate_20260610(self, nums: List[int]) -> int:
        # logn means binary search and constant space means no extra array
        # so knowing every element appears twice except for one, what does this mean
        # [1,1,2,3,3,4,4,8,8]
        #  l       m       r
        # how do we know where to move m
        # so if we have 1 number being single, we know the array is always odd count
        # so let's check if answer is on the right
        # [1,1,2,2,3,3,4,8,8]
        #  l       m       r
        # we also notice this is not an exact find binary search
        # so we are looking for the earliest number to break the pattern
        # which means this is a min boundary binary search
        # also we also notice we start odd and need to continue going to the odd side
        # so that means we should do m % 2 to determine which side to go to
        # in here, we have m % 2 = 0 but we can't really decide on this
        # so if we don't have a single digit, nums[m] == nums[m+1]
        # that means if equal, then answer is in the upper bound
        # but this is with assumption that m is the first digit of the duplicate
        # so we need to make sure that is the case
        # and we do that by doing if m % 2 == 1, shift m down by 1
        l, r = 0, len(nums) - 1

        while l < r:
            m = (l+r)//2
            # apply shift down logic so m is always at first of the duplicates
            if m % 2 == 1:
                m-=1
            # knowing nums[m] == nums[m+1] for if there are no singles
            # that means if this is true, number is in the upper quadrant
            # so we set l = m + 2
            # biasing left since this is min boundary
            if nums[m] == nums[m+1]:
                l = m + 2
            else:
                r = m

        return nums[l]
    
    def singleNonDuplicate_20260613(self, nums: List[int]) -> int:
        # logn means binary search and constant space means no extra array
        # so the problem is really kinda just a trick
        # what we can notice is that it is sorted, and trying to find an unknown number
        # so clearly a boundary type of binary search
        # in order for binary search to work, we need to make sure m is always on the first elemenet of the duplicate
        # and we should also note that if numbers are duplicated, it means the count is always 2 each time, so in example 2, after mid is correctly placed at the first 7
        # we will note the left side has size 2, so the single element cannot be there

        l, r = 0, len(nums) - 1

        while l < r:
            m = (l+r)//2
            # let's correct m first
            # if m is equal to m+1, we don't need to do anything
            # if m is not equal, we need to move m down
            if m+1 < len(nums) and nums[m] != nums[m+1]:
                m-=1
            
            # now we do the binary search
            # if left side is even numbers, we know result is in right boundary
            if m%2 == 0:
                # m + 2 since we got duplicates
                l = m + 2
            else:
                r = m
        
        return nums[l]
