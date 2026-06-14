package review.leetcode.leetcodeExtra;

import java.util.HashMap;
import java.util.Map;

public class SubarraySumEqualsK_560_M_PREFIXSUM
{
    /*
    * https://leetcode.com/problems/subarray-sum-equals-k/
    * */

    /*
    * Prefix sum problem
    *
    * We want to use a hashmap for the prefix sum since we are counting number of continuous subarrays that add up to k
    * As such, we will use SUM as the key and use the FREQ as the value so we know exactly how often the SUM appears in our array
    *
    * 1. Create SUM -> FREQ hashmap
    * 2. Iterate through the array and put contiguous sum and freq into hashmap
    * 3. We should also note that if currentSum is bigger than k by (currentSum - k),
    *    that means we can also get sum by removing the elements that add up to the currentSum
    *    so we should check to see if map.get(currentSum - k) exists and add it to our counter
    *
    * */

    public int subarraySum(int[] nums, int k)
    {
        int count=0;
        int currentSum=0;
        Map<Integer,Integer> prefix = new HashMap<>();
        // Go through the array and populate prefix sum as usual
        for(Integer n : nums)
        {
            currentSum+=n;
            // Check if current sum exist in our table already
            // If it does exist, increment our count
            if(currentSum==k) count++;
            // Check if currentSum-k exist in our hashmap already
            // If it does, that means we have prefix.get(currentSum-k) ways to get to k
            count+=prefix.getOrDefault(currentSum-k,0);
            // Add prefix sum to hashmap with 1 additional frequency
            prefix.put(currentSum, 1 + prefix.getOrDefault(currentSum,0));
        }
        return count;
    }
}
