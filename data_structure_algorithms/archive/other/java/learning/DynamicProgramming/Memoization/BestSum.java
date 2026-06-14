package review.learning.DynamicProgramming.Memoization;

import java.util.HashMap;
import java.util.Map;

public class BestSum
{
    /*
     * Assuming nums has non-negative numbers.
     * Return a solution to the target from numbers within the array
     * You can take multiple of the same number
     *
     * This code is buggy, need some fixing
     *
     * Time Complexity: O(n^m * m) where n is numbers' size and m is height of decision tree based on target
     * Since we also do an arraycopy which is of size m, thus final time complexity is O(n^m * m)
     *
     * Space Complexity: O(m^2) since we initially have a call stack, which is height of the decision tree
     * Then we have a shortestCombination for each call stack, thus total space usage is O(m^2)
     *
    * */

    public int[] bestSum(int[] numbers, int target)
    {
        // If we have target < 0, it's impossible to get to negatives with only positive #s
        // If we have target = 0, that means an empty array can complete the problem

        if(target<0) return null;
        if(target==0) return new int[]{};

        int[] shortestCombination = null;

        for(Integer x : numbers)
        {
            int remainder = target - x;
            int[] remainderSolution = bestSum(numbers,remainder);
            if(remainderSolution!=null)
            {
                // If here, that means we do have a way to get to target sum
                int[] potentialSolution = new int[remainderSolution.length+1];
                System.arraycopy(remainderSolution,0,potentialSolution,0,remainderSolution.length);
                potentialSolution[potentialSolution.length-1] = x;
                if(shortestCombination==null || shortestCombination.length>potentialSolution.length) shortestCombination=potentialSolution;
            }
        }
        return shortestCombination;
    }

    /*
    * This code is buggy, need some fixing
    * */

    public int[] bestSumMemoization(int[] numbers, int target)
    {
        Map<Integer, int[]> memo = new HashMap<>();
        return bestSumMemoizationHelper(numbers,target,memo);
    }

    public int[] bestSumMemoizationHelper(int[] numbers, int target, Map<Integer,int[]> memo)
    {
        // If we have target < 0, it's impossible to get to negatives with only positive #s
        // If we have target = 0, that means an empty array can complete the problem

        if(memo.containsKey(target)) return memo.get(target);
        if(target<0) return null;
        if(target==0) return new int[]{};

        int[] shortestCombination = null;

        for(Integer x : numbers)
        {
            int remainder = target - x;
            int[] remainderSolution = bestSumMemoizationHelper(numbers,remainder,memo);
            if(remainderSolution!=null)
            {
                // If here, that means we do have a way to get to target sum
                int[] potentialSolution = new int[remainderSolution.length+1];
                System.arraycopy(remainderSolution,0,potentialSolution,0,remainderSolution.length);
                potentialSolution[potentialSolution.length-1] = x;
                if(shortestCombination==null || shortestCombination.length>potentialSolution.length) shortestCombination=potentialSolution;
            }
        }
        memo.putIfAbsent(target,shortestCombination);
        return shortestCombination;
    }
}
