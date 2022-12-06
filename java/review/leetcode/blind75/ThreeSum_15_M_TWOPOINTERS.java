package review.leetcode.blind75;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ThreeSum_15_M_TWOPOINTERS
{
    /*
    * https://leetcode.com/problems/3sum/
    * */

    public List<List<Integer>> threeSum(int[] nums)
    {
        // a + b + c = 0
        // [-1,0,1,2,-1,-4]
        // [[-1,-1,2],[-1,0,1]]

        // Let a = value at current index
        // Use Two Sum to find b and c

        // Seems to be impossible to do this better than O(nlogn), so we will sort first
        // This opens up a simplified Two Pointer solution for Two Sum

        Arrays.sort(nums);

        List<List<Integer>> resultList = new ArrayList<>();

        for(int i=0;i<nums.length;i++)
        {
            int a = nums[i];
            int target = -a; // need to find b and c to match a
            int left=i+1;
            int right=nums.length-1;
            while(left<right)
            {
                if(nums[left]+nums[right]==target)
                {
                    List<Integer> potentialResult = new ArrayList<>();
                    potentialResult.add(i);
                    potentialResult.add(left);
                    potentialResult.add(right);
                    resultList.add(potentialResult);
                    while(left<right && nums[left]==nums[left+1]) left++; // avoid duplicates for b
                    while(left<right && nums[right]==nums[right-1]) right--; // avoid duplicates for c
                }
                else if(nums[left]+nums[right]<target) left++;
                else right--;
            }
        }
        return resultList;
    }
}
