package review.leetcode.leetcodeExtra;

public class ReplaceElementsWithGreatestRight_1299_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/
    * */

    /**

     1. Initial thought process is to go from end of array to start
     2. Since we care only about greatest on the right side, we know that rightmost value is -1
     3. Thus we will use a single variable that indicates the current max which will be -1 to start

     */
    public int[] replaceElements(int[] arr)
    {
        int currentMax = -1;

        for(int i=arr.length-1;i>=0;i--)
        {
            int temp = arr[i];
            arr[i] = currentMax;
            currentMax = Math.max(temp,currentMax);
        }
        return arr;
    }

}
