package review.leetcode.leetcodeExtra;

import java.util.HashMap;
import java.util.Map;

public class PermutationInString_567_M_SLIDINGWINDOW
{
    /*
    * https://leetcode.com/problems/permutation-in-string/
    * */


    /*
    * Input: s1 = "ab", s2 = "eidbaooo"
    * Output: true
    * Explanation: s2 contains one permutation of s1 ("ba").
    * */

    // We can actually just do this with one singular array since we know it is lowercase only
    // needle is + in the freq Array
    // hayStack is - in the freq Array

    public boolean checkInclusionFrequencyArray(String needle, String hayStack)
    {
        if(hayStack.length()<needle.length()) return false;

        int[] freqArray = new int[26];

        for(int i=0;i<needle.length();i++)
        {
            freqArray[needle.charAt(i)-'a']++;
            freqArray[hayStack.charAt(i)-'a']--;
        }

        // If we already found a match in the first search, we can just return

        if(isPermutation(freqArray)) return true;

        for(int i=needle.length();i<hayStack.length();i++)
        {
            // If we are here, that means no matches have been found
            // If that is the case, we need to re-add the portions that we took out
            freqArray[hayStack.charAt(i)-'a']--;
            freqArray[hayStack.charAt(i-needle.length())-'a']++;
            if(isPermutation(freqArray)) return true;
        }
        return false;
    }

    public boolean isPermutation(int[] freqArray)
    {
        for(int i=0;i<freqArray.length;i++)
        {
            if(freqArray[i]!=0) return false;
        }
        return true;
    }


    // This solution is too slow
    // We need to traverse through needle in case of any match then mismatch and we always traverse through hayStack
    // Therefore, this time complexity is always O(n*m) where m can be m to m^(n/m)

    public boolean checkInclusion(String needle, String hayStack)
    {
        // permutation of needle must be a substring in hayStack

        // Since we don't care about the ordering of needle in hayStack, we can put every character of needle into a Set
        // Whenever we find a matching character, we should set left to beginning of that substring <- NOT TRUE
        // Need to use a Hashmap or Array in order to keep track of count

        Map<Character,Integer> freqMap = resetNeedleMap(needle);

        int left=0;
        int right=0;

        while(right<hayStack.length())
        {
            if(freqMap.containsKey(hayStack.charAt(right)) && freqMap.get(hayStack.charAt(right)) > 0)
            {
                // Decrement the map frequency

                if(freqMap.get(hayStack.charAt(right)) >= 1) freqMap.put(hayStack.charAt(right),freqMap.get(hayStack.charAt(right))-1);

                // After the decrement, check to see if everything

                if(freqMap.values().stream().mapToInt(Integer::intValue).sum() == 0 && right-left+1==needle.length()) return true;
            }
            else
            {
                // if we are here AND left != right, that means we did find something that matched but now we don't
                // so we need to reset the needle map
                if(left!=right)
                {
                    freqMap = resetNeedleMap(needle);
                }
                right=left;
                left++;
            }
            right++;
        }
        return false;
    }

    // O(n) for each reset

    public Map<Character, Integer> resetNeedleMap(String needle)
    {
        Map<Character,Integer> freqMap = new HashMap<>();
        for(int i=0;i<needle.length();i++)
        {
            freqMap.put(needle.charAt(i),freqMap.getOrDefault(needle.charAt(i),0)+1);
        }
        return freqMap;
    }
}
