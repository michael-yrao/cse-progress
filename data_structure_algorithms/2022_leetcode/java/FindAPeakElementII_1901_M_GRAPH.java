package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.*;

public class FindAPeakElementII_1901_M_GRAPH
{
    /*
    * https://leetcode.com/problems/find-a-peak-element-ii/
    * */

    /*
    * Extension of the first Find Peak Element
    *
    * What we can do is run a BFS on each element and that will give us the solution of O(n*m)
    * However, this doesn't get accepted on leetcode since it wants an O(nlogm) solution
    *
    * This problem has the same restrictions as the first: No two adjacent cells are equal.
    * Which means we need to find the max in each row since it will always be the "peak" in that row
    *
    * */
    public int[] findPeakGrid(int[][] mat)
    {
        int left=0;
        int right=mat.length-1;
        while(left<=right)
        {
            int mid = (left+right)/2;

            int maxIndex = findPeak1D(mat[mid]);

            // We now have a coordinate of the max, so we need to check if this value is bigger than its top and bottom

            if(mid==0)
            {
                // top row don't need to check top
                if(mat[mid][maxIndex] > mat[mid+1][maxIndex]) return new int[]{mid,maxIndex};
            }
            else if(mid==mat.length-1)
            {
                // bottom row don't need to check bottom
                if (mat[mid][maxIndex] > mat[mid-1][maxIndex]) return new int[]{mid,maxIndex};
            }
            else
            {
                // Other rows need to check both
                if(mat[mid][maxIndex] > mat[mid+1][maxIndex] && mat[mid][maxIndex] > mat[mid-1][maxIndex]) return new int[]{mid,maxIndex};
            }

            // If we are here, that means this row isn't it, so we need to decide which row to go to

            if(mat[mid][maxIndex] < mat[mid+1][maxIndex]) left = mid + 1;
            else right = mid - 1;
        }
        return new int[]{-1,-1};
    }

    // Finds the max in each row
    private int findPeak1D(int[] nums)
    {
        int max=Integer.MIN_VALUE;
        int returnIndex=-1;
        for(int i=0;i<nums.length;i++)
        {
            if(nums[i] > max)
            {
                max = nums[i];
                returnIndex=i;
            }
        }
        return returnIndex;
    }
}
