package review.leetcode.leetcodeExtra;

import java.util.ArrayList;
import java.util.List;

public class Subsets_78_M_BACKTRACKING
{
    /*
    * https://leetcode.com/problems/subsets/
    * */

    /*
    *
    * This is basically a combination problem but you want everything from size 0 to nums.length
    * So what we can first try to do is implement exactly that first and see if we can come up with something better later
    *
    * */

    public List<List<Integer>> subsets(int[] nums)
    {
        /*
            If we want literally every permutation of nums, we are doing backtracking
            1. We need a way to prevent duplicates, not sure how to do this just yet
            2. We need a decision tree that basically says whether to take or not take the current index,
               which is just 2 decisions, so our backtracking solution would be O(2^n)
        */

        List<Integer> currentSolution = new ArrayList<>();

        List<List<Integer>> result = new ArrayList<>();

        backtrack(0,nums,currentSolution,result);

        return result;
    }


    private void backtrack(int currentIndex, int[] nums, List<Integer> currentSolution, List<List<Integer>> result)
    {
        if(currentIndex>=nums.length)
        {
            result.add(new ArrayList<>(currentSolution));
            return;
        }

        // Choose to take current index

        currentSolution.add(nums[currentIndex]);

        backtrack(currentIndex+1,nums,currentSolution,result);

        currentSolution.remove(currentSolution.size()-1);

        // Choose not to take current index

        backtrack(currentIndex+1,nums,currentSolution,result);
    }
}
