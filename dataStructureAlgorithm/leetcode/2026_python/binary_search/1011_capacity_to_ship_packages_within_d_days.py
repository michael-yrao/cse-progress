"""
A conveyor belt has packages that must be shipped from one port to another within days days.

The ith package on the conveyor belt has a weight of weights[i]. Each day, we load the ship with packages on the conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.

Example 1:

Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
Output: 15
Explanation: A ship capacity of 15 is the minimum to ship all the packages in 5 days like this:
1st day: 1, 2, 3, 4, 5
2nd day: 6, 7
3rd day: 8
4th day: 9
5th day: 10

Note that the cargo must be shipped in the order given, so using a ship of capacity 14 and splitting the packages into parts like (2, 3, 4, 5), (1, 6, 7), (8), (9), (10) is not allowed.

Example 2:

Input: weights = [3,2,2,4,1,4], days = 3
Output: 6
Explanation: A ship capacity of 6 is the minimum to ship all the packages in 3 days like this:
1st day: 3, 2
2nd day: 2, 4
3rd day: 1, 4

Example 3:

Input: weights = [1,2,3,1,1], days = 4
Output: 3
Explanation:
1st day: 1
2nd day: 2
3rd day: 3
4th day: 1, 1

Constraints:

    1 <= days <= weights.length <= 5 * 104
    1 <= weights[i] <= 500
"""
from typing import List

class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        # ordering matters, so can't sort
        # seems like what we are doing is getting the min boundary for each day
        # so sum(weights)/days is at minimum the capacity we need if we can split up the weights, which we cannot
        # then sum(weights) is a guarantee that we can ship all in one day
        # so what we can do is binary search min boundary with those two
        # so above thought for minimum capacity is wrong, since we will never be able to ship some packages
        # e.g. [1,1,1,1,10], days = 5
        # sum(weights)//days = 2, which means we will never be able to ship out the 10
        # the minimum boundary of sum(weights)//days is unfortunately just logically impossible
        # thus we don't start with it
        
        def canShip(dailyCapacity):
            daysNeeded = 1
            currentLoad = 0
            
            for weight in weights:
                if currentLoad + weight > dailyCapacity:
                    daysNeeded+=1
                    currentLoad=0
                currentLoad+=weight
            return daysNeeded <= days

        l = max(weights)
        r = sum(weights)

        while l < r:
            mid = (l + r) // 2
            # criteria is that we are able to ship
            # so let's find the smallest possible to ship
            if canShip(mid):
                r=mid
            else:
                l=mid+1 
        return l