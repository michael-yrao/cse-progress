package review.leetcode.leetcodeExtra;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class ContainsDuplicatesII_219_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/contains-duplicate-ii/
    * */

    // Overthought this problem too much
    // Idea here is similar to first Contains Duplicates
    //  1. Create a Map of value -> index
    //  2. If value already exist in map, that means we should check if the old index and current index are <= k
    //  3. If it is, then just return true, otherwise we can just place the value -> index in the map.
    //     Reason we can just replace it is because we are looking for <= k, thus the old index is definitely farther
    public boolean containsNearbyDuplicate(int[] nums, int k)
    {
        Map<Integer,Integer> indicesMap = new HashMap<>();
        for(int i=0;i<nums.length;i++)
        {
            if(indicesMap.containsKey(nums[i]) && i-indicesMap.get(nums[i]) <= k) return true;
            indicesMap.put(nums[i],i);
        }

        return false;
    }
}
