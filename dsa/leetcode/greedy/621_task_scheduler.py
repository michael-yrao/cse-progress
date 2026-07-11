"""
You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of at least n intervals between two tasks with the same label.

Return the minimum number of CPU intervals required to complete all tasks.

Example 1:

Input: tasks = ["A","A","A","B","B","B"], n = 2

Output: 8

Explanation: A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.

After completing task A, you must wait two intervals before doing A again. The same applies to task B. In the 3rd interval, neither A nor B can be done, so you idle. By the 4th interval, you can do A again as 2 intervals have passed.

Example 2:

Input: tasks = ["A","C","A","B","D","B"], n = 1

Output: 6

Explanation: A possible sequence is: A -> B -> C -> D -> A -> B.

With a cooling interval of 1, you can repeat a task after just one other task.

Example 3:

Input: tasks = ["A","A","A", "B","B","B"], n = 3

Output: 10

Explanation: A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B.

There are only two types of tasks, A and B, which need to be separated by 3 intervals. This leads to idling twice between repetitions of these tasks.

Constraints:

    1 <= tasks.length <= 104
    tasks[i] is an uppercase English letter.
    0 <= n <= 100
"""
from collections import Counter
import collections
import heapq
from typing import List

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # minimizing number of intervals needed
        # try a greedy approach but what does that mean in this context
        # A, A, A, A, B; n = 2. The bottleneck here is clearly that there are too many As
        # so we tackle the most frequent one first, so that's our greedy criteria
        # that also puts out frequency map
        # for us to get the most frequent, we use a max heap
        # looking at example 1, we see that A -> B -> idle -> A ; n = 2
        # there are n + 1 unique tasks before we can repeat A again
        # so we pop n + 1 elements off the heap to try to do them
        # if any are left with value still, we put it back on the heap

        freqMap = Counter(tasks)
        maxHeap = []
        result = 0

        for key, value in freqMap.items():
            heapq.heappush(maxHeap,(-value, key))
        
        # while there are still tasks to do
        while maxHeap:
            # we pop n + 1 values off the maxHeap to do
            tasksLeftOver = set()
            for _ in range(n+1):
                # if there are still tasks left to do
                # and if current value is not already in task
                # then we do the task
                if maxHeap:
                    currentTaskCounter, currentTask = heapq.heappop(maxHeap)
                    # we add since max heap is negated
                    currentTaskCounter+=1
                    # we did a task, increment result
                    result+=1
                    # if it is in task, we do an idle, so we increment result and just add to tasksLeftOver
                    # now that we tried to do this task, let's add to the leftover tasks queue
                    if currentTaskCounter < 0:
                        tasksLeftOver.add((currentTaskCounter, currentTask))
                else:
                # no actions possible, but if we finished all tasks, we can just exit
                    if not tasksLeftOver:
                        return result
                # no actions possible, just increment result
                    result+=1
            # add left over tasks back in
            for _ in range(len(tasksLeftOver)):
                heapq.heappush(maxHeap, tasksLeftOver.pop())
        return result
    # O(maxHeap * k) solution
    def leastInterval_20260701(self, tasks: List[str], n: int) -> int:
        # from the problem, we know that between two tasks of the same type
        # they must have n space in between, so there must be n + 1 tasks done in total
        # before the next of the same task can run again
        # we also know the most frequent task is a bottleneck, so we should prioritize that
        # so frequency map and max heap

        freqMap = Counter(tasks)
        interval = 0
        distinctTasks = n + 1
        maxHeap = []

        for key,value in freqMap.items():
            heapq.heappush(maxHeap,(-value,key)) # type: ignore

        # while there are still tasks to be done
        while maxHeap:
            # take out distinctTasks for us to do
            # after we finish doing these tasks, we do also need to put them back into the heap if they are not at 0
            taskSet = set()
            for i in range(distinctTasks):
                # if heap is empty and taskSet is empty, we are done and don't need to continue
                if not maxHeap and not taskSet:
                    return interval
                # if we can't do any tasks
                if maxHeap:
                    # do the task
                    currentTaskCounter, currentTask = heapq.heappop(maxHeap)
                    currentTaskCounter+=1
                # increment cpu time for the task and also increment if we had to idle
                interval+=1
                # for any tasks left over, add to set
                if currentTaskCounter != 0:
                    taskSet.add((currentTaskCounter, currentTask))
            # add taskSet back to heap
            for task in taskSet:
                heapq.heappush(maxHeap, task)
        
        return interval
    # O(n) solution
    def leastInterval_20260701_v2(self, tasks: List[str], n: int) -> int:
        # from the problem, we know that between two tasks of the same type
        # they must have n space in between, so there must be n + 1 tasks done in total
        # before the next of the same task can run again
        # we also know the most frequent task is a bottleneck, so we should prioritize that
        # so frequency map and max heap

        freqMap = Counter(tasks)
        interval = 0
        maxDistinctTasks = n + 1
        maxHeap = []

        for key,value in freqMap.items():
            heapq.heappush(maxHeap,(-value,key)) # type: ignore

        # while there are still tasks to be done
        while maxHeap:
            # check if we have distinct tasks to do, if not, just do however many tasks are available in maxHeap
            todoTasks = min(len(maxHeap),maxDistinctTasks)
            # after we finish doing these tasks, we do also need to put them back into the heap if they are not at 0
            taskSet = set()
            for _ in range(todoTasks):
                # with this method, we know there are tasks to do here
                # and don't have to consider idles here
                currentTaskCounter, currentTask = heapq.heappop(maxHeap)
                currentTaskCounter+=1
                # for any tasks left over, add to set
                if currentTaskCounter != 0:
                    taskSet.add((currentTaskCounter, currentTask))
            # add taskSet back to heap
            for task in taskSet:
                heapq.heappush(maxHeap, task)
            # if there are tasks left, that means we needed to use the full maxDistinctTasks
            if maxHeap:
                interval+=maxDistinctTasks
            else:
            # otherwise, we only needed to do todoTasks
                interval+=todoTasks
        
        return interval
    def leastInterval_20260710(self, tasks: List[str], n: int) -> int:
        # we know from common sense that if we can't repeat
        # the most frequent element will be the blocker
        # so we will try to do that one as priority
        # so we need frequency map
        # since we want to prioritize highest frequency, we should use a heap
        # knowing we do highest freq one first, the earliest we do it next is:
        # A . . A ; n = 2
        # 1 2 3 4 ; i + n + 1
        # so we are doing n + 1 tasks before the next time we see it again
        # we also need to decrement the value each time after we do them
        # if it hits 0, we remove it completely, otherwise add it back in heap
        
        freqMap = Counter(tasks)
        maxHeap = []

        for key, value in freqMap.items():
            heapq.heappush(maxHeap,(-value, key))
        
        interval = 0
        maxTaskToDo = n + 1

        # while there are tasks to do
        while maxHeap:
            sizeOfHeap = len(maxHeap)
            tasksToQueue = min(maxTaskToDo,sizeOfHeap)
            tasksToAddBack = set()
            for _ in range(tasksToQueue):
                currentCounter, currentTask = heapq.heappop(maxHeap)
                # do the task ; adding since we are negated here
                currentCounter+=1
                if currentCounter < 0:
                    tasksToAddBack.add((currentCounter,currentTask))
            # if any tasks remaining
            for currentCounter, currentTask in tasksToAddBack:
                heapq.heappush(maxHeap,(currentCounter, currentTask))
            # if we still have tasks to do, it means we needed the full n + 1 time
            if len(maxHeap) > 0:
                interval+=maxTaskToDo
            # if no more tasks, then we take tasksToQueue
            else:
                interval+=tasksToQueue
        return interval