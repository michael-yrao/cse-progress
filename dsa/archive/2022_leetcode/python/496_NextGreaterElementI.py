from typing import List

class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # From a glance, seems best case is O(n1 * n2) since we have to go through both of these regardless.
        # There is however a O(nums1 + nums2) solution that uses monotone stack
        # This problem becomes a MEDIUM/HARD problem easily if O(n1 + n2) is required
        # 1. We will use a map to keep track of nums1 value -> index
        #    as it is required to know where to place our result values
        # 2. Create a monotone decreasing stack, 
        #    when we see a value that is not monotonically decreasing, 
        #    we pop stack until not decreasing
        # 3. We will only push in numbers that are in nums1 into the stack

        # python magic
        map = { n:i for i,n in enumerate(nums1) }

        # Initialize res to all -1 assuming no element has NGE
        res = [-1] * len(nums1)
        
        stack = []
    
        for i in range(len(nums2)):
            # Check if current value is next greater element to anything in stack
            currentValue = nums2[i]
            while stack and currentValue > stack[-1]:
            # Since it is the NGE, we want to now find the index to put in result
                value = stack.pop()
                index = map[value]
                res[index] = currentValue
            # If this value is part of nums1, we want to push them onto the stack
            if currentValue in map:
                stack.append(currentValue)
        return res

    def nextGreaterElementBasic(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # We want to have a map of nums1 value -> index,
        # since it's possible the values don't appear in nums2,
        # and our solution is dependent on the indices of the nums1

        # python magic
        map = { n:i for i,n in enumerate(nums1) }

        # Initialize res to all -1 assuming no element has NGE
        res = [-1] * len(nums1)

        for i in range(len(nums2)):
            # This value is not in nums1, so we will move forward
            if nums2[i] not in map:
                continue
            # Now that we have found a matching number, we want to find the next greater element
            for j in range(i + 1, len(nums2)):
                if nums2[j] > nums2[i]:
                    # We have found a next greater element
                    # Index is where we want to put our result
                    index = map[nums2[i]]
                    # Put the result in that index in the result
                    res[index] = nums2[j]
                    # Since we found the result for this value, we can just break out of this loop
                    break
        return res