package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.*;

public class MergeIntervals_56_M_INTERVALS
{
    /*
    * https://leetcode.com/problems/merge-intervals/
    * */


    /*
    * So key here is to identify whether or not two intervals are overlapping
    * One thing it seems we can do is start[i-1] < start[i] && end[i-1] >= start[i]
    * This relies on the fact that the array is sorted by start time, which it seems to be the case in the problem
    *
    * But to ensure this is the case, what we should do is convert these intervals to Pairs and use a minHeap based on start time
    * */

    public int[][] mergeIntervals(int[][] intervals)
    {
        // Sort by start value
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

        // Create the result list, we'll use an arraylist of int[] since we don't know end size
        ArrayList<int[]> ans = new ArrayList<>();

        // We'll insert the first interval into the result first so we can use it as a base for the rest of our intervals
        ans.add(new int[]{intervals[0][0],intervals[0][1]});

        for(int i=1;i<intervals.length;i++)
        {
            int prevStart = ans.get(ans.size()-1)[0];
            int prevEnd = ans.get(ans.size()-1)[1];
            int currentStart = intervals[i][0];
            int currentEnd = intervals[i][1];

            // Don't need to compare starting since we are sorted
            if(currentStart <= prevEnd)
            {
                // Given intervals [1,5] and [2,4]
                // We need to take the max of these two ends and not just the current end time
                int[] newInterval = new int[]{prevStart,Math.max(prevEnd,currentEnd)};
                ans.remove(ans.size()-1);
                ans.add(newInterval);
            }
            else ans.add(new int[]{intervals[i][0], intervals[i][1]});
        }
        int[][] result = new int[ans.size()][2];
        ans.toArray(result);
        return result;
    }

    public int[][] mergeSecondSubmission(int[][] intervals)
    {
        /*

        We always need a base line interval in our final list, so we should insert the first interval in regardless

        One thing to note here is that this must be sorted using start time in order to properly compare

        From here, we can check the logic..

        Requiring Merging:

            first=[1,3]
            second=[2,6]

            first[end] >= second[start]

        */

        Arrays.sort(intervals, (a,b) -> (a[0] - b[0]));

        List<int[]> result = new ArrayList<>();

        result.add(intervals[0]);

        for(int i=1;i<intervals.length;i++)
        {
            int prevStart = result.get(result.size()-1)[0];
            int prevEnd = result.get(result.size()-1)[1];
            int currentStart = intervals[i][0];
            int currentEnd = intervals[i][1];

            if(prevEnd >= currentStart) result.get(result.size()-1)[1] = Math.max(prevEnd,currentEnd);
            else result.add(intervals[i]);
        }
        int[][] resultArray = new int[result.size()][2];
        result.toArray(resultArray);
        return resultArray;
    }
}
