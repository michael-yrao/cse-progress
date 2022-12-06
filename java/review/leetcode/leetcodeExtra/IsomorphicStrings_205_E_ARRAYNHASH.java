package review.leetcode.leetcodeExtra;

import java.util.HashMap;
import java.util.Map;

public class IsomorphicStrings_205_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/isomorphic-strings/
    * */

    /*
    * input: s = "egg", t = "add"; Output: true
    * input: s = "foo", t = "bar"; Output: false
    * input: s = "paper", t = "title"; Output: true
    * */

    /*
    * Idea here seems to be as such:
    * 1. Length of s and t must be the same
    * 2. Characters from s must be a 1-1 mapping to t and vice versa
    * 3. Positions from the mapping must be the same
    * */

    public boolean isIsomorphic(String s, String t)
    {
        if(s.length()!=t.length()) return false;

        Map<Character,Character> sToTMap = new HashMap<>();
        Map<Character,Character> tToSMap = new HashMap<>();

        for(int i=0;i<s.length();i++)
        {
            if(!sToTMap.isEmpty() && sToTMap.containsKey(s.charAt(i)) && sToTMap.get(s.charAt(i)) != t.charAt(i)) return false;
            if(!tToSMap.isEmpty() && tToSMap.containsKey(t.charAt(i)) && tToSMap.get(t.charAt(i)) != s.charAt(i)) return false;
            sToTMap.put(s.charAt(i),t.charAt(i));
            tToSMap.put(t.charAt(i),s.charAt(i));
        }
        return true;
    }
}