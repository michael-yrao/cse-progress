package review.leetcode.blind75;

public class HouseRobber_198_M_1DP
{
    /*
    * https://leetcode.com/problems/house-robber/
    * */

    /*
    * Input: nums = [1,2,3,1]
    * Output: 4 (Rob index 0 and index 2)
    *
    * [2,1,1,2] <- 0,3
    * */

    // Since we don't ever rob adjacent houses
    // Why not just rob every other house and compare
    // e.g. compare sum of odd vs even and return highest
    // However, this doesn't work: e.g. [2,1,1,2]. In this situation, we want to rob index 0 and 3

    public int robTabulation(int[] nums)
    {
        // Size 0 nums, we rob nothing
        // Size 1 nums, we rob first one
        // Size 2 nums, we rob whichever is larger

        if(nums == null || nums.length == 0) return 0;
        if(nums.length == 1) return nums[0];

        // We are doing tabulation with size of nums.length,
        // thus position 0 holds the max we can do if we have length 1
        // position 1 holds the max we can do if we have length 2

        int[] table = new int[nums.length];

        table[0] = nums[0];
        table[1] = Math.max(nums[0],nums[1]); // <- We can put this as a formula: table[i] = Math.max(table[i-1],table[i-2]+nums[i]);

        for(int i=2;i<nums.length;i++)
        {
            table[i] = Math.max(table[i-1],table[i-2]+nums[i]);
        }
        return table[nums.length-1];
    }

}
