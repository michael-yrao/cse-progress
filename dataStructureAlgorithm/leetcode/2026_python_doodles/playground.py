import math
from typing import List

class Playground:
    class MergeSort_20260326:
        def sortArrayWithMergeSort(self, nums: List[int]) -> List[int]:
            # divide & conquer
        
            def merge(arr, l, r):
                m = (l + r) // 2
                # when we are here, we would have [5,2] that we want to make into the correct sequence
                # following divide and conquer, create a left and right side
                leftArray = arr[l:m+1]
                rightArray = arr[m+1:r+1]
                # go through the arrays and compare and put in result
                arrIterator = leftIterator = rightIterator = 0
                while leftIterator < len(leftArray) and rightIterator < len(rightArray):
                    if leftArray[leftIterator] < rightArray[rightIterator]:
                        arr[arrIterator] = leftArray[leftIterator]
                        leftIterator+=1
                    else:
                        arr[arrIterator] = rightArray[rightIterator]
                        rightIterator+=1
                    arrIterator+=1
                # if len(leftArray) != len(rightArray), we would need to put those at the end
                # do this for both
                while leftIterator < len(leftArray):
                    arr[arrIterator] = leftArray[leftIterator]
                    leftIterator+=1
                    arrIterator+=1
                while rightIterator < len(rightArray):
                    arr[arrIterator] = rightArray[rightIterator]
                    rightIterator+=1
                    arrIterator+=1
                
            def mergeSort(arr, l, r):
                # base case to stop divide is if l==r
                if l == r:
                    return arr
                m = (l+r) // 2
                mergeSort(arr, l, m)
                mergeSort(arr, m+1, r)
                # now that we divided, we need to merge them
                merge(arr, l, r)
                # now that we did divide and conquer, we return the result
                return arr
            return mergeSort(nums,0,len(nums)-1)
    class MajorityElement_20260401:
        def majorityElement(self, nums: List[int]) -> int:
            # the straight forward solution is to have a map of value -> freq
            # then return the value with the highest freq
            freqMap = {}
            for num in nums:
                freqMap[num] = 1 + freqMap.get(num,0)
            
            majorityValuePair = (None, 0)
            # go through the map and return the highest
            for key, value in freqMap.items():
                if value > majorityValuePair[1]:
                    majorityValuePair = (key, value)
            
            return majorityValuePair[0]
        
        def majorityElementVariation(self, nums: List[int]) -> int:
            # a slightly cleaner approach to the straight forward method 
            majorityValuePair = (None, 0)
            freqMap = {}
            for num in nums:
                freqMap[num] = 1 + freqMap.get(num,0)
                if freqMap[num] > majorityValuePair[1]:
                    majorityValuePair = num, freqMap[num]
            return majorityValuePair[0]

        def majorityElementBoyerMoore(self, nums: List[int]) -> int:
            # Boyer Moore assumes there is always a majority element in the array
            # As such, we can keep track of a max and a counter
            # we can't use a tuple because tuples are immutable
            # Increment/Decrement as we see/do not see it
            # Swap out if it hits negative
            maxValue = nums[0]
            maxCounter = 0
            for num in nums:
                if num == maxValue:
                    maxCounter+=1
                else:
                    maxCounter-=1
                    if maxCounter < 0:
                        maxValue = num
                        maxCounter = 1
            return maxValue
    class SortColor_20260401:
        def sortColorsBucketSort(self, nums: List[int]) -> None:
            # counting/bucket sort specifically works for this
            # bucket sort works by basically putting these values into buckets
            bucket = {}
            for num in nums:
                bucket[num] = 1 + bucket.get(num,0)
            counter = 0
            for i in range(3):
                while bucket.get(i):
                    nums[counter] = i
                    bucket[i] = -1 + bucket.get(i,0)
                    counter+=1
        def sortColorsDutchFlag(self, nums: List[int]) -> None:
            # knowing there's only 3 colors
            # we can use 3 pointers
            # l for keeping track of position to put 0s
            # r for keeping track of position to put 2s
            # another pointer to increment through the array
            def swap(l,r):
                temp = nums[l]
                nums[l] = nums[r]
                nums[r] = temp

            l, inc, r = 0, 0, len(nums) - 1
            while inc < len(nums):
                if nums[inc] == 0:
                    swap(l,inc)
                    l+=1
                elif nums[inc] == 2:
                    swap(r,inc)
                    r-=1
                    # we have to move inc back one so we evaluate the value swapped from r
                    inc-=1
                inc+=1
    class MaximumSubarray_20260401:
        def maxSubArrayPrefixSum(self, nums: List[int]) -> int:
            
            # finding subarray with largest sum
            # sliding window problem with dynamic window size
            # one approach is prefix sum
            # create prefixSum array
            # prefixSum[j] - prefixSum[i] = sum of subarray between i and j, exclusive of i
            # so we can keep track of a maximum sum
            # keep track of the smallest prefixSum[i] we can find
            # this way we maximize prefixSum[j] and minimize prefixSum[i]
            prefixSum = []
            for i in range(len(nums)):
                if i == 0:
                    prefixSum.append(nums[i])
                else:
                    prefixSum.append(nums[i] + prefixSum[i-1])
            
            # needs to be 0 to calc subarray of size 1, e.g. [1]
            minPrefixSum = 0
            maxSum = -math.inf

            # nums = [-2,1,-3,4,-1,2,1,-5,4]
            # prefixSum = [-2, -1, -4, 0, -1, 1, 2, -3, 1]

            for curSum in prefixSum:
                maxSum = max(maxSum, curSum - minPrefixSum)
                minPrefixSum = min(minPrefixSum, curSum)
            return maxSum
        def maxSubArrayKadane(self, nums: List[int]) -> int:
            # constant space dynamic sliding window algorithm
            # we can be greedy and not care for negative sums
            # e.g. if current sum is negative, discard it, start back at 0 at current index

            # start maxSum at first index
            # it should not be 0 since we have negatives
            # e.g. if result is negative and we start at 0, 0 will always be bigger and we will return 0 if we initialize to 0

            maxSum = nums[0]
            curMax = 0

            for n in nums:
                if curMax < 0:
                    curMax = 0
                curMax+=n
                maxSum=max(maxSum, curMax)
            
            return maxSum
    class RemoveDuplicatesFromSortedArray_20260402:
        def removeDuplicates(self, nums: List[int]) -> int:
            # two pointers
            # one pointer to traverse and find unique
            # another pointer for positioning
            # knowing index 0 is already correct, we can start at index 1
            # then check index - 1 for equality
            left = right = counter = 1
            while right < len(nums):
                if nums[right] != nums[left - 1]:
                    nums[left] = nums[right]
                    left+=1
                    counter+=1
                right+=1
            return counter
    class MoveZeroes_20260402:
        def moveZeroes(self, nums: List[int]) -> None:
            """
            Do not return anything, modify nums in-place instead.
            """
            # two pointer
            # we don't start left = 0, right = len(nums) - 1 since we want to preserve order
            # so we do left as position to swap
            # right as the traversing pointer
            def swap(l,r):
                temp = nums[left]
                nums[left] = nums[right]
                nums[right] = temp

            left = right = 0
            while right < len(nums):
                if nums[right] != 0:
                    swap(left,right)
                    left+=1
                right+=1