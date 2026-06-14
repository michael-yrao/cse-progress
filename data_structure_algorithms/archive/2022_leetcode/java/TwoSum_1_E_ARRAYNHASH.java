package review.leetcode.blind75;

import java.util.HashMap;
import java.util.Map;

public class TwoSum_1_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/two-sum/
    * */

    public int[] twoSum(int[] nums, int target)
    {
        Map<Integer, Integer> indiceMap = new HashMap<>();

        // Put into a Hashmap for constant time access

        for(int i=0;i<nums.length;i++)
        {
            indiceMap.put(nums[i], i);
        }

        for(int i=0;i<nums.length;i++)
        {
            int diff = target - nums[i];

            if(indiceMap.containsKey(diff) && i != indiceMap.get(diff))
            {
                return new int[] {indiceMap.get(diff), i};
            }
        }

        return null;
    }

}
