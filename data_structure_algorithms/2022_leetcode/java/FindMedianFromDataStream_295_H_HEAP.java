package review.leetcode.blind75;

import java.util.PriorityQueue;

public class FindMedianFromDataStream_295_H_HEAP
{
    /*
    * https://leetcode.com/problems/find-median-from-data-stream/
    * */

    /*
    * Design a Data Structure that finds the median value efficiently
    * Median: 1,2,3,4,5,6,7,8,9,10 <- 5.5
    * Median: 1,2,3,4,5,6,7,8,100  <- 5
    * */

    public class MedianFinder {


        // Use a maxHeap to store the smaller values
        // Use a minHeap to store the bigger values

        PriorityQueue<Integer> bigMinHeap;
        PriorityQueue<Integer> smallMaxHeap;

        public MedianFinder()
        {
            bigMinHeap = new PriorityQueue<>();
            smallMaxHeap = new PriorityQueue<>((a,b)->(b-a));
        }

        public void addNum(int num)
        {
            // Add first number to whichever heap
            // If the size of two heaps differ by more than 1
            // Move the bigger heap's biggest/smallest number to the other heap

            // For our example, we will just by default add to the smallMaxHeap
            // If our small Max Heap has 2 digits while the big Min Heap has 0
            // We will give the largest value from our Max Heap to our Min Heap

            smallMaxHeap.add(num);

            // If the size of the two heaps differ by more than 1, move the biggest value from maxheap to minheap

            if(smallMaxHeap.size()-bigMinHeap.size()>1)
            {
                bigMinHeap.offer(smallMaxHeap.poll());
            }

            // If the largest value in maxheap is smaller than smallest value of minheap, swap them

            if(smallMaxHeap.size() > 0
                    && bigMinHeap.size() > 0
                    && smallMaxHeap.peek() > bigMinHeap.peek())
            {
                int bigValue = bigMinHeap.poll();
                bigMinHeap.offer(smallMaxHeap.poll());
                smallMaxHeap.offer(bigValue);
            }
        }

        public double findMedian()
        {
            if(bigMinHeap.size() == smallMaxHeap.size())
                return (double) (bigMinHeap.peek() + smallMaxHeap.peek()) / 2;
            else
            {
                if(bigMinHeap.size()>smallMaxHeap.size()) return (double)bigMinHeap.peek();
                else return (double)smallMaxHeap.peek();
            }
        }
    }

}
