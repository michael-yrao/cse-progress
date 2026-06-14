package review.leetcode.leetcodeExtra;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class CombinationSumII_40_M_BACKTRACKING
{
    /*
    * https://leetcode.com/problems/combination-sum-ii/
    * */

    /*
    * 1. isValid
    * 2. getCandidates
    * 3. search
    * */

    /*
    * Think main thing here is we need to keep track of whether or not we have visited this vertex for the current solution yet
    * So what we want to do is similar to Combination Sum but we need a way to not include same number
    * But if we are not able to use same number, we might want to consider Subarray Sum Equals K
    *
    *
    * */

    public List<List<Integer>> combinationSum2SecondSubmission(int[] candidates, int target)
    {
        /*

        1. First thing we should note is that we need to generate using each number once per solution
        Thus we should increment regardless of whether we choose to use current index or not

        2. Another thing we should do is sort the array before we go into the solution.
           This way we can handle situations that might produce a duplicated result in different orders

        */

        List<List<Integer>> result = new ArrayList<>();

        Arrays.sort(candidates);

        backtrack(0,target,candidates,new ArrayList<>(),result);

        return result;
    }

    private void backtrack(int currentIndex, int target, int[] candidates, List<Integer> currentSolution, List<List<Integer>> result)
    {
        if(currentIndex == candidates.length)
        {
            if(target==0) result.add(new ArrayList<>(currentSolution));
            return;
        }

        if(candidates[currentIndex] <= target)
        {
            currentSolution.add(candidates[currentIndex]);

            backtrack(currentIndex+1,target - candidates[currentIndex],candidates,currentSolution,result);

            currentSolution.remove(currentSolution.size()-1);
        }

        while(currentIndex+1<candidates.length && candidates[currentIndex+1] == candidates[currentIndex]) currentIndex++;


        backtrack(currentIndex+1,target,candidates,currentSolution,result);
    }


    public List<List<Integer>> combinationSum2(int[] candidates, int target)
    {
        // Since we are backtracking, we will always be more than O(nlogn)
        // Thus sort the array for it to be easier to take care of the duplicate numbers
        Arrays.sort(candidates);
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> singleSolution = new ArrayList<>();
        combinationSumBacktrack(candidates,singleSolution, 0, target, result);
        return result;
    }

    public void combinationSumBacktrack(int[] candidates, List<Integer> currentCombination, int currentIndex, int target, List<List<Integer>> result)
    {
        // If our current combination sums up to our target, then we add it to the solution
        // Remember that since we are going to re-use currentCombination, we need to add a Copy of it
        if(target==0) result.add(new ArrayList<>(currentCombination));

        // If we have already found our solution OR if we have past our target
        // Then we can just return
        if(target<=0) return;

        for(int i=currentIndex;i<candidates.length;i++)
        {
            // If we have already used this index, continue
            if(i > currentIndex && candidates[i] == candidates[i-1]) continue;

            currentCombination.add(candidates[i]);
            combinationSumBacktrack(candidates, currentCombination, i+1, target - candidates[i], result);
            currentCombination.remove(currentCombination.size()-1);
        }
    }
}
