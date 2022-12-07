package review.leetcode.blind75;

public class ProductOfArrayExceptSelf_238_M_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/product-of-array-except-self/
    * */

    // Input: nums = [1,2,3,4]
    // Output: [24,12,8,6]

    public int[] productExceptSelf(int[] nums)
    {
        // Idea here is to try a "Divide & Conquer Algorithm"
        // e.g. multiplying everything to the left and right of each number
        // We will have an left array and a right array

        // Using example above: Input: nums = [1,2,3,4]
        // left = [1,1,2,6]
        // right = [24,12,4,1]
        // Result = left[i] * right[i]

        if(nums == null || nums.length==0) return nums;

        int[] leftProduct = new int[nums.length];

        leftProduct[0] = 1;

        for(int i=1;i<leftProduct.length;i++)
        {
            leftProduct[i] = leftProduct[i-1] * nums[i-1];
        }

        int[] rightProduct = new int[nums.length];

        rightProduct[rightProduct.length-1] = 1;

        for(int i=rightProduct.length-2;i>=0;i--)
        {
            rightProduct[i] = rightProduct[i+1] * rightProduct[i+1];
        }

        int[] result = new int[nums.length];

        for(int i=0;i<result.length;i++)
        {
            result[i] = leftProduct[i]*rightProduct[i];
        }

        return result;

    }

}
