package review.leetcode.blind75;

import java.util.HashMap;
import java.util.Map;

public class ClimbStairs_70_E_1DP
{
    /*
    * https://leetcode.com/problems/climbing-stairs/
    * */

    public int climbStairs(int n)
    {
        // Climbing Stairs is kind of deceiving, it is kind of similar to Fibonacci in many ways
        // Knowing there are 0 or 1 steps, there are exactly 1 way to reach the top
        // Otherwise we want to take 1 or 2 step, so we do n - 1 and n - 2 at each round
        if(n==0||n==1) return 1;
        return climbStairs(n-2)+climbStairs(n-1);
    }

    public int climbStairsTabulation(int n)
    {
        int[] nSizeArray = new int[n+1];
        nSizeArray[0]=1;
        nSizeArray[1]=1;
        for(int i=2;i<=n;i++)
        {
            nSizeArray[i]=nSizeArray[i-2]+nSizeArray[i-1];
        }
        return nSizeArray[n];
    }

    public int climbStairsMemoization(int n)
    {
        Map<Integer,Integer> memo = new HashMap<>();
        memo.putIfAbsent(0,1);
        memo.putIfAbsent(1,1);
        return climbStairsMemoizationHelper(n,memo);
    }

    public int climbStairsMemoizationHelper(int n, Map<Integer, Integer> memo)
    {
        if(memo.containsKey(n)) return memo.get(n);
        if(n==0||n==1) return 1;
        memo.putIfAbsent(n,climbStairsMemoizationHelper(n-2,memo)+climbStairsMemoizationHelper(n-1,memo));
        return memo.get(n);
    }

}
