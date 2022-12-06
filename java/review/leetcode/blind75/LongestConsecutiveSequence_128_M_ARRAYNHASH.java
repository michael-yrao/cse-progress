package review.leetcode.blind75;

import java.util.HashSet;
import java.util.Set;

public class LongestConsecutiveSequence_128_M_ARRAYNHASH
{

    /*
    * https://leetcode.com/problems/longest-consecutive-sequence/
    *
    // Input: [100,4,200,1,3,2]
    // Output: 4
    // Requirement: algorithm must run in O(n) time, thus sorting is not an option
    *
    * */

    public int longestConsecutive(int[] nums)
    {
        // In order to find the longest consecutive sequence
        // We need to find the start of each sequence
        // Since we also know it has to be a sequence, each element + 1 must also exist for us to increment our longest counter
        // Since we need to search elements quite often, it would be beneficial to put the data into a HashSet
        // It doesn't really matter if numbers repeat or not, it doesn't affect the length

        if(nums.length==1) return 1;

        Set<Integer> hashSet = new HashSet<>();

        for(Integer x : nums)
        {
            hashSet.add(x);
        }

        int longestSequence=Integer.MIN_VALUE;

        for(Integer x : nums)
        {

            // We want to find the start of the sequence for x
            // If the set doesn't contain x - 1, it means this is start of sequence

            if(!hashSet.contains(x-1))
            {
                // Now we want to see just how long this sequence is
                int currentLongestSequence=0;
                while(hashSet.contains(x+currentLongestSequence))
                {
                    currentLongestSequence++;
                }
                longestSequence=Math.max(longestSequence,currentLongestSequence);
            }
        }
        return longestSequence;

    }

}
