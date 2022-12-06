package review.leetcode.leetcodeExtra;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class SubsetsII_90_M_BACKTRACKING
{
    /*
    * https://leetcode.com/problems/subsets-ii/
    * */

    /*
    * This problem is quite interesting, we are doing backtracking but we also need to make sure
    * we don't add anything that we've already added before
    * */

    public List<List<Integer>> subsetsWithDupSecondSubmission(int[] nums)
    {
        /*

        If we think of this as a decision tree, we can do a simple decision of whether or not take the current index
        How do we ensure we don't make duplicated results..

        One thing we need to remember is that we can manipulate the data if necessary
        One hint is actually in the problem example which shows the number in order

        Thus we need to order the array in order to find some pattern in our numbers

        1. Sort nums array
        2. Have a backtrack helper method as normal
        3. For our base case, we can just do if our current index is outside of bounds, we add to solution
        4. Add current value to the list
        5. Increment index until next value is not same as current value

        */

        List<List<Integer>> result = new ArrayList<>();

        Arrays.sort(nums);

        backtrack(0,nums,new ArrayList<>(), result);

        return result;
    }


    private void backtrack(int currentIndex, int[] nums, List<Integer> currentSolution, List<List<Integer>> result)
    {
        if(currentIndex>=nums.length)
        {
            result.add(new ArrayList<>(currentSolution));
            return;
        }

        currentSolution.add(nums[currentIndex]);

        backtrack(currentIndex+1,nums,currentSolution,result);

        currentSolution.remove(currentSolution.size()-1);

        while(currentIndex+1<nums.length && nums[currentIndex+1]==nums[currentIndex]) currentIndex++;

        backtrack(currentIndex+1,nums,currentSolution,result);
    }


    public List<List<Integer>> subsetsWithDup(int[] nums)
    {
        /*
        * Key to note here is we need to know the relationship between our current value and next value
        * e.g. if they are the same number, we don't want to add it to our solution
        * Therefore, we need to sort the array before we start any implementation
        * */
        Arrays.sort(nums);
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> currentSolution = new ArrayList<>();
        subsetsWithDupBacktrack(nums,0,currentSolution,result);
        return result;
    }

    public void subsetsWithDupBacktrack(int[] nums, int currentIndex, List<Integer> currentSolution, List<List<Integer>> result)
    {
        // Base case
        if(currentIndex >= nums.length)
        {
            result.add(new ArrayList<>(currentSolution));
            return;
        }

        // Backtrack
        currentSolution.add(nums[currentIndex]);
        subsetsWithDupBacktrack(nums,currentIndex+1, currentSolution,result);
        currentSolution.remove(currentSolution.size()-1);

        // If we have same value, just skip to next iteration
        while(currentIndex + 1 < nums.length && nums[currentIndex] == nums[currentIndex+1])
            currentIndex++;

        subsetsWithDupBacktrack(nums,currentIndex+1, currentSolution,result);
    }
}
