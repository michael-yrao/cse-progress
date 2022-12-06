package review.leetcode.leetcodeExtra;

import java.util.HashMap;
import java.util.Map;

public class MaximumSizeSubarraySumEqualsK_325_M_PREFIXSUM
{
    /*
    * This problem is Premium:
    * https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/
    *
    * You can find the same problem on LintCode:
    * https://www.lintcode.com/problem/911/
    * */

    /*
    * This problem seems very similar to Subarray Sum Equals K
    * But instead of frequency, we instead want the max length instead
    * So what we should do is create a prefix sum hashmap where key = prefixsum and value = leading index of this sum
    * This way, once we find the sum, we can do i + 1 to get the true length of the subarray that gave us this sum
    * We can also do the same type of check we did in Subarray Sum Equals K and do map.get(runningSum - k) to see if we have better ones available
    * We also should keep track of the max subarray
    * */

    public int maxSubArrayLen(int[] nums, int k)
    {
        // Keeps track of max size of subarray
        int maxSize = 0;

        // Prefix Sum map
        Map<Integer,Integer> map = new HashMap<>();

        // Prefix Sum
        int runningSum=0;

        for(int i=0;i<nums.length;i++)
        {
            runningSum+=nums[i];

            // If running sum == k, that means there is a subarray starting from index 0 to i that gives k
            // Thus update max to i+1 if it's bigger than current max
            if(runningSum==k) maxSize = Math.max(maxSize,i + 1);

            // Let x = (runningSum - k)
            // x + k = runningSum
            // k = runningSum - x
            // Thus if x exists in our map, then we are able to remove x to get to k
            // So we do i - map.get(runningSum-k) to get size of that subarray
            if(map.containsKey(runningSum-k)) maxSize = Math.max(maxSize, i - map.get(runningSum-k));

            // If map doesn't contain this sum already, we will add it to the map
            map.putIfAbsent(runningSum,i);
        }
        return maxSize;
    }

}
