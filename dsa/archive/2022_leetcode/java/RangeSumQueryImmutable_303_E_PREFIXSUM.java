package review.leetcode.leetcodeExtra;

public class RangeSumQueryImmutable_303_E_PREFIXSUM
{
    /*
    * https://leetcode.com/problems/range-sum-query-immutable/
    * */


    // The O(n) solution to this is pretty trivial
    // Thus let's think of something a bit more clever
    // The nums will never be modified, so we don't really have to store it
    // We can maybe use prefix sum
    // e.g. given nums: [-2, 0, 3, -5, 2, -1]
    // We would want to populate prefix sum, e.g. populate the index with sum of values before it
    // initialize prefixSum[0] to nums[0]
    // Loop through nums starting from index 1, and we can do something like:
    // prefixSum[i] = prefixSum[i-1] + nums[i]
    // n: [-2, 0, 3, -5, 2, -1]
    // p: [-2,-2, 1, -4,-2, -3]

    int[] prefixSum;

    public RangeSumQueryImmutable_303_E_PREFIXSUM(int[] nums)
    {
        prefixSum = new int[nums.length];
        prefixSum[0] = nums[0];
        for(int i=1;i<nums.length;i++)
        {
            prefixSum[i] = prefixSum[i-1] + nums[i];
        }
    }

    // Since we stored our values as sums
    // We can simplify our addition logic
    public int sumRange(int left, int right)
    {
        // If left = 0, that means we are just fetching our prefix sum values
        if(left==0 && right>=0 && right <= prefixSum.length) return prefixSum[right];

        // If left != 0, that means we just have to remove prefix[left] from prefix[right] to get the in-between
        // Remember to do left - 1 since we are doing inclusive

        return prefixSum[right] - prefixSum[left-1];
    }
}
