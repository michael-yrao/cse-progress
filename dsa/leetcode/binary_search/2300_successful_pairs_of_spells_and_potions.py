"""
You are given two positive integer arrays spells and potions, of length n and m respectively, where spells[i] represents the strength of the ith spell and potions[j] represents the strength of the jth potion.

You are also given an integer success. A spell and potion pair is considered successful if the product of their strengths is at least success.

Return an integer array pairs of length n where pairs[i] is the number of potions that will form a successful pair with the ith spell.

Example 1:

Input: spells = [5,1,3], potions = [1,2,3,4,5], success = 7
Output: [4,0,3]
Explanation:
- 0th spell: 5 * [1,2,3,4,5] = [5,10,15,20,25]. 4 pairs are successful.
- 1st spell: 1 * [1,2,3,4,5] = [1,2,3,4,5]. 0 pairs are successful.
- 2nd spell: 3 * [1,2,3,4,5] = [3,6,9,12,15]. 3 pairs are successful.
Thus, [4,0,3] is returned.

Example 2:

Input: spells = [3,1,2], potions = [8,5,8], success = 16
Output: [2,0,2]
Explanation:
- 0th spell: 3 * [8,5,8] = [24,15,24]. 2 pairs are successful.
- 1st spell: 1 * [8,5,8] = [8,5,8]. 0 pairs are successful. 
- 2nd spell: 2 * [8,5,8] = [16,10,16]. 2 pairs are successful. 
Thus, [2,0,2] is returned.

Constraints:

    n == spells.length
    m == potions.length
    1 <= n, m <= 105
    1 <= spells[i], potions[i] <= 105
    1 <= success <= 1010
"""
from typing import List

class Solution:
    # time complexity: O(nlogm + mlogm) ; mlogm to sort the potion ; nlogm to find min boundary
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        # ok so first thing to notice is that size of output = len(spells)
        # brute force solution is to just iterate over both, check spells[i]*potions[j]>success and increment output[i]
        # this would be a O(n*m) solution
        # so note that we are keeping track of numbers of success, so ordering doesn't matter much, so we can sort potions
        # if we can sort potions, we can find the minimum potion strength such that it is successful
        # so what this becomes is a min boundary binary search problem
        # condition that we found the min is that if potions[mid] * spells[i] >= success and potions[right] * spells[i] >= success
        # that means we definitely want to go to the left

        successRate = [0] * len(spells)

        potions.sort()

        for i in range(len(spells)):
            l, r = 0, len(potions) - 1
            while l < r:
                mid = (l + r) // 2
                if potions[mid] * spells[i] >= success:
                    r = mid
                else:
                    l = mid + 1

            # if min boundary is < success, then assign 0
            if potions[l] * spells[i] < success:
                successRate[i] = 0
            else:
                successRate[i] = len(potions) - l

        return successRate
    
    def successfulPairs_20260612(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        # ok so first thing to notice is that size of output = len(spells)
        # i guess naive solution is just to loop through both and multiply and do an output so O(n*m)
        # key thing is that we actually just want number of successes, so we can order the potions
        # if we are doing that, we can binary search on potions and find the smallest potion such that we can succeed on
        # so min boundary binary search

        result = [0] * len(spells)

        potions.sort()

        for index in range(len(spells)):
            l, r = 0, len(potions) - 1
            while l < r:
                m = (l+r)//2
                if potions[m]*spells[index] >= success:
                    r = m
                else:
                    l = m + 1
            
            # now l is at the smallest potion possible to succeed
            # but looking at the example, it's possible we just have 0
            if potions[l] * spells[index] < success:
                result[index] = 0
            else:
                # if l is bigger, that means we need to do len - l
                result[index] = len(potions) - l
                
        return result
    def successfulPairs_20260619(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        # result size = spells size
        # sucess if spells * potions[i] > success
        # one thing to note is that first example, potions is sorted
        # and the output wants how many so order does not matter
        # so we should start by sorting potions
        # what this means is, we can then find the smallest number in potion such that it is successful
        # so min boundary for binary search
        
        potions.sort()
        
        result = [0] * len(spells)

        # for each of the spells, we want to find the min boundary

        for i in range(len(spells)):
            l, r = 0, len(potions) - 1
            while l < r:
                m = (l+r)//2
                # if greater, drop r = m
                if spells[i] * potions[m] >= success:
                    r = m
                else:
                    l = m + 1
            # so now l is the minimum index for success
            # so 5 - 1, so len(potions) - l
            # we also do have to consider case of spells[1] where nothing succeeds
            # so if no success at position l, it means we would never succeed so we set it to 0
            if spells[i] * potions[l] < success:
                result[i] = 0
            else:
                result[i] = len(potions) - l
        
        return result
