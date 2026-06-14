"""

MEDIUM

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

    For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.

 

Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].

Example 2:

Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3]
Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].

Example 3:

Input: numCourses = 1, prerequisites = []
Output: [0]

 

Constraints:

    1 <= numCourses <= 2000
    0 <= prerequisites.length <= numCourses * (numCourses - 1)
    prerequisites[i].length == 2
    0 <= ai, bi < numCourses
    ai != bi
    All the pairs [ai, bi] are distinct.

"""
import collections
from typing import List

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # so same idea as course schedule 1
        # we need to find starting nodes to go for
        # so we once again need a way to indicate whether a course is takeable
        # so we will use canTake = [0] * numCourses
        # then we will have a map of prereq -> courses
        # traverse through the neighbors and add to a result list as we take each course
        # one thing we do need to consider is cycles
        # so how do we detect cycles in a graph

        canTake = [0] * numCourses

        prereqMap = collections.defaultdict(list)

        courseList = []

        for row in prerequisites:
            course = row[0]
            prereq = row[1]
            # increase requirement for this course
            canTake[course]+=1
            # append to prereq
            prereqMap[prereq].append(course)
        
        # now we go through the canTake array and put everything takeable now into the queue for BFS
        
        courseQueue = collections.deque()
        
        for i in range(len(canTake)):
            if canTake[i] == 0:
                courseQueue.append(i)
        
        # with this initial list of takeable classes, we start BFS

        while courseQueue:
            currentCourse = courseQueue.popleft()
            # we mark this as taken by adding to the result
            courseList.append(currentCourse)
            # now we check neighbors of this and add to the list if they are takeable
            for neighbor in prereqMap[currentCourse]:
                canTake[neighbor]-=1
                # if takeable, add to queue
                if canTake[neighbor] <= 0:
                    courseQueue.append(neighbor)
        
        if numCourses != len(courseList):
            return []
        else:
            return courseList

    def findOrder_20260613(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # this is basically identical to course schedule i
        # 1. get counter of how many prereq a course needs before taking
        # 2. map prereq -> list[courses]
        # 3. get list of courses we can take now
        # 4. add course into result as we take them

        prereqMap = collections.defaultdict(list)

        prereqCounter = [0] * numCourses

        for row in prerequisites:
            course = row[0]
            prereqCounter[course]+=1
            prereq = row[1]
            prereqMap[prereq].append(course)
        
        canTake = collections.deque()

        for i in range(len(prereqCounter)):
            if prereqCounter[i] == 0:
                canTake.append(i)
        
        result = []

        while canTake:
            currentCourse = canTake.popleft()
            # take current course
            result.append(currentCourse)

            # check neighbors
            for course in prereqMap[currentCourse]:
                # since we took the course, decrement counter
                prereqCounter[course]-=1
                if prereqCounter[course] == 0:
                    canTake.append(course)
        
        if len(result) < numCourses:
            return []
        else:
            return result