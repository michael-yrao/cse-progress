import sys
from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        # Knowing that the two lists are both sorted
        # What we can do is loop starting from the end of the list
        # Compare the last value of nums1 and nums2, whichever is bigger goes into the end
        
        # We can actually just use m and n to increment since they are given
        last = m + n - 1

        while m > 0 and n > 0:
            if nums1[m - 1] > nums2[n - 1]:
                nums1[last] = nums1[m - 1]
                m-=1
            else:
                nums1[last] = nums2[n - 1]
                n-=1
            last-=1
        
        # It's possible to have values leftover in nums2
        # In the case where there are 1 or more elements in nums2 smaller than the smallest
        # value in nums1

        while n > 0:
            nums1[last] = nums2[n - 1]
            last, n = last - 1, n - 1