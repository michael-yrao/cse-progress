package review.leetcode.blind75;

import java.util.HashSet;
import java.util.Set;

public class LongestSubstringWithoutRepeatingCharacters_3_M_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/longest-substring-without-repeating-characters/
    * */

    public int lengthOfLongestSubstring(String s)
    {

        /*
            Idea here is to using the Sliding Window technique
            We'll have 2 pointers both starting at index 0, have a max variable to keep track of current maximum
            Since we want no repeating characters, we should use a Set to store characters currently in our window
            If we find a character that is already in the Set, e.g. already exist,
            We should remove the character at the left pointer and increment it.
            Otherwise, add the character to the Set and increment right
        */

        Set<Character> characterSet = new HashSet<>();

        if(s == null || s.isEmpty()) return 0;
        if(s.length() == 1) return 1;

        int left=0,right=0,max=Integer.MIN_VALUE;
        Set<Character> set = new HashSet<>();

        while(right<s.length())
        {
            // If we bump into a duplicate, remove left char, increment left
            if(!set.isEmpty() && set.contains(s.charAt(right)))
            {
                set.remove(s.charAt(left++));
            }
            else
            {
                set.add(s.charAt(right++));
            }
            max=Math.max(max,right-left); // We don't do right-left+1 here since we already incremented one or the other
        }
        return max;
    }
}
