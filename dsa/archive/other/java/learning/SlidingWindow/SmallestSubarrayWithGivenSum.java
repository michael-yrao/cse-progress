package review.learning.SlidingWindow;

public class SmallestSubarrayWithGivenSum
{
    /*
    * Given an integer array, find the smallest subarray size summing up to or greater than target, ideally as close to target as possible
    * */

    public int smallestSubarrayWithGivenSum(int[] numbers, int target)
    {
        int leftWindow=0;
        int rightWindow=0;

        int runningSum=0;
        int minCounter=Integer.MAX_VALUE;

        while(rightWindow<numbers.length)
        {
            runningSum+=numbers[rightWindow];
            while(runningSum>=target)
            {
                minCounter=Math.min(minCounter,rightWindow-leftWindow+1);
                runningSum-=numbers[leftWindow];
                leftWindow++;
            }
            rightWindow++;
        }
        return minCounter;
    }
}
