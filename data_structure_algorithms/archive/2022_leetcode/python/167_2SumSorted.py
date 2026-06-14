from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        # Since list is already sorted
        # We can actually just sum left and right
        # Move our pointers dependent on whether we are over or under

        l,r=0,len(numbers)-1

        while r>l:
            sum=numbers[r] + numbers[l]
            if sum == target:
                return [l+1,r+1]
            elif sum < target:
                l+=1
            else:
                r-=1
        return [-1,-1]
        