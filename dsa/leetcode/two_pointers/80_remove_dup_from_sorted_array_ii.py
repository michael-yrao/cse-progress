"""
Docstring for dsa.leetcode.two_pointers.80_remove_dup_from_sorted_array_ii
Given an integer array nums sorted in non-decreasing order, remove some duplicates in-place such that each unique element appears at most twice. The relative order of the elements should be kept the same.

Since it is impossible to change the length of the array in some languages, you must instead have the result be placed in the first part of the array nums. More formally, if there are k elements after removing the duplicates, then the first k elements of nums should hold the final result. It does not matter what you leave beyond the first k elements.

Return k after placing the final result in the first k slots of nums.

Do not allocate extra space for another array. You must do this by modifying the input array in-place with O(1) extra memory.

Custom Judge:

The judge will test your solution with the following code:

int[] nums = [...]; // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}

If all assertions pass, then your solution will be accepted.

 

Example 1:

Input: nums = [1,1,1,2,2,3]
Output: 5, nums = [1,1,2,2,3,_]
Explanation: Your function should return k = 5, with the first five elements of nums being 1, 1, 2, 2 and 3 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).

Example 2:

Input: nums = [0,0,1,1,1,1,2,3,3]
Output: 7, nums = [0,0,1,1,2,3,3,_,_]
Explanation: Your function should return k = 7, with the first seven elements of nums being 0, 0, 1, 1, 2, 3 and 3 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).

 

Constraints:

    1 <= nums.length <= 3 * 104
    -104 <= nums[i] <= 104
    nums is sorted in non-decreasing order.

"""
from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # we are given length is >= 1
        # so first element is always part of solution
        # thus we iterate starting at index 1
        # since request is O(1) memory to look through an array
        # algorithm choice would be two pointers
        # we will use one pointer to iterate through
        # second pointer to keep track of return array
        # where everything before it is valid

        # if 2 or less elements, we already satisfy the solution
        # thus we can just return
        if len(nums) < 3:
            return len(nums)

        ptr = 2

        for i in range(2,len(nums)):
            # moving ptr means we are adding element to the result
            # thus we move ptr if nums[i] should go into result
            # if nums[i] != nums[ptr-2], it means we can add it
            # ptr-2 since that satisfies the criteria of max of 2
            if nums[i] != nums[ptr-2]:
                nums[ptr] = nums[i]
                ptr+=1
            # if nums[i] == nums[ptr-2], we don't want it in result
            # thus we keep ptr where it is
        return ptr

    def removeDuplicates_20260625(self, nums: List[int]) -> int:
        # we use a left and right pointer
        # left pointer keep tracks of where to write
        # first 2 elements will never be removed, so we start at index 2

        l = r = 2

        while r < len(nums):
            # if nums[r] == nums[l-2], then we want to keep l in place
            # since we want to replace it with the next value
            if nums[r] == nums[l-2]:
                r+=1
                continue
            # if not the same, replace nums[l] with nums[r] and increment l
            else:
                nums[l] = nums[r]
                l+=1
            r+=1
        return l
    def removeDuplicates_20260627(self, nums: List[int]) -> int:
        # we know first 2 characters will never get removed
        if len(nums) < 3:
            return len(nums)
        
        # if we are 3 or more, we want to do two pointers
        # left to keep track where to replace
        # right to traverse and read
        l = r = 2

        while r < len(nums):
            # l - 2 is the golden source
            # since we know that is correct
            # [1,1,2,2,3,3]
            #          l
            #            r
            if nums[r] != nums[l-2]:
                nums[l] = nums[r]
                l+=1
            r+=1
        return l
    def removeDuplicates_20260711(self, nums: List[int]) -> int:
        # we are removing duplicates and not searching, thus not binary search
        # this seems like a two pointer problem where we have a left pointer that tells us where to place the next number and right pointer to traverse
        # we never replace the first two characters since a char can appear 2x
        # so we just start at index 2
        # so we know nums[l-2] and nums[l-1] are always correct
        # a number is invalid if it is equal to nums[l-2] since that means it is appearing 3x
        # so when a number is valid, aka nums[r] != nums[l-2], we should place nums[r] at l and move l forward

        if len(nums) < 3:
            return len(nums)
        
        l = r = 2

        while r < len(nums):
            if nums[r] != nums[l-2]:
                nums[l] = nums[r]
                l+=1
            r+=1
        
        return l