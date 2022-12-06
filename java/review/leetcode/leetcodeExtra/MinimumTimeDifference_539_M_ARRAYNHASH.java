package review.leetcode.leetcodeExtra;

import java.util.Arrays;
import java.util.List;

public class MinimumTimeDifference_539_M_ARRAYNHASH
{
    /*
    * https://leetcode.com/problems/minimum-time-difference/
    * */


    /*
    * 1. Convert the Strings to something a bit more easily comparable, maybe integers
    * 2. At this point, we can treat this as a regular Closest Pair of Points Problem
    * 3. The most efficient algorithms to solve these is O(nlogn)
    *
    * One tricky thing here is we need to realize that 23:59 and 00:00 are extremely close to each other
    * Thus we need to watch out for the special case here, thus after we do the normal closest pair solution,
    * make sure to check first element against last element
    *
    * */
    public int findMinDifference(List<String> timePoints)
    {
        int minDifference = Integer.MAX_VALUE;
        int[] convertedTime = new int[timePoints.size()];
        for(int i=0;i<timePoints.size();i++)
        {
            convertedTime[i] = convertTimeToInt(timePoints.get(i));
        }

        Arrays.sort(convertedTime);

        for(int i=1;i<convertedTime.length;i++)
        {
            minDifference = Math.min(minDifference, convertedTime[i] - convertedTime[i-1]);
        }

        // Check between first and last element since they can be closest (00:01 and 23:59)
        // We can convert one or the other to the other format, e.g. get 23:59 as close to 00:01 as possible by doing 24:00 - 23:59
        // Or we can do 00:01 + 24:00 compared to 23:59, whichever you prefer

        return Math.min(minDifference,(convertedTime[0] + 24 * 60) - convertedTime[convertedTime.length-1]);
    }

    private int convertTimeToInt(String time)
    {
        String[] timeSplit = time.split(":");
        if(timeSplit.length!=2) return Integer.MIN_VALUE;
        return (Integer.parseInt(timeSplit[0]) * 60) + Integer.parseInt(timeSplit[1]);
    }
}
