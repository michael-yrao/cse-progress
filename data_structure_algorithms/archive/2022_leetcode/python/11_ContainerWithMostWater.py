from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        # We can do a 2 pointer technique here
        # 1. Create a curMax variable as result variable
        # 2. We get bottlenecked by smaller of the two ends
        # 3. Thus, we will use l,r=0,len-1 and move whichever is smallest
        # Area = (r - l) * min(r,l)
        curMax=0
        l,r=0,len(height)-1
        while l < r:
            curArea = (r - l) * min(height[r],height[l])
            curMax = max(curMax,curArea)
            if height[l] < height[r]:
                l+=1
            else:
                r-=1
        return curMax
