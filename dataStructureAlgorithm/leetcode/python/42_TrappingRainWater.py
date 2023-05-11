from typing import List
import unittest

class Solution:    
    # Observation: Need to know left/right boundaries of anything being trapped
    # This suggests a use of two pointer technique (pointers l and r)
    # Not sure how we can determine these l,r boundaries just yet
    # Water that can be gathered at each index is bottlenecked by min(l,r)
    # At each index, the formula would be min(l,r) - height[i]
    
    def trap(self, height: List[int]) -> int:
        # If we take a look at our linear memory solution
        # We will notice it is not really necessary to know the higher value
        # Therefore, we will move our l,r pointers in according to whichever is smaller
        # With that, we can try to determine how much water there is at each index
        
        # this solution requires an edge case where height is empty
        if not height: 
            return 0
        
        l,r=0,len(height)-1
        maxLeft,maxRight=height[l],height[r]
        result = 0

        while l < r:
            if maxLeft < maxRight:
                l+=1
                maxLeft = max(maxLeft,height[l])
                result += maxLeft - height[l]
            else:
                r-=1
                maxRight = max(maxRight,height[r])
                result += maxRight - height[r]
        return result

    def trapLinearMemory(self, height: List[int]) -> int:
        # One way to do left/right boundaries if to find max left and max right of every index
        # This means we need additional arrays to keep track

        length = len(height)
        maxLeft,maxRight=[0] * length, [0] * length
        curMax=0
        result=0
        for i in range(len(height)):
            maxLeft[i]=curMax
            curMax=max(curMax,height[i])
        
        curMax=0
        for i in range(len(height)-1,-1,-1):
            maxRight[i]=curMax
            curMax=max(curMax,height[i])

        for i in range(len(height)):
            water = min(maxLeft[i],maxRight[i]) - height[i]
            if water>0:
                result+=water        
        return result
        

class UnitTest(unittest.TestCase):
    def testValidPalindromeII(self):
        input = [0,1,0,2,1,0,1,3,2,1,2,1]
        expectedAnswer = 6
        result = Solution().trapLinearMemory(input)
        self.assertEqual(expectedAnswer,result)

unittest.main()

        
