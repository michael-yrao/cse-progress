package review.leetcode.leetcodeExtra;

import java.util.Arrays;

public class GasStation_134_M_GREEDY
{
    /*
    * https://leetcode.com/problems/gas-station/
    *
    * Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
    * Output: 3
    *
    * */

    public int canCompleteCircuit(int[] gas, int[] cost)
    {
        /*
            gas[i] is gas we get when we get to i
            cost[i] is cost to get to next index

            Since we need to travel a full cycle, if total of gas < total of cost, we would never be able to complete it

            Obvious point is we can never go below negative net, e.g. gas-cost >= 0 must always be true
            If not, we need to move our starting point

            1. Go through list
            2. Keep a potential starting point
            3. Keep track of our total gas at each step
            4. If total gas ever goes below 0, update our starting point, also reset total gas since we are now starting over
        */

        if(Arrays.stream(gas).sum() < Arrays.stream(cost).sum()) return -1;

        int startingPoint=0;
        int totalGas=0;

        for(int i=0;i<gas.length;i++)
        {
            totalGas = totalGas + gas[i] - cost[i];
            if(totalGas < 0)
            {
                totalGas = 0;
                startingPoint=i+1;
            }
        }
        return startingPoint;
    }

}
