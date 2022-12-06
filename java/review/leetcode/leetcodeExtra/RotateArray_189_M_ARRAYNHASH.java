package review.leetcode.leetcodeExtra;

public class RotateArray_189_M_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/rotate-array/
    * */

    /*
    *
    * O(n) time; O(1) space solution
    *
    * 1. Reverse the array
    * 2. Reverse the first k elements
    * 3. Reverse the last nums.length-k elements
    * */

    public void rotate(int[] nums, int k)
    {
        /*
        * Java doesn't do reverse partial very easily so we have to write one ourselves
        * */
        reverseArray(nums,0,nums.length - 1);
        reverseArray(nums, 0, (k%nums.length) - 1);
        reverseArray(nums, (k%nums.length), nums.length - 1);
    }

    public void reverseArray(int[] array, int startIndex, int endIndex)
    {
        for(int i=startIndex,j=endIndex;
            i<j;
            i++,j--)
        {
            swap(array,i,j);
        }
    }

    public void swap(int[] array, int firstIndex, int secondIndex)
    {
        int temp = array[firstIndex];
        array[firstIndex] = array[secondIndex];
        array[secondIndex] = temp;
    }
}
