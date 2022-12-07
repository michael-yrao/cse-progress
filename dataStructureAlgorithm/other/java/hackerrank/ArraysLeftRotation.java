package review.hackerrank;

import DataStructure.Pair;

import java.util.*;
import java.util.Map.Entry;

public class ArraysLeftRotation
{
    /*
    * https://www.hackerrank.com/challenges/ctci-array-left-rotation/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=arrays
    * */

    /*
     * Complete the 'rotLeft' function below.
     *
     * The function is expected to return an INTEGER_ARRAY.
     * The function accepts following parameters:
     *  1. INTEGER_ARRAY a
     *  2. INTEGER d
     */

    public static List<Integer> rotLeft(List<Integer> list, int shift)
    {
        /*
        * Think we can do modular arithmetic to get proper shifting
        * Current positioning for each element is index%a.size()
        * Since each index is unique anyways, we can just do positioning + d for its new position
        *
        * We might be able to do this in a single loop but not too sure yet
        *
        * 1. Maybe have a minheap of pairs sorted by the new position
        * 2. Loop through once to put the values into the min heap
        * 3. Loop through second time to take values out of heap for result list
        *
        *  */

        PriorityQueue<Pair<Integer,Integer>> minHeap = new PriorityQueue<>(Comparator.comparingInt(a -> a.x));

        for(int i=0;i< list.size();i++)
        {
            int newPosition = ((i+shift) % list.size());
            minHeap.offer(new Pair(newPosition,list.get(i)));
        }

        List<Integer> resultList = new ArrayList<>();

        while(!minHeap.isEmpty())
        {
            resultList.add(minHeap.poll().y);
        }
        return resultList;
    }
}
