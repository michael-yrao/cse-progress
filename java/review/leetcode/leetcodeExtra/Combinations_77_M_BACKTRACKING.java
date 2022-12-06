package review.leetcode.leetcodeExtra;

import java.util.ArrayList;
import java.util.List;

public class Combinations_77_M_BACKTRACKING
{
    /*
    * https://leetcode.com/problems/combinations/
    * */

    /*
    * n choose k means we want every combination from enumerate(n) that has length k
    *
    * This is a backtracking problem and the input k is our base case
    * */

    public List<List<Integer>> combine(int n, int k)
    {
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> currentCombination = new ArrayList<>();
        combineBacktrack(n,k,1,currentCombination,result);
        return result;
    }

    // currentIndex is actually the current enumerate from 1 - n
    // currentCombination is what we are using to build our current solution

    public void combineBacktrack(int n, int k, int currentIndex, List<Integer> currentCombination, List<List<Integer>> result)
    {
        // base cases
        if(currentIndex > n + 1) return;
        if(currentCombination.size() == k)
        {
            result.add(new ArrayList<>(currentCombination));
            return;
        }

        // Make a decision whether to choose or not to choose the current index

        // Choose current index
        currentCombination.add(currentIndex);
        combineBacktrack(n,k,currentIndex+1,currentCombination,result);
        currentCombination.remove(currentCombination.size()-1);

        // Don't choose current index
        combineBacktrack(n,k,currentIndex+1,currentCombination,result);
    }
}
