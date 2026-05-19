package review.leetcode.blind75;

import DataStructure.Pair;

import java.util.HashMap;
import java.util.Map;

public class RegularExpressionMatching_10_H_2DP
{
    /*
    * https://leetcode.com/problems/regular-expression-matching/
    * */


    /*
     * We can try to understand this problem by doing a decision tree
     *
     * We'll ignore the period for now as it can match any character of size 1
     * But for *, we can match the preceding character from 0-infinite amount of times
     *
     * e.g. given String aa and Pattern a*
     * We can use the Pattern to form a decision tree to try to match with String aa
     *      null
     *     .    .
     *   "a"     ""             Here we can choose an empty string or choose 1 a to match with first character in String
     *
     * e.g. Given String "aab" and Pattern "c*a*b"
     *      null
     *     .    .
     *   "c"    "" <- Here we notice that we can't even take c since it doesn't match first character of String
     *                So we need to skip this pattern entirely to a.
     *                What this means for our algorithm is that we need a pointer at String and a pointer at Pattern
     *                We start with sp at 0 and pp at 0
     *                pp moves pp+2 when we want to skip over the star pattern
     *                sp moves sp+1 when we want to choose to use the star pattern, we can only use star pattern if previous character matches
     *                For non-star, we just try to match pp and sp and if they match, we move both+1, otherwise return false
     *                We can return true if BOTH sp and pp are out of bounds
     *
     *  Special Cases:
     *    1. pp is out of bound but sp is not out of bounds, return false
     *    2. sp is out of bound but pp is not out of bounds (e.g. s = "a"; p = "a*b*")
     *
     * If we just go with this decision tree solution, we will end up with a O(2^n) solution since we got 2 decisions here
     *
     * What we can do to help us alleviate some of this is maybe try to add memoization and just store the values we calculated
     *
     * */

    // Top-down Memoization

    public boolean isMatch(String string, String pattern)
    {
        // For the memoization solution, we will use a cache of the 2 pointers and check if we have already done that check
        Map<Pair<Integer,Integer>,Boolean> cache = new HashMap<>();
        return isMatchBacktrack(string,pattern,cache,0,0);
    }

    private boolean isMatchBacktrack(String string, String pattern, Map<Pair<Integer,Integer>,Boolean> cache, int stringPointer, int patternPointer)
    {
        // Memoization portion
        Pair<Integer,Integer> pointerPair = new Pair(stringPointer,patternPointer);
        if(cache.containsKey(pointerPair)) return cache.get(pointerPair);

        // Case as described on line 36
        if(stringPointer>=string.length() && patternPointer>=pattern.length()) return true;
        // Case as described on line 39
        if(patternPointer>=pattern.length()) return false;

        // Check if first character matches
        // Make sure to check if string pointer is within boundaries

        boolean match = stringPointer < string.length()
                && (match = string.charAt(stringPointer) == pattern.charAt(patternPointer) || pattern.charAt(patternPointer) == '.');

        // Check for star
        if(patternPointer+1<pattern.length() && pattern.charAt(patternPointer+1)=='*')
        {
            cache.put(pointerPair,
            // Use the star      (described in line 34)
                    (isMatchBacktrack(string,pattern,cache,stringPointer,patternPointer+2)
            // Dont use the star (described in line 33)
                    ||(match && isMatchBacktrack(string,pattern,cache,stringPointer+1,patternPointer))));
            return cache.get(pointerPair);
        }

        // If not star, just check if character match is true
        // and increment both pointers as specified on line 35

        if(match)
        {
            cache.put(pointerPair,isMatchBacktrack(string,pattern,cache,stringPointer+1,patternPointer+1));
            return cache.get(pointerPair);
        }

        // If we never returned from any of the above, just return false
        cache.put(pointerPair,false);
        return false;
    }


    // Backtrack solution without DP

    public boolean isMatchInefficientSolution(String string, String pattern)
    {
        return isMatchBacktrackOnly(string,pattern,0,0);
    }

    private boolean isMatchBacktrackOnly(String string, String pattern, int stringPointer, int patternPointer)
    {
        // Case as described on line 36
        if(stringPointer>=string.length() && patternPointer>=pattern.length()) return true;
        // Case as described on line 39
        if(patternPointer>=pattern.length()) return false;

        // Check if first character matches
        // Make sure to check if string pointer is within boundaries

        boolean match = stringPointer < string.length()
                && (match = string.charAt(stringPointer) == pattern.charAt(patternPointer) || pattern.charAt(patternPointer) == '.');

        // Check for star
        if(patternPointer+1<pattern.length() && pattern.charAt(patternPointer+1)=='*')
        {
            return
            // Dont use the star (described in line 33)
             (isMatchBacktrackOnly(string,pattern,stringPointer,patternPointer+2)
            // Use the star      (described in line 34)
             ||(match && isMatchBacktrackOnly(string,pattern,stringPointer+1,patternPointer)));
        }

        // If not star, just check if character match is true
        // and increment both pointers as specified on line 35

        if(match) return isMatchBacktrackOnly(string,pattern,stringPointer+1,patternPointer+1);

        // If we never returned from any of the above, just return false

        return false;
    }
}
