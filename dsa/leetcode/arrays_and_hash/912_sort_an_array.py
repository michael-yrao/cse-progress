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

    # ── Attempt · 2026-08-08 ──────────────
    def sortArrayMergeSort_20260808(self, nums: List[int]) -> List[int]:
        # merge sort - divide and conquer

        def merge(arr1, arr2):
            mergedArray = []
            index1 = index2 = 0
            while index1 < len(arr1) and index2 < len(arr2):
                if arr1[index1] < arr2[index2]:
                    mergedArray.append(arr1[index1])
                    index1+=1
                else:
                    mergedArray.append(arr2[index2])
                    index2+=1
                
            # append rest of the array
            while index1 < len(arr1):
                mergedArray.append(arr1[index1])
                index1+=1
            while index2 < len(arr2):
                mergedArray.append(arr2[index2])
                index2+=1

            return mergedArray

        def mergeSort(inputArray):
            # if an array is length of 1 or less, it is already sorted
            if len(inputArray) <= 1:
                return inputArray
            # divide by half of the array
            midPoint = len(inputArray)//2

            leftSide = mergeSort(inputArray[:midPoint])
            rightSide = mergeSort(inputArray[midPoint:])

            # now we merge these two sides
            return merge(leftSide, rightSide)
        
        return mergeSort(nums)

    # ── Attempt · 2026-07-29 ──────────────
    def sortArrayMergeSort_20260729(self, nums: List[int]) -> List[int]:
        # merge sort
        # key to remember is that we do divide AND conquer
        # they are not separate pieces

        def merge(leftArray, rightArray):
            li = ri = 0
            result = []
            while li < len(leftArray) and ri < len(rightArray):
                if leftArray[li] < rightArray[ri]:
                    result.append(leftArray[li])
                    li+=1
                else:
                    result.append(rightArray[ri])
                    ri+=1
            
            result+=(leftArray[li:])
            result+=(rightArray[ri:])
            
            return result

        def mergeSort(nums):
            # if size is <= 1, then it is sorted
            if len(nums) <= 1:
                return nums
            m = len(nums)//2
            leftSide = mergeSort(nums[:m])
            rightSide = mergeSort(nums[m:])

            # now that we got both sides, we merge them
            return merge(leftSide,rightSide)
        
        return mergeSort(nums)

    # ── Attempt · 2026-07-25 ──────────────
    def sortArrayMergeSort_20260725(self, nums: List[int]) -> List[int]:
        # divide and conquer via merge sort
        # main thing to remember, D&C is a strategy not a framework
        # so don't think of it as divide method and merge method
        # we are dividing and then merging in the same function
        # one down the stack, one up the stack

        def merge(leftArray, rightArray):
            # we assume left and right side are sorted
            resultArray = []
            li = ri = 0
            while li < len(leftArray) and ri < len(rightArray):
                if leftArray[li] < rightArray[ri]:
                    resultArray.append(leftArray[li])
                    li+=1
                else:
                    resultArray.append(rightArray[ri])
                    ri+=1
            while li < len(leftArray):
                resultArray.append(leftArray[li])
                li+=1
            while ri < len(rightArray):
                resultArray.append(rightArray[ri])
                ri+=1
            return resultArray

        def mergeSort(inputArray):
            # if inputArray is size 1 or less, we don't need to divide
            if len(inputArray) <= 1:
                return inputArray
            # otherwise, we find the middle point and divide them up
            mid = len(inputArray) // 2
            leftSide = mergeSort(inputArray[:mid])
            rightSide = mergeSort(inputArray[mid:])
            return merge(leftSide, rightSide)
        
        return mergeSort(nums)

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
