from typing import List

class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        # We only really care for the slots with 0s available
        # Therefore, what we should do is loop through the list
        # Keep track of all the slots with 0s
        # One 0 or two zeros can plant if one or both of the zeroes is the start/end of the list
        # Three 0s mean at least one flower can be planted
        # That said, a clean way of doing this is similar to Pascal's Triangle
        # Where we pad the beginning and end of the array
        # This way, we can always use the 3 0s methodology to validate if we can plant

        numFlowers = 0

        dummyFb = [0] + flowerbed + [0]

        for i in range(1,len(dummyFb)-1,1):
            if dummyFb[i-1] == 0 and dummyFb[i] == 0 and dummyFb[i+1] == 0:
                dummyFb[i] = 1
                numFlowers+=1
                if numFlowers == n:
                    return True
        return numFlowers>=n
    
    def canPlaceFlowersAlternative(self, flowerbed: List[int], n: int) -> bool:
        dummyFb = [0] + flowerbed + [0]
        for i in range(1,len(dummyFb)-1,1):
            if dummyFb[i-1] == 0 and dummyFb[i] == 0 and dummyFb[i+1] == 0:
                dummyFb[i] = 1
                n-=1
        return n<=0
