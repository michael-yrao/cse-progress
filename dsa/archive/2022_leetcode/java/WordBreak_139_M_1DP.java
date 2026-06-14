package review.leetcode.blind75;

import java.util.List;

public class WordBreak_139_M_1DP
{
    /*
    * https://leetcode.com/problems/word-break/
    * */

    /*
    * Brute-Force, we can check to see if each word in wordDict matches first word.length characters in String s
    * and loop until the end. This ends up with a O(n*m^2) solution
    *
    * The most efficient method is using bottom-up Dynamic Programming.
    *   1. Have a boolean cache of size s.length + 1
    *   2. Default last index of cache to true, otherwise false
    *   3. Each index of the cache indicates whether or not we can match a word starting with index i
    *   4. Iterate from end to beginning to populate cache
    *
    * Input: s = "leetcode", wordDict = ["leet","code"]
    *
    * */

    public boolean wordBreak(String s, List<String> wordDict)
    {
        boolean[] cache = new boolean[s.length()+1];
        cache[cache.length-1] = true;

        for(int i=s.length()-1;i>=0;i--)
        {
            for(String word : wordDict)
            {
                // Check if length of word + i surpasses length of s
                // If not, then we can see if word matches substring of s
                if(i+word.length() <= s.length() && s.substring(i,i+word.length()).equals(word))
                    cache[i] = cache[i+word.length()];

                // If we found a match already for this section
                if(cache[i]) break;
            }
        }
        return cache[0];
    }
}
