package review.leetcode.leetcodeExtra;

public class JumpGameII_45_M_GREEDY
{
    /*
    * https://leetcode.com/problems/jump-game-ii/
    * */

    public int minJump(int[] nums)
    {
        // [2,3,1,1,4]

        // If we think about this as a decision tree, 0 can jump to 1 and 2
        // Afterwards, 1 can jump to 2,3,4 and 2 can jump to 3
        //
        // Looks to be a 1D BFS to find shortest path to last position

        int height=0;           // Height is the decision tree height
        int furthestJump=0;     // Furthest position we can get to (should continuously go up as we go through the levels)
        int endOfLevel=0;       // Stores the last index where the level is going to be

        // We only iterate to 2nd to last char since we don't quite care what the last char is
        for(int i=0;i<nums.length;i++)
        {
            furthestJump = Math.max(furthestJump,i+nums[i]);
            if(i==endOfLevel) // If we have reached the end of the level, set end of level to furthest jump point
            {
                height++;
                endOfLevel=furthestJump;
            }
        }
        return height;
    }

}
