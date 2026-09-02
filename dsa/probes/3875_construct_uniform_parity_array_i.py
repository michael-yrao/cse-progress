"""
3875. Construct Uniform Parity Array I   ·   https://leetcode.com/problems/construct-uniform-parity-array-i/
Pattern: 🗓️ DAILY (self-directed, off-tracker) — solved by the learner.

You are given an integer array `nums1` of length `n`. Construct an array `nums2`
of length `n` in which every element has the SAME parity (all odd, or all even).
For each index `i` you must choose exactly one of:
  - nums2[i] = nums1[i], or
  - nums2[i] = nums1[i] - nums1[j]   for some j != i.

Return `true` if such a `nums2` can be constructed, otherwise `false`.

    nums1 = [2,3]  ->  true      nums2 = [-1, 3]  (both odd)
    nums1 = [4,6]  ->  true      nums2 = [ 4, 6]  (both even)

Constraints:
    1 <= n == nums1.length <= 100
    1 <= nums1[i] <= 100
    All integers in nums1 are distinct.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-09-01 ──────────────
    def uniformArray(self, nums1: List[int]) -> bool:
        # option 1 is just if the entire array is already odd or even
        # option 2 is helping us swap
        # so maybe we just have two arrays, one for odd and one for even
        # now we go through nums1 and just populate both
        # if either one of these become len(nums1), we got an answer
        # for option 2, we actually need a map of index to num

        numMap = {}

        for i in range(len(nums1)):
            numMap[i] = nums1[i]

        oddSet = set()
        evenSet = set()

        for i in range(len(nums1)):
            # option 1
            if nums1[i]%2==0:
                evenSet.add(i)
            else:
                oddSet.add(i)
            # option 2
            for index, value in numMap.items():
                if i != index and nums1[i] - nums1[index] %2 == 0:
                    evenSet.add(i)
                elif i != index and nums1[i] - nums1[index] %2 != 0:
                    oddSet.add(i)
        
        return len(nums1) == len(oddSet) or len(nums1) == len(evenSet)

    def uniformArray_numberTheory(self, nums1: list[int]) -> bool:
        # number theory
        # 1. if all even or odd already, true
        # 2. even - even = even ; odd -  odd = even
        # 3. even - odd  =  odd ; odd - even = odd
        # so if an even and an odd exist, we can always generate the other
        # thus 2 and 3 always becomes True if 1 is not true
        return True
