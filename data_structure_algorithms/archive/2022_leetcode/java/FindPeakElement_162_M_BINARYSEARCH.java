package review.leetcode.leetcodeExtra;

public class FindPeakElement_162_M_BINARYSEARCH
{
    /*
    * https://leetcode.com/problems/find-peak-element/
    * */

    /*
    * Problem asks us to write something in O(logn) time
    * So we can assume we need to use something like binary search or min/max heap
    *
    * For binary search to work, the list must be sorted.
    * We are given that nums[i] != nums[i+1] so from one index to another, it's always ascending or descending
    * so this list is indeed sorted at some point
    *
    * */

    // Trick to this problem is to find the middle point
    // Then check whether we are descending/ascending from one of its neighbors
    // And continue our binary search with the side that has an ascending

    public int findPeakElement(int[] nums)
    {
        int left=0;
        int right=nums.length-1;
        while(left<right)
        {
            int middle = (left+right)/2;
            // If right of middle is still ascending, check the right side of the array
            // Otherwise, check the left side of the array
            if(nums[middle] < nums[middle+1]) left = middle + 1;
            else right = middle;
        }
        // When we are out of the loop, left=right, so it doesn't really matter which one we return
        return left;
    }
}
