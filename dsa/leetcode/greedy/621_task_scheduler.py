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