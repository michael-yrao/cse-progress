package review.leetcode.blind75;

public class HouseRobberII_213_M_1DP
{
    /*
    * https://leetcode.com/problems/house-robber-ii/
    * */

    public int robSecondSubmission(int[] nums)
    {
        /*
        We can think of this problem like a bootleg decision tree:
            1. Pick first house
            2. Pick last house

        Compare and return the max of the two

        1. Make 2 tabulation tables
        2. One with first house as always pick
        3. One with last house as always pick
        4. Fill both with some type of logic..


        firstHouse[0] = nums[0]

        firstHouse[1] = Math.max(firstHouse[0],nums[1])
        firstHouse[2] = Math.max(firstHouse[1],firstHouse[0] + nums[2])

        lastHouse[0] = 0

        Same formula as first House Robber

        dp[n] = Math.max(dp[n-1],dp[n-2] + nums[n])

        */


        if(nums==null || nums.length==0) return 0;
        if(nums.length==1) return nums[0];
        if(nums.length==2) return Math.max(nums[0],nums[1]);


        int[] skipFirst = new int[nums.length];
        int[] skipLast = new int[nums.length];

        skipFirst[0] = 0;
        skipFirst[1] = nums[1];

        skipLast[0] = nums[0];
        skipLast[1] = nums[0];
        //skipLast[1] = Math.max(nums[1],skipLast[0]); <- Since we are not skipping first house, we can't pick second house

        for(int i=2;i<nums.length;i++)
        {
            skipFirst[i] = Math.max(skipFirst[i-1],skipFirst[i-2] + nums[i]);
        }

        // We only go to 2nd to last value since we need to skip last index
        for(int i=2;i<nums.length-1;i++)
        {
            skipLast[i] = Math.max(skipLast[i-1],skipLast[i-2] + nums[i]);
        }
        skipLast[nums.length-1] = skipLast[nums.length-2];

        return Math.max(skipFirst[nums.length-1],skipLast[nums.length-1]);
    }

    public int rob(int[] nums)
    {
        /*
        * Very similar to House Robber I, but since it is now a circular array, it is slightly trickier
        * Go through base cases and see how it changes the formula
        * */

        /*
         * Seems like if we have a really really big array, only thing different between
         * House Robber I and House Robber II is that we can't rob first house AND last house.
         *
         * Due to this, we should do 2 tabulations, 1 with first house and not last house
         * then 1 tabulation without first house and with last house
         * Then return Math.max(tab1,tab2)
         *
         * Tabulation would work the exact same way as House Robber I
         *
         * */

        if(nums==null || nums.length==0) return 0;
        if(nums.length==1) return nums[0];
        if(nums.length==2) return Math.max(nums[0],nums[1]);

        int length = nums.length;

        // Let's do scenario where we don't rob the first house

        int[] skipFirstHouseTable = new int[length+1];

        skipFirstHouseTable[0] = 0; // default
        skipFirstHouseTable[1] = 0; // Skipping first house

        for(int i=2;i<=length;i++)
        {
            skipFirstHouseTable[i] = Math.max(skipFirstHouseTable[i-1],skipFirstHouseTable[i-2]+nums[i-1]);
        }

        // Scenario where we don't rob the last house

        int[] skipLastHouseTable = new int[length+1];

        skipLastHouseTable[0] = 0;       // default
        skipLastHouseTable[1] = nums[0]; // rob first house
        skipLastHouseTable[2] = nums[0]; // this scenario, we always rob first house, so second house is not an option

        for(int i=3;i<length;i++)
        {
            skipLastHouseTable[i] = Math.max(skipLastHouseTable[i-1],skipLastHouseTable[i-2]+nums[i-1]);
        }

        // Since we skip the last house here, we are also skipping calculation for that slot
        // Thus, we need to set that value to the prior index

        skipLastHouseTable[length] = skipLastHouseTable[length-1];

        return Math.max(skipFirstHouseTable[length],skipLastHouseTable[length]);
    }
}
