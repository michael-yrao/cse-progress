package review.leetcode.blind75;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class LongestRepeatingCharacterReplacement_424_M_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/longest-repeating-character-replacement/
    * */

    public int characterReplacement(String s, int k)
    {
        int leftWindow = 0;
        int rightWindow = 0;

        // Since we care about count, we should create a frequency map

        Map<Character, Integer> freqMap = new HashMap<>();
        int maxCount = Integer.MIN_VALUE;

        // General idea is that we want to go through the String
        // Add character counter into our map

        while(rightWindow<s.length())
        {
            freqMap.put(s.charAt(rightWindow),freqMap.getOrDefault(s.charAt(rightWindow),0)+1);
            // Make sure the window is valid
            // rightWindow-leftWindow+1 is the length of our current window
            // If we subtract the most frequent item from the map, we can find how many distinct characters
            // If that is > k, we want to shift our left pointer
            while(rightWindow-leftWindow+1 - Collections.max(freqMap.values()) > k)
            {
                freqMap.put(s.charAt(leftWindow),freqMap.get(s.charAt(leftWindow))-1);
                leftWindow++;
            }
            // If we are out of the loop, that means the window is valid, so we should update max if necessary
            maxCount = Math.max(maxCount,rightWindow-leftWindow+1);
            rightWindow++;
        }
        return maxCount;
    }

    public int characterReplacementOptimized(String s, int k)
    {
        int leftWindow = 0;
        int rightWindow = 0;

        // Since we care about count, we should create a frequency map

        Map<Character, Integer> freqMap = new HashMap<>();
        int maxCount = Integer.MIN_VALUE;
        int maxFrequency = 0;

        // General idea is that we want to go through the String
        // Add character counter into our map

        while(rightWindow<s.length())
        {
            freqMap.put(s.charAt(rightWindow),freqMap.getOrDefault(s.charAt(rightWindow),0)+1);

            // This max Frequency implementation optimizes our code quite a bit so we don't have to go through the entire map to find the max

            maxFrequency = Math.max(maxFrequency,freqMap.get(s.charAt(rightWindow)));

            // Make sure the window is valid
            // rightWindow-leftWindow+1 is the length of our current window
            // If we subtract the most frequent item from the map, we can find how many distinct characters
            // If that is > k, we want to shift our left pointer
            while(rightWindow-leftWindow+1 - maxFrequency > k)
            {
                freqMap.put(s.charAt(leftWindow),freqMap.get(s.charAt(leftWindow))-1);
                leftWindow++;
            }
            // If we are out of the loop, that means the window is valid, so we should update max if necessary
            maxCount = Math.max(maxCount,rightWindow-leftWindow+1);
            rightWindow++;
        }
        return maxCount;
    }

}
