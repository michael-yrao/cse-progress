package review.leetcode.blind75;

public class JumpGame_55_M_GREEDY
{
    /*
    * https://leetcode.com/problems/jump-game/
    * */



    public boolean canJump(int[] nums)
    {
        /*
            Best way to solve this is probably go backwards
            See if we can reach last index by its previous index
            and continue from there

            1. Loop from the back of the array
            2. Check if nums[i] + i >= currentGoal
            3. If it is, set currentGoal to i
            4. If currentGoal is 0 at the end, return true

        */

        int currentGoal = nums.length-1;

        for(int i=nums.length-1;i>=0;i--)
        {
            if(i+nums[i] >= currentGoal) currentGoal=i;
        }
        return currentGoal==0;
    }
}
