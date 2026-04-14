import heapq
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
    class MergeSortedArray_20260403:
        def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
            """
            Do not return anything, modify nums1 in-place instead.
            """
            # sort from the end since we known num1 length covers entirety of m + n
            # three pointers, leftIterator and rightIterator tracks nums1 and nums2
            # arrIterator tracks position to place the value
            arrIterator = m + n - 1
            leftIterator = m - 1
            rightIterator = n - 1
            # while we are in bound for both
            while leftIterator >= 0 and rightIterator >= 0:
                if nums1[leftIterator] > nums2[rightIterator]:
                    nums1[arrIterator] = nums1[leftIterator]
                    leftIterator-=1
                else:
                    nums1[arrIterator] = nums2[rightIterator]
                    rightIterator-=1
                arrIterator-=1
            # now we cover the rest of the array
            # only one of these loops will run
            while leftIterator >= 0:
                nums1[arrIterator] = nums1[leftIterator]
                leftIterator-=1
                arrIterator-=1
            while rightIterator >= 0:
                nums1[arrIterator] = nums2[rightIterator]
                rightIterator-=1
                arrIterator-=1
    class RotateArray_20260404:
        def rotate(self, nums: List[int], k: int) -> None:
            """
            Do not return anything, modify nums in-place instead.
            """
            # rotation algorithm
            # reverse array
            # reverse first k elements, exclusive of k. so k-1
            # reverse len(nums)-k elements

            def reverseArray(l,r):
                def swap(l,r):
                    temp = nums[l]
                    nums[l] = nums[r]
                    nums[r] = temp
                while r > l:
                    swap(l,r)
                    l+=1
                    r-=1
            # edge case when k is larger than length
            k=k%len(nums)
            reverseArray(0,len(nums)-1)
            reverseArray(0,k-1)
            reverseArray(k,len(nums)-1)
    class ValidPalindromeII_20260405:
        def validPalindrome(self, s: str) -> bool:
        # main scenarios that come to mind are these
        # abca -> True
        # abcbda -> True
        # two pointer but do a skip ahead check for both sides

            def skippable(l,r):
                while l < r:
                    if s[l] == s[r]:
                        # continue
                        l+=1
                        r-=1
                    else:
                        return False
                return True

            l, r = 0, len(s)-1
            while l < r:
                if s[l] == s[r]:
                    # continue
                    l+=1
                    r-=1
                else:
                    # otherwise, we check if we can skip either sides
                    return skippable(l+1, r) or skippable(l,r-1)
            return True
    class SubarraySumEqualsK_20260405:
        def subarraySum(self, nums: List[int], k: int) -> int:
            # first thing that comes to mind is prefixSum
            # property of prefixSum
            # prefixSum[j] - prefixSum[i] = subarraySum from i to j
            # so we can say k is subarraySum from i to j
            # and we want to find all occurences of it
            # so we can do something like two sum where we look for the diff in a hashmap
            # we will calculate prefixSum and put it in a hashmap instead of an array
            # since we are doing that, we need a runningSum variable to keep track of prefixSum

            prefixMap = {}
            # we need to add 0 to map first to account for scenario where runningSum = k
            prefixMap[0] = 1
            runningSum = 0
            totalCount = 0
            for n in nums:
                # increment our runningSum
                runningSum+=n
                # check if this k-runningSum already exists
                totalCount+=prefixMap.get(runningSum - k,0)
                # add new runningSum to our prefixSum map
                prefixMap[runningSum] = 1 + prefixMap.get(runningSum,0)
            return totalCount
    class ThreeSum_20260407:
        def threeSum(self, nums: list[int]) -> list[list[int]]:
            # sort the array
            # use sorted 2 sum method
            # a + b + c = 0
            # loop on a, two sum sorted method to find b and c
            threeSumSet = set()
            nums.sort()
            for i in range(len(nums)):
                # two sum sorted
                j = i + 1
                k = len(nums) - 1
                while j < k:
                    if nums[i] + nums[j] + nums[k] == 0:
                        solution = (nums[i],nums[j],nums[k])
                        threeSumSet.add(solution)
                        j+=1
                        k-=1
                    elif nums[i] + nums[j] + nums[k] > 0:
                        k-=1
                    else:
                        j+=1
            return list(threeSumSet)
    class TopKFrequentElements_20260409:
        def topKFrequent(self, nums: List[int], k: int) -> List[int]:
            # frequency, so we should do a map
            # then we can keep a min heap of size k
            # return said heap's values
            freqMap = {}
            for n in nums:
                freqMap[n] = 1 + freqMap.get(n,0)
            
            minHeap = []

            for key,value in freqMap.items():
                # need to do value, key since minHeap will compare on first value in tuple
                heapq.heappush(minHeap, (value, key))
                while len(minHeap) > k:
                    heapq.heappop(minHeap)
            
            result = []
            for freq, key in minHeap:
                result.append(key)
            return result
    class RemoveDuplicatesFromSortedArrayII:
        def removeDuplicates(self, nums: List[int]) -> int:
            # O(1) space means we need multiple pointers
            # First 2 elements of the array are always valid
            # Thus we start looking at index 2
            # we will use l to keep track of index to replace
            # r to traverse through the array
            # [1,2,2,2,3,3,4]
            # looking at the above example, we should always check nums[r] == nums[l-2]
            # any equality means it is invalid and needs to be replaced

            l = r = 2

            while r < len(nums):
                # everything before l = good
                # everything at l = replace
                # not equal means we can replace and move l up
                if nums[r] != nums[l-2]:
                    nums[l] = nums[r]
                    l+=1
                # equal means we need to keep l in place to perform replacements
                r+=1
            return l
    class SearchInRotatedSortedArray:
        def search(self, nums: List[int], target: int) -> int:
            # if we are looking for logn time, we can't go through the array to find k
            # we should binary search to find k
            # then binary search on the 2 halves
            # k is smallest value, thus we do binary search on smallest value
            # since we are not looking for an exact value, we should do while l < r instead of while l <= r
            # Want exact target index? l <= r
            # Want first/last occurrence or smallest pivot? l < r
            # If one branch keeps mid as possible answer, prefer l < r
            # If both branches exclude mid, use l <= r

            l, r = 0, len(nums) - 1

            while l < r:
                mid = (l+r) // 2
                if nums[mid] > nums[r]:
                    l = mid + 1
                else:
                    r = mid
            
            k = l

            # binary search on both halves

            def binarySearch(l,r) -> int:
                while l<=r:
                    mid = (l+r)//2
                    if nums[mid] == target:
                        return mid
                    elif nums[mid] > target:
                        r = mid - 1
                    else:
                        l = mid + 1
                return -1
            
            result = binarySearch(0,k-1)
            if result == -1:
                result = binarySearch(k,len(nums)-1)
            
            return result
    class ProductOfArrayExceptSelf:
        def productExceptSelf(self, nums: List[int]) -> List[int]:
            # prefix and suffix product arrays
            # then loop through and just do result[i] = prefix[i] * suffix[i]
            # [1,2,3,4]
            # prefix: [1,1,2,6]
            # suffix: [24,12,4,1]
            # result = [24,12,8,6]

            prefix = [1] * len(nums)
            suffix = [1] * len(nums)
            result = [1] * len(nums)

            for i in range(1,len(nums)):
                prefix[i] = prefix[i-1] * nums[i-1]
            
            for i in range(len(nums)-2,-1,-1):
                suffix[i] = suffix[i+1] * nums[i+1]

            for i in range(len(nums)):
                result[i] = prefix[i] * suffix[i]

            return result
    class LongestConsecutiveSequence:
        def longestConsecutiveV1(self, nums: List[int]) -> int:
            if not nums:
                return 0
            
            num_set = set(nums)
            longest = 0
            
            for num in num_set:
                # Check if this is the start of a sequence
                if num - 1 not in num_set:
                    current = num
                    count = 1
                    
                    # Keep extending the sequence
                    while current + 1 in num_set:
                        current += 1
                        count += 1
                    
                    # Update the longest sequence found
                    longest = max(longest, count)
            
            return longest
        def longestConsecutive(self, nums: List[int]) -> int:
            # we need to know if current value is start of a sequence
            # so we should have a map? or a set?, key is the start sequence, value is length?
            # we don't actually need to keep track of all lengths
            # we can just assume we are at the start at each index so a set will suffice
            # go through each value, loop to see if value - 1 exists

            if not nums:
                return 0
            consecutiveSet = set(nums)
            longest = 0

            for num in consecutiveSet:
                if (num - 1) not in consecutiveSet:
                    # if starting point, length is 1
                    length = 1
                    # since we are starting point, let's check num + 1 until it's not in the set
                    while (num + length) in consecutiveSet:
                        length += 1
                    longest = max(longest,length)

            return longest