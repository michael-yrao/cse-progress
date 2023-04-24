from typing import List
import unittest

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Since we can't have dup answers, we'll just use a set
        result = set()

        nums.sort()

        for a in range(0,len(nums),1):
            b,c=a+1,len(nums)-1
            while b<c:
                total = nums[a] + nums[b] + nums[c]
                if total > 0:
                    c-=1
                elif total < 0:
                    b+=1
                else:
                    result.add((nums[a],nums[b],nums[c]))
                    b+=1 # Since indices b and c were already used, increment both
                    c-=1
        return result
    
    def threeSumAlternative(self, nums: List[int]) -> List[List[int]]:
        result = []

        nums.sort()

        for i in range(len(nums)):
            l,r = i+1, len(nums) - 1
            if i > 0 and nums[i] == nums[i-1]:
                continue
            while l < r:
                total = nums[i] + nums[l] + nums[r]
                if total > 0:
                    r -= 1
                elif total < 0:
                    l += 1
                else:
                    result.append([nums[i],nums[l],nums[r]])
                    # l and r have been used already, increment both
                    l += 1 
                    r -= 1
                    # avoid duplicates by avoiding any numbers that are the same
                    while l < r and nums[l] == nums[l-1]:
                        l += 1
                    while l < r and nums[r] == nums[r+1]:
                        r -= 1
        return result
    
class UnitTest(unittest.TestCase):
    def testThreeSum(self):
        inputArray = [-1,0,1,2,-1,-4]
        expectedAnswer = [[-1,-1,2],[-1,0,1]]
        result = Solution().threeSumAlternative(inputArray)
        self.assertEquals(expectedAnswer,result)

unittest.main()