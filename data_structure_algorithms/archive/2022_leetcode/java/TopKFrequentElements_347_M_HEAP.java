package review.leetcode.blind75;

import java.util.*;

public class TopKFrequentElements_347_M_HEAP
{
    /*
    * https://leetcode.com/problems/top-k-frequent-elements/
    * */

    // First look at this problem and what I would do is put everything into a HashMap
    // Mapping the element -> frequency
    // Then sort by the values and retrieve top k keys to return
    // The result would be O(nlogn) due to sorting. We can do better

    // Semi-efficient method would be to use a HashMap with Min-Heap
    // Instead of sorting the values, we can use a Min-Heap of size k to remove smallest values each time

    public int[] topKFrequentMinHeapMethod(int[] nums, int k)
    {
        Map<Integer, Integer> freqMap = new HashMap<>();

        for(Integer x : nums)
        {
            freqMap.put(x, freqMap.getOrDefault(x,0)+1);
        }

        // Create a PQ with a Key,Value pair as each Object
        // Java PQ is by default created with Min-Heap
        // So poll will remove smallest value
        // In the constructor here, we are saying to compare and sort by the value in the map
        // Alternatives and older syntax are also mentioned below

        PriorityQueue<Map.Entry<Integer,Integer>> minHeap = new PriorityQueue<>(Comparator.comparingInt(Map.Entry::getValue));

        // With lambda syntax, input parameter (a,b) says use b.getValue()-a.getValue() as comparator
        // However, our comparator here instead b.getValue gets higher priority than a.getValue
        // Thus below implementation is max heap sorted by value in the map
        // MAX HEAP -> PriorityQueue<Map.Entry<Integer, Integer>> maxHeap = new PriorityQueue<>((a,b)->(b.getValue()-a.getValue()));
        // Min heap with the old syntax would be the opposite of Max Heap
        // MIN HEAP -> PriorityQueue<Map.Entry<Integer, Integer>> minHeap = new PriorityQueue<>((a,b)->(a.getValue()-b.getValue()));

        // loop through each unique entry in map
        // if heap gets larger than size k, get rid of the smallest value

        for(Map.Entry x : freqMap.entrySet())
        {
            minHeap.offer(x);
            if(minHeap.size() > k) minHeap.poll();
        }

        // Can't convert minHeap of Entry directly to an array of int, so will need to construct the array with loop

        int[] returnArray = new int[k];

        for(int i=0;i<returnArray.length;i++)
        {
            returnArray[i] = minHeap.poll().getKey();
        }

        return returnArray;

    }

    // Another implementation that is potentially even more efficient is Bucket Sort
    // Given array nums, we know the maximum frequency of any number is nums.length
    // Thus we create a List array of size nums.length
    // Have the Frequency Hashmap as normal
    // Loop through the Entry Set of the HashMap and put data into the List Array
    // Retrieve the top K element starting from end of List Array

    public int[] topKFrequentBucketSortMethod(int[] nums, int k)
    {
        ArrayList<Integer>[] freqArray = new ArrayList[nums.length+1]; // nums.length + 1 size, 0 frequency goes to 0, etc.

        Map<Integer, Integer> freqMap = new HashMap<>();

        for(Integer x : nums)
        {
            freqMap.put(x,freqMap.getOrDefault(x,0)+1);
        }

        for(Map.Entry<Integer,Integer> x : freqMap.entrySet())
        {
            if(freqArray[x.getValue()] == null) freqArray[x.getValue()] = new ArrayList<>();
            freqArray[x.getValue()].add(x.getKey());
        }

        int[] resultArray = new int[k];
        int counter=0;

        for(int i=freqArray.length-1;i>=0;i--)
        {
            if(counter==k) break;
            for(Integer x : freqArray[i])
            {
                resultArray[counter++] = x;
                if(counter==k) return resultArray;
            }
        }
        return null;
    }

}
