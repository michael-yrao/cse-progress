package review.leetcode.blind75;

import java.util.HashMap;
import java.util.Map;

public class ValidAnagram_242_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/valid-anagram/
    * */

    public boolean isAnagram(String s, String t)
    {
        // All anagrams are equal if sorted
        // All anagrams have same frequency of characters

        Map<Character, Integer> sFrequency = new HashMap<>();
        Map<Character, Integer> tFrequency = new HashMap<>();

        for(int i=0;i<s.length();i++)
        {
            sFrequency.put(s.charAt(i), sFrequency.getOrDefault(s.charAt(i),0)+1);
        }

        for(int i=0;i<t.length();i++)
        {
            tFrequency.put(t.charAt(i), tFrequency.getOrDefault(t.charAt(i),0)+1);
        }

        return sFrequency.equals(tFrequency);
    }

}
