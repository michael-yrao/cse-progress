package review.leetcode.leetcodeExtra;

public class SearchInsertPosition_31_E_BINARYSEARCH
{
    /*
    * https://leetcode.com/problems/search-insert-position/
    * */

    /*
    * This problem is literally just binary search and return index of target
    * Since the given array is already sorted and distinct,
    * we don't need to do anything special and just go straight to binary search
    * */

    public int searchInsert(int[] nums, int target)
    {
        int left=0, right=nums.length-1;
        while(right>left)
        {
            // Use this formula to find mid to avoid integer overflow
            int mid = left + (right - left)/2;

            if(nums[mid]==target) return mid;
            else if(nums[mid] > target) right = mid;
            else left = mid + 1;
        }

        return (nums[left] < target)?left+1:left;
    }
}
