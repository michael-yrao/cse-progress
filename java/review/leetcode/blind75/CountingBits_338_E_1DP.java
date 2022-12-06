package review.leetcode.blind75;

public class CountingBits_338_E_1DP
{
    /*
    * https://leetcode.com/problems/counting-bits/
    * */

    /*
    * Problem was worded weirdly
    * This is asking us to create an array of size n+1 where each index is the target number
    * And we want to find the Hamming Weight of each number
    *
    * Thus the solution is quite simple, just do the same thing we did for Number Of 1 Bits but n times
    * However, the question also asks for a O(n) solution
    *
    * */

    /*
    * O(nlogn) solution
    * */

    public int[] countBits(int n)
    {
        int[] bitArray = new int[n+1];
        for(int i=0;i<=n;i++)
        {
            int currentNumber=i;
            while(currentNumber!=0)
            {
                currentNumber=(currentNumber)&(currentNumber-1);
                bitArray[i]++;
            }
        }
        return bitArray;
    }

    /*
    * O(n) solution
    *
    * This solution is only really visible if you draw out the bits of 0 through n
    * From here, we can notice that we are kinda doing repeated work every time we reach a power of 2
    * Therefore, what we can do is just do a dp solution instead and use each power of 2 as an offset to get our value
    *
    * */

    public int[] countBitsEfficient(int n)
    {
        /*
        O(n) solution:
            1. Since we want hamming weight of every value from 0-n, we can see if we can find a pattern
            2. 0 -> 0000 -> 0
               1 -> 0001 -> 1 : dp[1] = 1 + dp[0] = 1 + dp[n-1];
               2 -> 0010 -> 1 : dp[2] = 1 + dp[0] = 1 + dp[n-2];
               3 -> 0011 -> 2 : dp[3] = 1 + dp[2] = 1 + dp[n-2];
               4 -> 0100 -> 1 : dp[4] = 1 + dp[0] = 1 + dp[n-4];
               5 -> 0101 -> 2 : dp[5] = 1 + dp[4] = 1 + dp[n-4];
        */

        int[] result = new int[n+1];

        // Java initializes int array to all 0

        int closestPowerOf2 = 1;

        for(int i=1;i<=n;i++)
        {
            // We want to update cloestPowerOf2 whenever we hit a power of 2
            if(closestPowerOf2*2==i) closestPowerOf2=i;
            result[i] = 1 + result[i - closestPowerOf2];
        }
        return result;
    }

}
