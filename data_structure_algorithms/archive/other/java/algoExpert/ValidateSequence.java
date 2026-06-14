package review.algoExpert;

import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class ValidateSequence
{
    /*
    * https://www.algoexpert.io/questions/validate-subsequence
    * */

    public boolean isValidSubsequence(List<Integer> array, List<Integer> sequence)
    {
        // Write your code here.
        // Since it doesn't matter if it's adjacent, we can solve this by using a Queue
        // Put sequence into a Queue
        // Loop through array and check equality against queue.peek()
        // If found, queue.poll(), return whether or not queue.isEmpty()

        Queue<Integer> queue = new LinkedList<>();

        for(Integer x : sequence) queue.offer(x);

        for(Integer x : array)
            if(x==queue.peek()) queue.poll();

        return queue.isEmpty();
    }

}
