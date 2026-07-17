"""

MEDIUM

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

    For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return true if you can finish all courses. Otherwise, return false.

 

Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.

Example 2:

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

 

Constraints:

    1 <= numCourses <= 2000
    0 <= prerequisites.length <= 5000
    prerequisites[i].length == 2
    0 <= ai, bi < numCourses
    All the pairs prerequisites[i] are unique.
"""

import collections
from typing import List

class Solution:

    # ── Attempt · 2026-07-16 ──────────────
    def canFinish_20260716(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # a course can have multiple pre-reqs, so we need an array with number of prereqs
        prereqCounter = [0] * numCourses
        # this is a BFS problem, so we will take what we can with prereqCounter of 0
        # we should move prereq into an adj map, so course -> courses that require course
        adjMap = collections.defaultdict(list)
        # we also need a way to tell us which course have been taken, so like a visited set
        taken = set()

        for course, prereq in prerequisites:
            adjMap[prereq].append(course)
            prereqCounter[course]+=1
        
        # pre-populate with courses we can take now
        queue = collections.deque()

        for i in range(len(prereqCounter)):
            if prereqCounter[i] == 0:
                queue.append(i)
        
        # now that we have courses we can take first, let's take them
        while queue:
            currentCourse = queue.popleft()
            taken.add(currentCourse)
            # now go through each of the courses that require currentCourse
            # decrement reqs by 1 and add them to queue if they are at 0
            for course in adjMap[currentCourse]:
                prereqCounter[course]-=1
                if prereqCounter[course] == 0:
                    queue.append(course)
        
        return len(taken) == numCourses

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # one big thing that prevented us from solving this problem initially was not properly tracking
        # what if a course had multiple pre-reqs. So this means we should keep track of how many prereqs each node has
        # given 0 <= ai, bi < numCourses, we will initialize prereqCounter = [0] * numCourses
        # then do same thing as we did in our initial thought process

        prereqCounter = [0] * numCourses
        neighborMap = collections.defaultdict(list)
        canTake = collections.deque()
        numbersOfCoursesTaken = 0

        for row in prerequisites:
            course = row[0]
            prereq = row[1]
            prereqCounter[course]+=1
            neighborMap[prereq].append(course)

        # so now we add all nodes with 0s in prereqCounter to canTake
        for i in range(len(prereqCounter)):
            if prereqCounter[i] == 0:
                canTake.append(i)
        
        # now we do standard BFS
        while canTake:
            currentCourse = canTake.popleft()
            numbersOfCoursesTaken+=1

            # now let's take a look at all the neighbors of currentCourse
            for dependentCourse in neighborMap[currentCourse]:
                # since we already took currentCourse, we decrement prereqCounter[dependentCourse]
                prereqCounter[dependentCourse]-=1
                # if this is now zero, we can take it, so we add it to the queue
                if prereqCounter[dependentCourse] == 0:
                    canTake.append(dependentCourse)
        
        return numbersOfCoursesTaken >= numCourses

    def canFinishVersion1_Incomplete(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # first thought is that we find all nodes that do not have a pre-req
        # so we can look through all the courses that have a req, so that's pre[i][0], we'll put that in a set of classes requiring other courses
        # go through list of pre[i][1] and anything that's not in reqSet means it's a potential starting node
        # so now that we have our starting node, we can do BFS. 
        # so look for all nodes that have starting node as a requirement
        # this means our starting nodes should be part of a queue

        # let's do a map of row[1] -> list[row[0]]
        # put all the courses that need pre-reqs in reqSet

        neighborMap = collections.defaultdict(list)

        reqSet = set()

        for row in prerequisites:
            course = row[0]
            prereq = row[1]
            reqSet.add(course)
            neighborMap[prereq].append(course)

        canTake = collections.deque()

        numOfCoursesTaken = 0

        # now we go through row[1] and get all the nodes that do not need reqs
        for row in prerequisites:
            potentialCourse = row[1]
            if potentialCourse not in reqSet:
                canTake.append(potentialCourse)
        
        # now we go through this like a normal bfs
        # we 'take' these courses by popping them out of the queue

        while canTake:
            courseTaken = canTake.popleft()
            numOfCoursesTaken+=1

            # check if we passed required numCourses yet
            if numOfCoursesTaken >= numCourses:
                return True

            # now we bfs on 'neighbors' of courseTaken
            # basically these are courses that have a pre-req of courseTaken
            # this actually makes me think we need a map of courseTaken -> courses that need courseTaken
            # ok so we have a map of courseTaken -> courses now, so we will loop through that list
            coursesListLen = len(neighborMap[courseTaken])
            for i in range(coursesListLen):
                canTake.append(neighborMap[courseTaken].pop())

        return numOfCoursesTaken >= numCourses
    
    def canFinish_20260612(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # so we need to find all courses we can take immediately, this is the starting queue of our BFS
        # we need to find how many pre-req each course has, this allows us to add to queue of BFS
        # then we also need a map to see which prereq allows which class to be taken, this tells us about the neighbors of the BFS
        # don't think we need to take care of circular since we'd never have a course in queue that is not possible to take

        numberOfCoursesTaken = 0

        hasPrereq = [0] * numCourses

        prereqMap = collections.defaultdict(list)

        for row in prerequisites:
            course = row[0]
            prereq = row[1]
            hasPrereq[course]+=1
            prereqMap[prereq].append(course)

        canTake = collections.deque()

        for i in range(len(hasPrereq)):
            if hasPrereq[i] == 0:
                canTake.append(i)
        
        while canTake:
            currentCourse = canTake.popleft()
            # say we took this course
            numberOfCoursesTaken+=1

            for course in prereqMap[currentCourse]:
                # since we just took current course, we decrement the amount of courses each of its dependency
                hasPrereq[course]-=1
                if hasPrereq[course] == 0:
                    canTake.append(course)
                

        return numberOfCoursesTaken >= numCourses
    
    def canFinish_20260613(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # need to know all courses we can take first
        # aka, the courses that have no prereq
        # we also need to know what each course unlocks
        # so we need a map from prereq -> list[course]
        # we also need a counter for how many prereq a course has

        prereqMap = collections.defaultdict(list)

        prereqCounter = [0] * numCourses

        numberOfCoursesTaken = 0

        for row in prerequisites:
            course = row[0]
            prereq = row[1]
            prereqMap[prereq].append(course)
            prereqCounter[course]+=1

        # get list of courses we can take right now

        canTake = collections.deque()

        for i in range(len(prereqCounter)):
            if prereqCounter[i] == 0:
                canTake.append(i)
        
        while canTake:
            # take this course
            currentCourse = canTake.popleft()
            # increment courses taken
            numberOfCoursesTaken+=1
            
            # check courses that need currentCourse as prereq
            for course in prereqMap[currentCourse]:
                # since we just took current course, we can decrement how many courses are needed to take this course
                prereqCounter[course]-=1
                # if 0, then we can take it, so we add it the queue
                if prereqCounter[course] == 0:
                    canTake.append(course)
        
        return numberOfCoursesTaken >= numCourses

if __name__ == "__main__":
    numCourses = 2
    prerequisite = [[1,0]]

    Solution().canFinish(numCourses, prerequisite)
