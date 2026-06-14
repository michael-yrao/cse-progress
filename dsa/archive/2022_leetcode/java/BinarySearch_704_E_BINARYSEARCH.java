package review.leetcode.leetcodeExtra;

public class BinarySearch_704_E_BINARYSEARCH
{
    /*
    * https://leetcode.com/problems/binary-search/
    * */

    // We want to return the index of target if it is found

    public int search(int[] nums, int target)
    {
        int left=0, right=nums.length-1;

        while(left<=right)
        {
            int middle = (left+right)/2;
            if(target==nums[middle]) return middle;
            else if(target<nums[middle]) right=middle-1;
            else left=middle+1;
        }
        return -1;
    }
}
