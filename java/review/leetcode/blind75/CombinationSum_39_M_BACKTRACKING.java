package review.leetcode.blind75;

import java.util.ArrayList;
import java.util.List;

public class CombinationSum_39_M_BACKTRACKING
{
    /*
    * https://leetcode.com/problems/combination-sum/
    * */

    /*
     * This is basically coin change but we want the list of everything that added up to the target
     * So a complex version of Coin Change II
     * */

    public List<List<Integer>> combinationSum(int[] candidates, int target)
    {
        /*
        If we think of a decision tree, this is again a 2 decision tree, whether to use or not to use current value
        which gives us a O(2^n) algorithm

        1. We need to do backtrack
        2. Our base case will be when our target becomes 0
        3. If our target goes below 0, this isn't a possible answer, so we just return
        4. Completely missed the fact we can use the same index multiple times,
           thus when we choose to use current index, we don't want to increment the index until we've used it up completely
        */

        List<List<Integer>> result = new ArrayList<>();
        List<Integer> currentSolution = new ArrayList<>();

        backtrack(0,target,candidates,currentSolution,result);

        return result;
    }

    private void backtrack(int currentIndex, int target, int[] candidates, List<Integer> currentSolution, List<List<Integer>> result)
    {
        if(currentIndex == candidates.length)
        {
            if(target==0) result.add(new ArrayList<>(currentSolution));
            return;
        }

        if(target<0) return;

        if(candidates[currentIndex] <= target)
        {
            // Choose current index

            currentSolution.add(candidates[currentIndex]);

            backtrack(currentIndex,target-candidates[currentIndex],candidates,currentSolution,result);

            currentSolution.remove(currentSolution.size()-1);
        }

        // Do not choose current index

        backtrack(currentIndex+1,target,candidates,currentSolution,result);
    }
}
