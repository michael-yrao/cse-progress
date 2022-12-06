package review.leetcode.blind75;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

public class GroupAnagram_49_M_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/group-anagrams/
    * */

    public List<List<String>> groupAnagrams(String[] strs)
    {
        // Since anagrams are all the same, we can group them together by having the sorted version as the key, then the true version as values

        HashMap<String, List<String>> map = new HashMap<>();

        for(String s : strs)
        {
            char[] charArray = s.toCharArray();
            Arrays.sort(charArray);
            String sortedString = String.valueOf(charArray);
            map.putIfAbsent(sortedString, new ArrayList<>());
            map.get(sortedString).add(s);
        }

        return new ArrayList<>(map.values());
    }
}
