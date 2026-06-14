package review.leetcode.blind75;

public class MinimumInRotatedSortedArray_153_M_BINARYSEARCH
{
    /*
    * https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
    * */

    public int findMin(int[] nums)
    {
        // Since this is a rotated sorted array, we know in some degree, this array is sorted
        // Since we need to find the minimum, we need to traverse the entire array to ensure it is the minimum <- Not true since array is already sorted

        // [1,2],
        // [2,1]

        // [0,1,2,4,5,6,7],
        // [1,2,4,5,6,7,0],
        // [2,4,5,6,7,0,1],
        // [4,5,6,7,0,1,2],
        // [5,6,7,0,1,2,4],
        // [6,7,0,1,2,4,5],
        // [7,0,1,2,4,5,6]

        int min=Integer.MAX_VALUE;
        int left = 0, right = nums.length-1;

        // This covers the case of 1 single element or if the list is not rotated

        // [2,3,4,5,1]

        while(left<=right)
        {
            int mid=(left+right)/2;
            if(nums[left]<=nums[right]) return nums[left];

            if(mid>0 && nums[mid-1]>nums[mid]) return nums[mid];

            if(mid<nums.length-1 && nums[mid] > nums[mid+1]) return nums[mid+1];

            if(nums[left] <= nums[mid]) left=mid+1;
            else right=mid-1;
        }
        return min;
    }

}
