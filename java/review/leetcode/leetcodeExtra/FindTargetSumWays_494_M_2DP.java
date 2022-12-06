package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.HashMap;
import java.util.Map;

public class FindTargetSumWays_494_M_2DP
{
    /*
    * https://leetcode.com/problems/target-sum/
    * */

    /*
    * First thought was I could use a decision tree for this
    * Basically each number in nums can be positive or negative, so we just do something like backtracking
    * and return number of ways we can get to target. Complexity of that is 2^(nums.length), let's see if we can do better
    * */

    public int findTargetSumWays(int[] nums, int target)
    {
        Map<Pair<Integer,Integer>, Integer> cache = new HashMap<>();
        return backtrack(nums,target,0,0,cache);
    }

    public int backtrack(int[] nums, int target, int index, int currentTotal, Map<Pair<Integer,Integer>, Integer> cache)
    {
        // Base case
        // Once we reach end of the array, if current total = target, then we found one permutation
        // Thus we return 1, but if not we return 0
        if(index==nums.length) return (target==currentTotal)?1:0;

        // Dynamic Programming portion
        // Check to see if we have already calculated this exact scenario before
        // If we have, just return it
        Pair<Integer,Integer> pair = new Pair<>(index,currentTotal);

        if (cache.containsKey(pair)) return cache.get(pair);

        // Decision tree

        cache.put(pair, backtrack(nums,target,index+1,currentTotal + nums[index], cache)
                        + backtrack(nums,target,index+1,currentTotal - nums[index], cache));

        return cache.get(pair);
    }
}
