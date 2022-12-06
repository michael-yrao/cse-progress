package review.leetcode.leetcodeExtra;

import java.util.ArrayList;
import java.util.List;

public class PalindromePartitioning_131_M_BACKTRACKING
{
    /*
     * https://leetcode.com/problems/palindrome-partitioning/
     * */

    /*
    * Each List<String> makes up the full word of s
    * Seems to me like Subsets II where we want all possible subsets that are not duplicated and are palindromes
    * */

    public List<List<String>> partition(String s)
    {
        List<List<String>> result = new ArrayList<>();
        List<String> currentSolution = new ArrayList<>();
        partitionBacktrack(s, 0, currentSolution,result);
        return result;
    }

    public void partitionBacktrack(String s, int currentIndex, List<String> currentSolution, List<List<String>> result)
    {
        // Base case
        if(currentIndex == s.length())
        {
            result.add(new ArrayList<>(currentSolution));
            return;
        }

        // Need to go through each character in the String
        // Then add each palindrome substring to our current solution

        for(int i=currentIndex;i<s.length();i++)
        {
            // substring is not inclusive for ending, so need to do + 1
            String currentString = s.substring(currentIndex,i+1);

            if(isPalindrome(currentString))
            {
                currentSolution.add(currentString);
                partitionBacktrack(s,i+1, currentSolution, result);
                currentSolution.remove(currentSolution.size()-1);
            }
        }
    }

    public boolean isPalindrome(String s)
    {
        if(s.isEmpty()) return false;
        int left=0;
        int right=s.length()-1;
        while(right>left)
        {
            if(s.charAt(left) != s.charAt(right)) return false;
            right--;
            left++;
        }
        return true;
    }
}
