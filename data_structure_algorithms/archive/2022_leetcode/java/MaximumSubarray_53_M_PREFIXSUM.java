package review.leetcode.blind75;

public class MaximumSubarray_53_M_PREFIXSUM
{
    /*
    * https://leetcode.com/problems/maximum-subarray/
    * */

    // This solution variation is like a bootleg Sliding Window

    public int maxSubArray(int[] nums)
    {
        // Keep a running sum
        // Keep a largest sum
        // Reset running sum whenever it hits below 0

        int largestSum = Integer.MIN_VALUE;
        int runningSum = 0;

        for(int i=0;i<nums.length;i++)
        {
            runningSum+=nums[i];
            largestSum=Math.max(largestSum,runningSum); // This must be in front of the replace since total can be negative
            runningSum=Math.max(runningSum,0);          // If current sum is less than 0, discard it
        }
        return largestSum;
    }


    // Kadane's Algorithm
    // This Algorithm is a combination of Prefix Sum and Dynamic Programming
    // Instead of storing all prefix sums in an array, this just keeps the largest prefix sum value in a single variable

    public int maxSubArrayKadane(int[] nums)
    {
        int max = nums[0];
        int currentSum = nums[0];

        for(int i=1;i<nums.length;i++)
        {
            currentSum = Math.max(nums[i], currentSum+nums[i]);
            max = Math.max(max,currentSum);
        }
        return max;
    }

}
