package review.leetcode.leetcodeExtra;

import java.util.HashMap;
import java.util.Map;

public class ContainsDuplicatesIII_220_H_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/contains-duplicate-iii/
    * */

    /*
    * Input: nums = [1,2,3,1], indexDiff = 3, valueDiff = 0
    * Output: true
    *
    * Given input above, we need to look within the window of size (indexDiff + 1) to find 2 values with valueDiff
    *
    * What this means is we should try to bucket our values into buckets of size (indexDiff + 1)
    * So what we can do is map values of nums to their buckets, so a HashMap of bucket:value
    *
    * So what we want to do is use our map as the bucket and we will keep that bucket as size valueDiff
    *   a. This way if a number comes in and have the exact same key, we know they are less than indexDiff apart
    *
    * */

    public boolean containsNearbyAlmostDuplicate(int[] nums, int indexDiff, int valueDiff)
    {
        // If index difference is less than 1, it's not possible
        if(indexDiff<1 || valueDiff < 0) return false;

        Map<Long,Long> bucket = new HashMap<>();

        // subtracting a huge positive and a huge negative might cause issues
        // so we will convert the input integers into longs

        // Our values are at most indexDiff + 1 apart, so thus bucketSize

        long bucketSize = (long)valueDiff + 1;

        for(int i=0;i<nums.length;i++)
        {
            long normalizedNumber = (long)nums[i] - Integer.MIN_VALUE;

            long bucketId = normalizedNumber/bucketSize;

            if(bucket.containsKey(bucketId)) return true;

            if(bucket.containsKey(bucketId - 1) && normalizedNumber - bucket.get(bucketId-1) <= valueDiff) return true;

            if(bucket.containsKey(bucketId + 1) && bucket.get(bucketId + 1) - normalizedNumber <= valueDiff) return true;

            // Maintain map to be size indexDiff

            if(bucket.size() >= indexDiff)
            {
                long outdatedBucket = ((long)nums[i-indexDiff] - Integer.MIN_VALUE) / bucketSize;
                bucket.remove(outdatedBucket);
            }
            bucket.put(bucketId,normalizedNumber);
        }
        return false;
    }
}
