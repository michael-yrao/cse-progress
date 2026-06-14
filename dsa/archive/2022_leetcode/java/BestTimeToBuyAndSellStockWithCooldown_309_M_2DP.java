package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.HashMap;
import java.util.Map;

public class BestTimeToBuyAndSellStockWithCooldown_309_M_2DP
{
    /*
    * https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
    * */

    /*
    *
    * Solution will use a Dynamic Programming method called Caching, which utilizes HashMap
    *
    * Visualize this problem by drawing out the decision tree
    *   1. Have the vertices as the current profit amount
    *   2. Have the edges be the decision + amount to add/subtract from profit
    *
    * After visualization, we can see that we need to do a DFS. Since vertices is profit, we will have return as int for profit
    *
    * We can also note the below:
    * Options at each step: Buy/Sell/Cooldown
    *   1. We must keep track of current index's state (Buy/Sell).
    *       a. Note that Cooldown is not really a State as it does not affect our profit and only affect index incrementation,
    *          thus we can skip adding Cooldown as a State
    *   2. If Sell, Move index by 2, e.g. i+2 since we must do cooldown and makes next index useless for profit calculation
    *   3. If Buy, Move index by 1, e.g. i+1 as we are not constrained to must cooldown
    *
    * */

    public int maxProfit(int[] prices)
    {
        Map<Pair<Integer, Boolean>, Integer> profitMap = new HashMap<>();

        // Always buy at first index
        return decisionTreeDFS(prices,profitMap,0,true);

    }

    /*
    *
    * Our DFS function will help us determine the maximum profit
    *
    * */

    public int decisionTreeDFS(int[] prices, Map<Pair<Integer, Boolean>, Integer> profitMap, Integer index, Boolean buying)
    {
        // Base case if we traverse out of bound, just return 0
        if(index < 0 || index >= prices.length) return 0;

        // Second base case for Dynamic Programming. If already calculated, just return it

        Pair<Integer,Boolean> pair = new Pair<>(index,buying);
        if(profitMap.containsKey(pair)) return profitMap.get(pair);

        // buying: true = buy, false = sell

        // Default option is Cooldown since we can always do cooldown
        // e.g. Skip current index, keep current Buying/Selling boolean and decide on next iteration

        int cooldown = decisionTreeDFS(prices,profitMap,index+1,buying);

        // Now we see whether or not we are Buying Or Sell

        int buyOrSell;

        // If we are buying, then we must subtract the price at current index, then DFS on next index for Sell decision
        // We DFS for Sell decision since we have already accounted for cooldown decision above and we cannot buy as we just bought

        if(buying) buyOrSell = decisionTreeDFS(prices,profitMap,index+1,false) - prices[index];

        // If we are selling, then we must add the price at current index, skip an index since it is mandatory to skip after Sell
        // Then call DFS for Buy decision since we no longer have a stock

        else buyOrSell = decisionTreeDFS(prices,profitMap,index+2,true) + prices[index];

        // Put the decision into our Cache

        profitMap.put(pair,Math.max(buyOrSell,cooldown));

        // Return the profit for this decision

        return profitMap.get(pair);
    }
}
