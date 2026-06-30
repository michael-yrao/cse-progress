"""
Docstring for dataStructureAlgorithm.leetcode.2026_python.arrays_and_hash.128_longest_consecutive_sequence
Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example 1:

Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

Example 2:

Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9

Example 3:

Input: nums = [1,0,1,2]
Output: 3

Constraints:

    0 <= nums.length <= 105
    -109 <= nums[i] <= 109

"""
from collections import defaultdict
from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numSet = set(nums)
        longestSequence = 0
        for n in nums:
            # only start looping if n is the start of the sequence
            if n-1 not in numSet:
                currentLongest=1
                while n+currentLongest in numSet:
                    currentLongest+=1
                longestSequence = max(longestSequence, currentLongest)
        return longestSequence
    
    def longestConsecutiveMap(self, nums: List[int]) -> int:
        numSet = set(nums)
        numMap = {}
        longest = 0

        for n in numSet:
            # numMap[n-1] = length ending at n-1
            leftSequenceLength = numMap.get(n-1,0)
            # numMap[n+1] = length starting at n+1
            rightSequenceLength = numMap.get(n+1,0)
            # Add left sequence length, right sequence length and 1 for current value to get current sequence length
            numMap[n] = leftSequenceLength + rightSequenceLength + 1
            # set starting left sequence to new value
            numMap[n-leftSequenceLength] = numMap[n]
            # set ending right sequence to new value
            numMap[n+rightSequenceLength] = numMap[n]
            longest = max(longest, numMap[n])
            
        return longest
    
    def longestConsecutive_20260627(self, nums: List[int]) -> int:
        # we maintain a set to keep track of the numbers in the list
        # this way we can access the values in O(1) time and also take care any duplicates
        numSet = set(nums)
        
        maxLength = 0
        
        for n in numSet:
            # we only care if we are start of a sequence
            if n - 1 not in numSet:
                currentLength = 1
                while n + currentLength in numSet:
                    currentLength+=1
                maxLength = max(maxLength, currentLength)
        
        return maxLength
    def longestConsecutive_20260629(self, nums: List[int]) -> int:
        # key to this problem is that we don't want to do anything unless we are start of the sequence
        # convert nums to a set to take care of duplicates
        # then go through the set and only do something if we are start of sequence
        numSet = set(nums)
        maxConsecutive = 0
        for n in numSet:
            if n - 1 not in numSet:
                counter = 1
                while n + counter in numSet:
                    counter+=1
                maxConsecutive = max(maxConsecutive, counter)
        
        return maxConsecutive