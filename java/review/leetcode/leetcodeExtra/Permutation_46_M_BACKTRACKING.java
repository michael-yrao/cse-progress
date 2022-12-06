package review.leetcode.leetcodeExtra;

import java.util.ArrayList;
import java.util.List;

public class Permutation_46_M_BACKTRACKING
{
    /*
    * https://leetcode.com/problems/permutations/
    * */

    /*
    * Input: nums = [1,2,3]
    * Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    * */

    public List<List<Integer>> permuteSecondSubmission(int[] nums)
    {
        /*

        This problem is kind of an extension of Subsets but instead of creating every single permutation, we want permutation with size of nums.length
        Thus this changes how we set our base case

        1. Using a decision tree, we notice our decisions shrinks at every level
        2. What we should do is basically ensure we don't choose the same element again
        3. If we go out of bounds, return
        4. If we reach a solution of size nums.length, add it to the result
        5. We want every permutation of size nums.length, so we need to loop through nums to generate
        */

        List<List<Integer>> result = new ArrayList<>();

        backtrack(0,nums,new ArrayList<>(), result);

        return result;
    }

    private void backtrack(int currentIndex, int[] nums, List<Integer> currentSolution, List<List<Integer>> result)
    {
        if(currentIndex==nums.length)
        {
            result.add(new ArrayList<>(currentSolution));
            return;
        }

        // For every possible combination, we want to generate a solution

        for(int i=0;i<nums.length;i++)
        {
            if(currentSolution.contains(nums[i])) continue;
            currentSolution.add(nums[i]);
            backtrack(currentIndex+1,nums,currentSolution,result);
            currentSolution.remove(currentSolution.size()-1);
        }
    }









    /*
    * Get all permutations, since we need every single permutation, we just need to backtrack to get them all
    * Since we know permutations are of length nums.length, we can just use that as our base case
    *
    * So this is not a very normal backtracking problem because our decision tree's decisions decrease at every level
    * What we can try instead is actually swap the values in the input array instead
    *
    * */

    public List<List<Integer>> permute(int[] nums)
    {
        List<List<Integer>> result = new ArrayList<>();
        int solutionLength = nums.length;
        permuteBacktrack(nums, solutionLength, 0, result);
        return result;
    }

    public void permuteBacktrack(int[] nums, int length, int currentIndex, List<List<Integer>> result)
    {
        // Base case
        if(currentIndex == length)
        {
            List<Integer> list = new ArrayList<>();
            for(Integer x : nums) list.add(x);
            result.add(list);
            return;
        }

        // Go through each index of the original list and perform every possible swap
        for(int i=currentIndex;i<length;i++)
        {
            swap(nums,i,currentIndex);
            permuteBacktrack(nums,length,currentIndex+1,result);
            swap(nums,i,currentIndex);
        }
    }

    public void swap(int[] nums, int firstIndex, int secondIndex)
    {
        int temp = nums[firstIndex];
        nums[firstIndex] = nums[secondIndex];
        nums[secondIndex] = temp;
    }
}
