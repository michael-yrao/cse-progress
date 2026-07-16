"""
Docstring for dsa.leetcode.arrays_and_hash.912_sort_an_array

Given an array of integers nums, sort the array in ascending order and return it.

You must solve the problem without using any built-in functions in O(nlog(n)) time complexity and with the smallest space complexity possible.

Example 1:

Input: nums = [5,2,3,1]
Output: [1,2,3,5]
Explanation: After sorting the array, the positions of some numbers are not changed (for example, 2 and 3), while the positions of other numbers are changed (for example, 1 and 5).

Example 2:

Input: nums = [5,1,1,2,0,0]
Output: [0,0,1,1,2,5]
Explanation: Note that the values of nums are not necessarily unique.

Constraints:

    1 <= nums.length <= 5 * 104
    -5 * 104 <= nums[i] <= 5 * 104

"""

from typing import List

class Solution:

    # ── Attempt · 2026-07-15 ──────────────
    def sortArrayMergeSort_20260715(self, nums: List[int]) -> List[int]:
        # we will master the O(n) space solution of merge sort first
        
        # if 1 item or less, already sorted by default
        if len(nums) <= 1:
            return nums
        middle = len(nums)//2
        sortedLeft = self.sortArrayMergeSort_20260715(nums[:middle])
        sortedRight = self.sortArrayMergeSort_20260715(nums[middle:])
        
        def merge(left,right):
            result = []

            leftPointer = 0
            rightPointer = 0
            # while there are elements in both
            # compare values and put the smaller one in front
            while leftPointer < len(left) and rightPointer < len(right):
                if left[leftPointer] < right[rightPointer]:
                    result.append(left[leftPointer])
                    leftPointer+=1
                else:
                    result.append(right[rightPointer])
                    rightPointer+=1
            
            # now only one is left
            result+=left[leftPointer:]
            result+=right[rightPointer:]
            return result

        return merge(sortedLeft, sortedRight)
    
    def sortArrayMergeSort(self, nums: List[int]) -> List[int]:
        # recursive divide and conquer
        # using two pointer (left and right to keep track of the sub-arrays)
        # since its recursive, we should create a helper
    
        def merge(array, l, m, r):
            leftArray = array[l:m+1] # array[left:right] is inclusive of left and exclusive of right
            rightArray = array[m+1:r+1]

            # we'll use 3 pointers here
            # numsPointer to increment and perform the merge in source array starting from the left
            # leftPointer to traverse through leftArray
            # rightPointer to traverse through rightArray

            numsPointer, leftPointer, rightPointer = l, 0, 0

            while leftPointer < len(leftArray) and rightPointer < len(rightArray):
                if leftArray[leftPointer] < rightArray[rightPointer]:
                    array[numsPointer] = leftArray[leftPointer]
                    leftPointer+=1
                else:
                    array[numsPointer] = rightArray[rightPointer]
                    rightPointer+=1
                numsPointer+=1

            # handle case where original array is skewed
            # thus we are exiting prior while without having through all of both arrays

            while leftPointer < len(leftArray):
                array[numsPointer] = leftArray[leftPointer]
                leftPointer+=1
                numsPointer+=1
            
            while rightPointer < len(rightArray):
                array[numsPointer] = rightArray[rightPointer]
                rightPointer+=1
                numsPointer+=1
            
        def mergeSort(array, l, r):
            # two pointer to keep track of sub-arrays
            # base case: array size = 1, which means l = r
            if l == r:
                return array
            # split the array in half to recurse through
            m = (l + r) // 2
            # split arrays recursively halving each time
            mergeSort(array, l, m)
            mergeSort(array, m+1, r)
            # merge the split arrays
            merge(array, l, m, r)
            return array
        
        return mergeSort(nums, 0, len(nums)-1)
