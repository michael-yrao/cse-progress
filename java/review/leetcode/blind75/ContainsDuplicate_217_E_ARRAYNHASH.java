package review.leetcode.blind75;

import java.util.HashSet;
import java.util.Set;

public class ContainsDuplicate_217_E_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/contains-duplicate/
    * */

    public boolean containsDuplicate(int[] nums)
    {
        // Since this is asking if anything appears more than once, we can just use a Set

        Set<Integer> set = new HashSet<>();

        for(Integer x : nums)
        {
            if(set.contains(x)) return true;
            set.add(x);
        }
        return false;

    }

}
