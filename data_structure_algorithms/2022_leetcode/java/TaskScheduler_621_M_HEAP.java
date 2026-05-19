package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.*;

public class TaskScheduler_621_M_HEAP
{
    /*
    * https://leetcode.com/problems/task-scheduler/
    * */

    /*
    * n = length of intervals we need to wait for between same tasks
    *
    * So it doesn't seem like the ordering in the array given to us actually matters
    * So what I would want to do is put these into a Frequency Map
    *
    * What we should also note is that we should go for the task with the biggest frequency first
    * This way we can minimize the idle time. This means we can use something like a Max Heap
    *
    * We do also need to keep track of the idle time so we can queue up the task when it is off cooldown
    * */

    public int leastInterval(char[] tasks, int n)
    {
        Map<Character, Integer> freqMap = new HashMap<>();
        for(char x : tasks)
        {
            freqMap.put(x, freqMap.getOrDefault(x,0)+1);
        }

        PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a,b) -> b-a);

        for(Map.Entry<Character, Integer> entry : freqMap.entrySet())
        {
            maxHeap.offer(entry.getValue());
        }

        // Will use this to increment time
        int currentTime=0;

        // Pair will consist of frequency of task and when this task will be available again to execute

        Queue<Pair<Integer, Integer>> queue = new LinkedList<>();

        while(!maxHeap.isEmpty() || !queue.isEmpty())
        {
            // Increment time
            currentTime++;
            // Perform current task. We will perform task with the largest frequency
            if(!maxHeap.isEmpty())
            {
                int remainingTask = maxHeap.poll() - 1;

                // Now that we have performed the task, let's check to see if this task needs to be performed again
                if(remainingTask>0)
                {
                    queue.add(new Pair<>(remainingTask,currentTime+n));
                }
            }
            if(!queue.isEmpty() && queue.peek().y == currentTime)
            {
                maxHeap.offer(queue.poll().x);
            }
        }
        return currentTime;
    }
}
