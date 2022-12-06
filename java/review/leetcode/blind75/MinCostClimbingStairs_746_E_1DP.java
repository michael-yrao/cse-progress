package review.leetcode.blind75;

public class MinCostClimbingStairs_746_E_1DP
{
    /*
    * https://leetcode.com/problems/min-cost-climbing-stairs/
    *
    * Can start at index 0 or index 1
    * */

    public int minCostClimbingStairs(int[] cost)
    {
        if(cost.length==1) return cost[0];

        if(cost.length==2) return Math.min(cost[0], cost[1]);

        int[] table = new int[cost.length+1];


        // Question is weirdly worded, it seems that we want to step to the step of cost.length + 1
        // Thus table[0] will be 1 step, while table[cost.length] will be cost.length + 1 step

        table[0] = 0;                           // Technically no cost since we can start at step 1
        table[1] = 0;                           // Similarly, we can also start at step 2, so this would also be no cost
        table[2] = Math.min(cost[0],cost[1]);   // First step we really have to take, we can do min of 1, 2
        // table[3] = Math.min(table[1] + cost[1], table[2] + cost[2]); <- Formula: Math.min(table[i-2]+cost[i-2],table[i-1]+cost[i-1])

        for(int i=2;i<table.length;i++)
        {
            table[i] = Math.min(table[i-1] + cost[i-1],table[i-2]+cost[i-2]);
        }
        return table[cost.length];
    }
}
