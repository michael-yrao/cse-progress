package review.leetcode.blind75;

public class MaximumProductSubarray_152_M_1DP
{
    /*
    * https://leetcode.com/problems/maximum-product-subarray/
    * */

    public int maxProduct(int[] nums)
    {
        /*
        * Since we have both positive and negative
        * We should keep track of a max and a min
        * If min is negative, it will become much bigger when given another negative value
        *
        * With the above information, we can try a variation of Kadane's Algorithm
        * e.g. Keep track of Max and Min ending in current index
        *
        * */

        if(nums==null || nums.length==0) return 0;

        int max = nums[0]; // return value

        // Utilizing Kadane's Algorithm, we will have 2 variables
        // 1 keep track of current max ending in index i
        // 1 keep track of current min ending in index i

        int currentMax = nums[0];
        int currentMin = nums[0];

        for(Integer x : nums)
        {
            // Both these variables can end up being potential min if values are opposite signs
            // Therefore, we should do a Math.max and Math.min on them when we update the currentMax and currentMin
            int potentialMax = x * currentMax;
            int potentialMin = x * currentMin;

            // We also compare to x in the case that the number by itself is larger than both

            currentMax = Math.max(x, Math.max(potentialMax,potentialMin));
            currentMin = Math.min(x, Math.min(potentialMax,potentialMin));

            // Update our return value

            max = Math.max(currentMax,max);
        }
        return max;
    }
}
