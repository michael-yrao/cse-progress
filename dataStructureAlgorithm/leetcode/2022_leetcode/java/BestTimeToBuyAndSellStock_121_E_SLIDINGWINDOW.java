package review.leetcode.blind75;

public class BestTimeToBuyAndSellStock_121_E_SLIDINGWINDOW
{
    /*
    * https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
    * */

        /*
        We want 2 pointers where we have a buy day and a sell day and we want to maximize prices[sell] - prices[buy]
        So seems like a 2 pointers/sliding window problem.
        1. Declare 2 pointers, left and right, we will start them at 0 and 1 respectively
        2. Since we want the max profit, let's keep a variable to keep track of that
        2. If prices[right] < prices[left], set right=left
        3. increment right and do max(max,right-left) at each iteration
        */

    public int maxProfit(int[] prices)
    {
        int left=0,right=1;
        int max=Integer.MIN_VALUE;

        while(right<prices.length)
        {
            max=Math.max(max,prices[right]-prices[left]);
            if(prices[right]<prices[left]) left=right;
            right++;
        }
        return Math.max(max, 0);
    }
}
