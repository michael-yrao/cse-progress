package review.leetcode.blind75;

import java.util.ArrayList;
import java.util.List;

public class CoinChangeII_518_M_2DP
{
    /*
    * https://leetcode.com/problems/coin-change-2/
    * */


    /*
     * Instead of best way to get to amount, we want number of ways to get to amount
     * This is an Unbounded Knapsack question
     * */

    public int change(int amount, int[] coins)
    {
        int[] tabulation = new int[amount+1];
        tabulation[0] = 1; // by default, there is 1 way to make up 0 coins

        // Loop through each coin

        for(int i=0;i<coins.length;i++)
        {
            // We know it's not possible to solve anything if current index is less than coins[i]
            // Therefore, we just start at coins[i] and use same strategy as coin change I

            for(int j=coins[i];j<=amount;j++)
            {
                tabulation[j] += tabulation[j-coins[i]];
            }
        }
        return tabulation[amount];
    }

    /*
     * We can do the exact same thing as we did for Combination Sum
     * We will just return number of values instead of the List of Lists
     * But this solution is not accepted on Leetcode since it's too slow
     * */

    List<List<Integer>> resultList = new ArrayList<>();

    public int changeBacktrackingMethod(int amount, int[] coins)
    {
        List<Integer> result = new ArrayList<>();
        changeBacktrackingMethodDFS(0,amount,coins,result);
        return resultList.size();
    }

    private void changeBacktrackingMethodDFS(int index, int amount, int[] coins, List<Integer> result)
    {
        if(index==coins.length)
        {
            if(amount==0) resultList.add(new ArrayList<>(result));
            return;
        }
        if(amount<0) return;
        if(coins[index]<=amount)
        {
            result.add(coins[index]);
            changeBacktrackingMethodDFS(index,amount-coins[index],coins,result);
            result.remove(result.size()-1);
        }
        // If we can't use this coin, we just run DFS with the next value
        changeBacktrackingMethodDFS(index+1,amount,coins,result);
    }
}
