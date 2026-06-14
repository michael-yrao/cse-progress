package review.leetcode.leetcodeExtra;

public class MajorityElement_169_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/majority-element/
    * */

    /*
    * The trivial solution is just to use a freq map and get the value with highest freq
    *
    * However, here we are to understand and implement Boyer-Moore's Majority Voting Algorithm
    * 1. Boyer-Moore Majority Voting Algorithm is reliant on an element appearing n/2 times
    * 2. We use a counter and an int result variable
    * */
    public int majorityElement(int[] nums)
    {
        int count=0, result=nums[0];

        /*
        * 1. Go through array checking if current value is same as our presumed result
        * 2. If it is, we increment count, otherwise we decrement count
        * 3. Notice that every time counter goes below 0,
        *    the current element is no longer the majority of this current subarray, thus we reset whenever we hit <0
        *
        * */

        for(int i=0;i<nums.length;i++)
        {
            if(nums[i]!=result) count--;
            else count++;
            if(count<0)
            {
                result = nums[i];
                count=1;
            }
        }
        return result;
    }
}
