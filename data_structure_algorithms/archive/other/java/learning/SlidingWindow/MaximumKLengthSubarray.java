package review.learning.SlidingWindow;

public class MaximumKLengthSubarray
{
    /*
    * Given input array, find the max sum with fixed size of k
    * */

    public int maximumKSizedSubarray(int[] numbers, int k)
    {
        int max = Integer.MIN_VALUE;
        int runningSum = 0;

        for(int i=0;i<numbers.length;i++)
        {
            runningSum+=numbers[i];
            // Below is the sliding window portion
            // If we are at the size of the window, we need to remove the earliest value in the sum
            if(i>=k-1)
            {
                max=Math.max(max,runningSum);
                runningSum-=numbers[i-k+1];
            }
        }
        return max;
    }
}
