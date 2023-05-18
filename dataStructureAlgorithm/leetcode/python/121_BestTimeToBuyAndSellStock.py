from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # * We can't buy after we sell, so we should just use sliding window
        # * Key difference between Two Pointers and Sliding Window:
        # * l,r=0,len-1 for Two Pointer
        # * l,r=0,0 or 0,1 for Sliding Window
        # * In this case, we should do 0,1 sliding window since we can't buy/sell the same day
        # * Cases:
        # * profit<0: move both l and r
        # * profit>0: keep track of max profit variable, keep moving r

        l,r=0,1
        maxProfit=0

        while r < len(prices):
            if prices[r] < prices[l]:
                l=r
            else:
                maxProfit=max(maxProfit,prices[r]-prices[l])
            r+=1
        
        return maxProfit