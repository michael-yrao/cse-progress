"""
853. Car Fleet   ·   https://leetcode.com/problems/car-fleet/
Pattern: stack

There are n cars at given miles away from the starting mile 0, travelling to reach the mile target.

You are given two integer arrays position and speed, both of length n, where position[i] is the
starting mile of the ith car and speed[i] is the speed of the ith car in miles per hour.

A car cannot pass another car, but it can catch up and then travel next to it at the speed of the
slower car.

A car fleet is a car or cars driving next to each other. The speed of the car fleet is the minimum
speed of any car in the fleet.

If a car catches up to a car fleet at the mile target, it will still be considered as part of the
car fleet.

Return the number of car fleets that will arrive at the destination.

Example 1:
  Input:  target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
  Output: 3
  Explanation: The cars starting at 10 (speed 2) and 8 (speed 4) become a fleet, meeting each other
  at 12. The fleet forms at target. The car starting at 0 (speed 1) does not catch up to any other
  car, so it is a fleet by itself. The cars starting at 5 (speed 1) and 3 (speed 3) become a fleet,
  meeting each other at 6. The fleet moves at speed 1 until it reaches target.

Example 2:
  Input:  target = 10, position = [3], speed = [3]
  Output: 1

Example 3:
  Input:  target = 100, position = [0,2,4], speed = [4,2,1]
  Output: 1

Constraints:
  n == position.length == speed.length
  1 <= n <= 10^5
  0 < target <= 10^6
  0 <= position[i] < target
  All the values of position are unique.
  0 < speed[i] <= 10^6
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-10-08 ──────────────
    def carFleet_20261008(self, target: int, position: List[int], speed: List[int]) -> int:
        # position matters, nothing can pass the positions in front
        # so we order by largest to smallest and see if anyone can catch up to the one in front
        # need to combine position and speed since they are together

        positions = []

        for i in range(len(position)):
            positions.append((position[i], speed[i]))
        
        positions.sort(reverse=True)

        fleet_times = []

        for pos, speed in positions:
            # need to get time it needs to get to target
            time_to_target = (target - pos) / speed
            # if this car's time to target is less or equal to prior
            # we can combine the fleet and do nothing
            # but if it is greater, then we add a new fleet
            if len(fleet_times) == 0 or time_to_target > fleet_times[-1]:
                fleet_times.append(time_to_target)
            
        return len(fleet_times)

    # ── Attempt · 2026-09-28 ──────────────
    def carFleet_20260928(self, target: int, position: List[int], speed: List[int]) -> int:
        # need to notice that position matters
        # the position in front can never be passed
        # so let's sort by position, we do need to create a new array since the indices in the two arrays need to be together
        # we then need to see how long it takes for each car to get to target

        car_position_and_speed = []
        
        for i in range(len(position)):
            car_position_and_speed.append((position[i], speed[i]))
        
        # do descending so we have the highest position first
        car_position_and_speed.sort(reverse=True)

        fleet = []

        for i in range(len(car_position_and_speed)):
            # (target - position) / speed is how long it takes i to get to target
            # we need a way to look at other car's time_to_target to see if we should add a new fleet
            time_to_target = (target - car_position_and_speed[i][0]) / car_position_and_speed[i][1]

            # if we form a new fleet, e.g. no fleet so far or we are slower than the latest, add in
            if not fleet or time_to_target > fleet[-1]:
                fleet.append(time_to_target)
        
        return len(fleet)

    # ── Attempt · 2026-08-29 ──────────────
    def carFleet_20260829(self, target: int, position: List[int], speed: List[int]) -> int:
        # main trick to notice with this problem is that if a car is in front
        # it will never be passed so we have to sort with highest position first
        # issue is that speed index is tied with position, so we need to make a new array
        # where we have them as tuples as sort by position
        # then if any cars catch up to the previous car, they are the same fleet

        cars = []

        for i in range(len(position)):
            cars.append((position[i],speed[i]))
        
        cars.sort(reverse=True)

        # now we keep track of who is in front and who NOT catchup
        # if any car catches up, it's the same fleet, so we can just ignore

        fleets = []

        for carPosition, carSpeed in cars:
            # we know 8,4 will catch up to 10,2 because given target
            # if they had no constraint, 8,4 will hit target at same time or faster
            carTime = (target - carPosition) / carSpeed
            # this means fleets should hold the time to finish
            
            # if nothing else in fleets, nothing to compare, new fleet
            if not fleets:
                fleets.append(carTime)
            # if carTime <=, that means it will become same fleet
            # so we add to the fleets array if > so it becomes a new fleet
            elif fleets and carTime > fleets[-1]:
                fleets.append(carTime)

        return len(fleets)

    # ── Attempt · 2026-08-17 ──────────────
    def carFleet_20260817(self, target: int, position: List[int], speed: List[int]) -> int:
        # first thing we should notice is that since we can't pass
        # starting position actually matters a lot, basically no one can pass the car in the front
        # because of this, we will sort desc. but we can't do that on the input
        # since position and speed indices are tied, so let's create a new tuple array to sort

        numCars = len(position)

        cars = []

        for i in range(numCars):
            cars.append((position[i], speed[i]))

        # descending since no one can pass the front car
        cars.sort(reverse=True)

        # now we need to check who can catch up to who
        # we need a way to determine how fast cars behind will finish
        # fastest for each car is (target - carPosition) / carSpeed
        # if a car is not to pass, it comes a second fleet
        # so we use a increasingStack that will hold time to finish
        # if a car is to pass, we neuter it and set it to current car's position and speed
        # so they become a fleet. we can accomplish this by just doing nothing

        increasingStack = []

        for carPosition, carSpeed in cars:
            time = (target - carPosition) / carSpeed
            
            # we only add to stack if time > increasingStack[-1] or increasingStack is empty
            if not increasingStack or time > increasingStack[-1]:
                increasingStack.append(time)
        
        return len(increasingStack)

    # ── Attempt 1 · 2026-08-15 ────────────────────────────────────────────
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        # sort based on position. these cars are closest to the finish line
        # so we order them in descending order since we can't pass cars
        # so cars in front are the limiting factor
        # we will have a monotonic stack that hold fleets
        # so if the car behind the latest car has a faster or equal finish time, it is part of same fleet
        # which means we check if time to finish > stack[-1]
        # so this is an increasing stack with time as the main factor
        
        increasingStack = []

        cars = []

        for i in range(len(position)):
            cars.append((position[i], speed[i]))
        
        # sort with highest first
        cars.sort(reverse=True)

        for carPosition, carSpeed in cars:
            # get time to finish for each car at current speed
            # which is (target - position) / speed, we don't use // since // doesn't even reach the target
            time = (target - carPosition) / carSpeed

            # since we cannot pass, it is impossible for cars behind each car iteration to finish earlier
            # we are using stack to keep track of total fleets, so if it takes longer, we add to stack
            if not increasingStack or time > increasingStack[-1]:
                increasingStack.append(time)
        
        return len(increasingStack)
