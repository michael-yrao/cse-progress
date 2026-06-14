package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.ArrayList;
import java.util.List;

public class TimeBasedKeyValueStore_981_M_BINARYSEARCH_TODO
{
    /*
    * https://leetcode.com/problems/time-based-key-value-store/
    * */

    class TimeMap
    {

        /*
        * Initial thought was to do a Heap but we need to be able to access every element of the Heap, so Heap is out
        * We can try to do a ArrayList where the index is the timestamp and the value stored at the ArrayList is the Map
        *
        * */

        List<Pair<String,String>> timeMap;

        public TimeMap()
        {
            timeMap = new ArrayList<>();
            timeMap.add(0, null);
        }

        public void set(String key, String value, int timestamp)
        {
            // In the case that we get an input timestamp that is repeated, we need to ensure current element is not overridden
            if(timeMap.size() >= timestamp && timeMap.get(timestamp) != null) return;

            timeMap.add(timestamp,new Pair<String,String>(key,value));
        }

        public String get(String key, int timestamp)
        {
            /*
            * Need to find closest timestamp <= input timestamp if input timestamp doesn't exist
            *
            * Since we are actually just looking at index, we can just use a modified binary search
            *
            * */

            if(timeMap.size() >= timestamp && timeMap.get(timestamp) != null) return timeMap.get(timestamp).y;

            int left=0, right=timeMap.size();
            // We wil assume timestamp is the target, but we actually want closest value to timestamp that is less than timestamp

            while(right>left)
            {
                int middle = (left+right)/2;
                if(middle==timestamp)
                {
                    if(timeMap.get(middle-1) != null) return timeMap.get(timestamp-1).y;
                    right = middle-1;
                    timestamp = middle-1;
                }
                else if(middle<timestamp) left=middle;
                else right=middle;
            }
            return "";
        }
    }
}
