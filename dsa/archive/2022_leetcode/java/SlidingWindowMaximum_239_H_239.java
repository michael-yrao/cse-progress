package review.leetcode.leetcodeExtra;

import java.util.ArrayDeque;
import java.util.Deque;

public class SlidingWindowMaximum_239_H_239
{
    /*
    * https://leetcode.com/problems/sliding-window-maximum/
    * */

    public int[] maxSlidingWindow(int[] nums, int k)
    {
        // We will store index in our deque
        Deque<Integer> monotonicDecreasingDeque = new ArrayDeque<>();

        int[] solution = new int[nums.length-k+1];

        int solutionCounter=0;

        for(int i=0;i<nums.length;i++)
        {
            // Make sure our deque is always in decreasing order
            while(!monotonicDecreasingDeque.isEmpty() && nums[i] > nums[monotonicDecreasingDeque.peekLast()]) monotonicDecreasingDeque.pollLast();

            monotonicDecreasingDeque.offer(i);

            // Check window size versus left index to make sure we are always in window size
            while(!monotonicDecreasingDeque.isEmpty() && i - k + 1 > monotonicDecreasingDeque.peekFirst())
            {
                monotonicDecreasingDeque.pollFirst();
            }

            if(i+1 >= k) solution[solutionCounter++] = nums[monotonicDecreasingDeque.peekFirst()];
        }
        return solution;
    }
}
