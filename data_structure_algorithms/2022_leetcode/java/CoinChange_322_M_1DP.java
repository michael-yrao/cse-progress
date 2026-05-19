package review.leetcode.blind75;

import java.util.Arrays;

public class CoinChange_322_M_1DP
{
    /*
    * https://leetcode.com/problems/coin-change/
    * */

    /*

        First thing we should note here is that we should work backwards
        so we should start with amount, then form a decision tree on how to use the coins

        This means we are dealing with a DP problem, so we will use tabulation to solve this problem

        Let's start with the absolutes:

            1. We will have table of size amount+1, so 0th index will be 0 amount, 1st index will be 1 amount, etc
            2. Default all of the indices to be not reachable, e.g. larger than amount number of coins
            3. table[0] = 0 by default since no coin is needed to make up table[0]
            4. We can then assume all coins will be initialized as 1

    */

    public int coinChange(int[] coins, int amount)
    {
        if(amount <= 0 || coins == null || coins.length == 0) return 0;

        int[] table = new int[amount+1];

        // We will work backwards
        // e.g. assume the indices are not reachable

        // Default to an amount that is considered as "unreachable"
        // Normally I would put Integer.MAX_VALUE, but we might do +1 on it causing it overflow

        Arrays.fill(table,amount+1);

        // First index is by default 0 since we can always reach it with 0 coins

        table[0] = 0;

        // Otherwise, let's try to see if we can actually reach

        for(int i=1;i<table.length;i++)
        {
            // We need a second loop here so we can test to see if each coin can actually reach this index
            for(Integer coin : coins)
            {
                // Best case scenario, we have a coin equal to index, we need only 1 coin
                if(coin==i) table[i] = 1;
                // If coin > i, we can ignore it since it there is no way to make up i with coin
                if(coin<i)
                {
                    // table[i-coin] is checking whether or not that index is reachable
                    // If it was reachable, we could simply add 1 to it to get to our current index
                    // Otherwise, we would just have our default unreachable value
                    table[i] = Math.min(table[i-coin]+1,table[i]);
                }
            }
        }
        if(table[amount]==amount+1) return -1;
        return table[amount];
    }
}
