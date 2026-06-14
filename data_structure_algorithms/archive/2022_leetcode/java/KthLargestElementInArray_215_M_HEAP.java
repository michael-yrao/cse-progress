package review.leetcode.leetcodeExtra;

import java.util.Collections;
import java.util.PriorityQueue;

public class KthLargestElementInArray_215_M_HEAP
{
    /*
    * https://leetcode.com/problems/kth-largest-element-in-an-array/
    * */

    /*
    * Input: nums = [3,2,1,5,6,4], k = 2
    * Output: 5
    * */

    // First obvious way to look at this is to just sort nums and go through from right to left for the kth value
    // This solution gives O(nlogn) due to sorting
    // An easier method is put all the numbers into a max heap
    // Remove from the max heap k times

    public int findKthLargestMaxHeap(int[] nums, int k)
    {
        // Java PQ is constructed as a Min Heap by default
        // Below are a few ways to create a max heap
        // We will use the reverseOrder one since that is the most readable

        // PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a,b) -> (b-a));
        // PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a,b) -> b.compareTo(a));

        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

        for(Integer x : nums)
        {
            maxHeap.offer(x);
        }

        int count=0;
        while(count++<k-1)
        {
            maxHeap.poll();
        }
        Integer peek = maxHeap.peek();
        return peek;
    }

    public int findKthLargestMinHeap(int[] nums, int k)
    {
        // Using a min heap, we can solve this problem in 1 single loop
        // Keep min heap the size of k
        // If we poll all numbers until we have only size k, that means the kth element is the smallest
        // Which means we can grab it just by peeking at the top of the heap

        PriorityQueue<Integer> minHeap = new PriorityQueue<>();

        for(Integer x : nums)
        {
            minHeap.offer(x);
            if(minHeap.size() > k)
            {
                minHeap.poll();
            }
        }
        return minHeap.peek();
    }

}
