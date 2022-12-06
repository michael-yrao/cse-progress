package review.leetcode.blind75;

public class SearchInRotatedSortedArray_33_M_BINARYSEARCH
{
    /*
    * https://leetcode.com/problems/search-in-rotated-sorted-array/
    * */

    public int search(int[] nums, int target)
    {
        // We know the list is sorted but split in half
        // Use a modified binary search to find the target

        int left=0;
        int right=nums.length-1;

        while(left<=right)
        {
            int middle = (left+right)/2;
            // If middle = target, return

            if(nums[middle] == target) return middle;

            // if left <= middle, this section is sorted

            if(nums[left] <= nums[middle])
            {
                if(target < nums[left] || target > nums[middle]) left = middle + 1;
                else right = middle - 1;
            }
            // left - mid is not sorted here
            else
            {
                if(target < nums[middle] || target > nums[right]) right = middle - 1;
                else left = middle + 1;
            }
        }
        return -1;
    }

}
