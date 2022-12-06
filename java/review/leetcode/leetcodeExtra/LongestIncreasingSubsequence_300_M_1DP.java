package review.leetcode.leetcodeExtra;

import java.util.Arrays;
import java.util.Collections;

public class LongestIncreasingSubsequence_300_M_1DP
{
    /*
    * https://leetcode.com/problems/longest-increasing-subsequence/
    * */

    public int lengthOfLIS(int[] nums)
    {
        /*

        Immediate glance, there is really no pattern here other than the result is in increasing order
        We can't sort since that kinda defeats the whole purpose of this problem
        Don't think we can use monotonic since idea of monotonic is to visit each vertex once and only once

        We will backtrack it instead...

        We can actually DP this starting from the back
        * */

        int[] table = new int[nums.length];
        Arrays.fill(table,1);

        for(int i=table.length-1;i>=0;i++)
        {
            for(int j=i+1;j<table.length;j++)
            {
                if(nums[i] < nums[j])
                    table[i] = Math.max(nums[i], 1 + nums[j]);
            }
        }

        int max=Integer.MIN_VALUE;

        for(Integer x : table) max=Math.max(x,max);

        return max;
    }
}
