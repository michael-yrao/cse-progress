package review.leetcode.leetcodeExtra;

public class RemoveElement_27_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/remove-element/
    * */

    public int removeElement(int[] nums, int val)
    {
        int pointer = 0;
        for(int i=0;i<nums.length;i++)
        {
            if(nums[i]!=val)
            {
                nums[pointer] = nums[i];
                pointer++;
            }
        }
        return pointer;
    }
}
