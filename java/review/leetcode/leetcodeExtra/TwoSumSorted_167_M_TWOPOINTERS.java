package review.leetcode.leetcodeExtra;

public class TwoSumSorted_167_M_TWOPOINTERS
{
    /*
    * https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
    * */

    public int[] twoSum(int[] numbers, int target)
    {
        // Since we are returning indices, we should try to keep trace of indices
        // Since everything is already sorted, we should try a two pointer technique
        // One starting left, one starting right
        // If l + r > target, we move r--. If l + r < target, we move l++, else return l,r

        int leftIndex=0;
        int rightIndex=numbers.length-1;

        while(leftIndex>rightIndex)
        {
            if(numbers[leftIndex]+numbers[rightIndex] == target) return new int[] {leftIndex+1,rightIndex+1};
            else if(numbers[leftIndex]+numbers[rightIndex] < target) leftIndex++;
            else if(numbers[leftIndex]+numbers[rightIndex] > target) rightIndex--;
            else return null;
        }
        return null;
    }
}
