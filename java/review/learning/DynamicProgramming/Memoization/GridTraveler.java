package review.learning.DynamicProgramming.Memoization;

import java.util.HashMap;
import java.util.Map;

public class GridTraveler
{
    /*
    * Given a 2D Grid and we start at the top left corner (0,0) and your goal is to travel to the bottom-right
    * You may only move down or right
    * In how many ways can you travel to the goal on a grid with dimensions m * n?
    *
    * Time Complexity of O(m*n)
    *
    * */

    public long gridTraveler(long m, long n)
    {
        if(m==0 || n==0) return 0;
        if(m==n && m==1) return 1;

        return gridTraveler(m-1,n)+gridTraveler(m,n-1);
    }

    /*
    * Time Complexity of O(m+n)
    *
    * */

    public long gridTravelerMemoization(long m, long n)
    {
        // gridTraveler(m,n) = gridTraveler(n,m)

        Map<String,Long> memo = new HashMap<>();
        return gridTravelerMemoizationHelper(m,n,memo);
    }

    public long gridTravelerMemoizationHelper(long m, long n, Map<String,Long> memo)
    {
        String key = m+","+n;
        if(memo.containsKey(key)) return memo.get(key);
        if(m==0 || n==0) return 0;
        if(m==n && m==1) return 1;
        memo.putIfAbsent(key,(gridTravelerMemoizationHelper(m-1,n,memo)+gridTravelerMemoizationHelper(m,n-1,memo)));
        return memo.get(key);
    }

}
