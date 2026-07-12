"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.229_majority_element_2
Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.

Example 1:
Input: nums = [3,2,3]
Output: [3]

Example 2:
Input: nums = [1]
Output: [1]

Example 3:
Input: nums = [1,2]
Output: [1,2]

Constraints:

    1 <= nums.length <= 5 * 104
    -109 <= nums[i] <= 109

Follow up: Could you solve the problem in linear time and in O(1) space?
"""
from collections import defaultdict
import collections
from typing import List
import unittest

class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        # all return keys must have size bigger than minSize
        # double / for int, single / for float
        minSize = len(nums)//3
        
        # map of n -> freq(n)

        freqMap = defaultdict(int)

        for n in nums:
            freqMap[n] += 1
        
        returnList = []

        for key, value in freqMap.items():
            if value > minSize:
                returnList.append(key)
        
        return returnList
    
    def majorityElementBoyerMoore(self, nums: List[int]) -> List[int]:
        # all return keys must have size bigger than minSize
        minSize = len(nums)//3
        
        # map of n -> freq(n)
        freqMap = defaultdict(int)
        
        for n in nums:
            freqMap[n] += 1
            # we want to keep size of map to 2 or less
            # reason being there can only be 2 values in nums having freq > n/3
            if len(freqMap) <= 2:
                continue
            
            # we have 3 elements in freqMap
            # so let's decrement and clean out the map

            for n, count in freqMap.items():
                freqMap[n] = count - 1

            # cannot iterate over a map while popping
            # thus we convert the key of the map to a list and use that to pop
            # since map is at most O(3), this is still O(1) space
            for n in list(freqMap):
                if freqMap[n] == 0:
                    freqMap.pop(n)
            
        result = []

        # we can't just check the map for the frequency here
        # since we have been decrementing, their true size might be bigger than minSize

        for n in freqMap:
            # nums.count(n) is an O(n) operation but since freqMap is O(2), O(2*n) is still O(n)
            if nums.count(n) > minSize: 
                result.append(n)
        
        return result
    
    def majorityElement_20260627(self, nums: List[int]) -> List[int]:
        # more than floor of n / 3, and we are adding all elements that fit that criteria
        # so is it easier to find elements less common
        # we'll need to keep the size of nums
        # one thing to note is that there can only be two elements that appear more than n / 3
        # so we can simulate O(1) space using a map of size 2
        # we can use this to keep track of frequency
        # we increment

        size = len(nums)
        
        freqMap = defaultdict(int)

        for n in nums:
            freqMap[n]+=1
            # if there are more than 2 elements in here
            # subtract 1 from each until we get one that is equal to zero
            # then we remove that element
            if len(freqMap) > 2:
                for key in freqMap:
                    freqMap[key]-=1
                # make a copy of freqMap in a list since we can't remove elements from it while looping through it
                for key in list(freqMap):
                    if freqMap[key] == 0:
                        freqMap.pop(key)

        # because we have been manipulating freqMap, we can't check if those values
        # are truly greater than n/3

        result = []

        for n in freqMap:
            if nums.count(n) > len(nums)//3:
                result.append(n)
        
        return result
    def majorityElement_20260629(self, nums: List[int]) -> List[int]:
        # key thing to note here is that there can never be more than 2 elements appearing more than n/3 times
        # so we keep a map of size 2
        # if we ever go beyond size 2, we decrement until the freq hits 0
        # then we remove them from the map

        freqMap = defaultdict(int)

        for n in nums:
            freqMap[n]+=1
            # if larger than size 2, decrement by 1 for all
            if len(freqMap) > 2:
                for key in freqMap:
                    freqMap[key]-=1
                # we can't modify a map while traversing it
                # so use a set or a list and remove the element with 0 value
                for key in set(freqMap):
                    if freqMap[key] == 0:
                        freqMap.pop(key)
        
        # now that we have two max, we need to check if they actually were the biggest
        minSize = len(nums)//3
        result = []
        for key in freqMap:
            if nums.count(key) > minSize:
                result.append(key)
        return result

    def majorityElement_20260712(self, nums: List[int]) -> List[int]:
        # key point: there can at most 2 elements that appear more than n/3 times
        # so we can keep a map and keep it at max of size 2 (initial thought was minHeap)
        # when we see an element that is already in the map, increment its freq
        # when we see an element that is not already in map, add it to the map
        # and if the size is greater than 2, decrement everything's frequency by 1 until there are only two elements left in the map

        freqMap = collections.defaultdict(int)

        for n in nums:
            freqMap[n]+=1
            if len(freqMap) > 2:
                # we can't remove a key from map while traversing over it
                # therefore we will just decrement for now
                for key,value in freqMap.items():
                    value-=1
                # use a list or set so we can pop out of the map
                for key in set(freqMap):
                    if freqMap[key] <= 0:
                        freqMap.pop(key)
        
        # now we have the elements, let's make sure these elements are actually valid
        minSize = n/3
        result = []
        for key in freqMap:
            keyCount = nums.count(key)
            if keyCount > minSize:
                result.append(key)
        return result

class UnitTest(unittest.TestCase):
    input = [1,1,2,2,3,3,1,2]
    output = [1,2]

    def testBoyerMoore(self):
        result = Solution().majorityElementBoyerMoore(self.input)
        self.assertEqual(result, self.output)

unittest.main()
