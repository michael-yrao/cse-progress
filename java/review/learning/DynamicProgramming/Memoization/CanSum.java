package review.learning.DynamicProgramming.Memoization;

import java.util.HashMap;
import java.util.Map;

public class CanSum
{
    /*
    * Assuming nums has non-negative numbers.
    * Return true/false dependent on whether you can get target from numbers within the array
    * You can take multiple of the same number
    *
    * Time Complexity: O(n^m) where m is the target but it's also the height of the decision tree
    * Space Complexity: O(m)
    * */

    public boolean canSum(int[] numbers, int target)
    {
        // Base cases
        // If we have target < 0, it's impossible to get to negatives with only positive #s
        // If we have target = 0, we can assume true without having to add anything in numbers
        if(target<0)  return false;
        if(target==0) return true;

        for(Integer x : numbers)
        {
               int remainder = target - x;
               // If we hit the target==0 base case, we can return from the method
               if (canSum(numbers, remainder)) return true;
        }

        // If we do not return from the loop, we would assume no solution was found, thus false

        return false;
    }

    /*
    * Time Complexity: O(m*n)
    * Space Complexity: O(m)
    * */

    public boolean canSumMemoization(int[] numbers, int target)
    {
        Map<Integer, Boolean> memo = new HashMap<>();
        return canSumMemoizationHelper(numbers,target,memo);
    }

    public boolean canSumMemoizationHelper(int[] numbers, int target, Map<Integer, Boolean> memo)
    {
        // Base cases
        if(memo.containsKey(target)) return memo.get(target);
        if(target<0)  return false;
        if(target==0) return true;

        for(Integer x : numbers)
        {
            int remainder = target - x;
            if (canSumMemoizationHelper(numbers, remainder, memo))
            {
                memo.putIfAbsent(target,true);
                return true;
            }
        }

        // If this point is reached, there is no possible solution

        memo.putIfAbsent(target,false);
        return false;

    }

}
