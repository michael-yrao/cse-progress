package review.leetcode.leetcodeExtra;

public class FindTheHighestAltitude_1732_E_PREFIXSUM
{
    /*
    * https://leetcode.com/problems/find-the-highest-altitude/
    * */

    /*
    * This is probably the most literal problem for prefix sum
    *   1. Create array of size gain + 1
    *   2. Set arr[0] to 0
    *   3. from i=0 to gain length, set arr[i+1] = gain[i] + arr[i]
    *
    *   index:   0  1 2 3  4
    *   gain = [-5, 1,5,0,-7]
    * arr = [0, -5,-4,1,1,-6]
    *
    * */

    public int largestAltitude(int[] gain)
    {
        int[] prefixSum = new int[gain.length+1];
        for(int i=0;i<gain.length;i++)
        {
            prefixSum[i+1] = gain[i] + prefixSum[i];
        }
        int maxValue = Integer.MIN_VALUE;
        for(Integer x : prefixSum) maxValue = Math.max(x,maxValue);
        return maxValue;
    }
}
