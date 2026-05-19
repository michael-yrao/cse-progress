package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.ArrayDeque;
import java.util.Deque;

public class LargestRectangleInHistogram_84_H_STACK
{
    /*
    * https://leetcode.com/problems/largest-rectangle-in-histogram/
    * */

    public int largestRectangleArea(int[] heights)
    {
        /*
        * Mono-Increasing Stack
        *
        * 1. We want to push in a Pair of Index,Height into the Mono-Increasing Stack, increasing based on the height
        * 2. We want to push in the currentIndex, height into the stack if we are not popping from the stack
        * 3. However, if we need to pop from the Stack:
        *    a. Calculate max area of each value popped
        *    b. Populate index with the last stack.pop() that is > current height
        * 4. Once we finish adding values to the mono-increasing stack, calculate max in the values left in the stack
        *    a. We can use the same calculation logic we use for step 3a
        * */

        // Max Area to be updated each time we perform max area calculation
        int maxArea = 0;

        // Stack will hold Pair of Index:Height, this will be a Mono-Increasing Stack
        Deque<Pair<Integer,Integer>> stack = new ArrayDeque<>();

        for(int i=0;i<heights.length;i++)
        {
            // Start Index is used to assign the index of our Pairs in our Stack if we are to pop
            int startIndex = i;
            int currentHeight = heights[i];
            while(!stack.isEmpty() && currentHeight < stack.getLast().y)
            {
                Pair<Integer,Integer> pair = stack.pollLast();
                int index = pair.x;
                int height = pair.y;
                // Update Max Area to Height * Width
                maxArea = Math.max(maxArea, height * (i-index));
                startIndex = index;
            }
            stack.offer(new Pair(startIndex, currentHeight));
        }

        // Perform the same max area calculation on rest of the Stack
        while(!stack.isEmpty())
        {
            Pair<Integer,Integer> pair = stack.pollLast();
            int index = pair.x;
            int height = pair.y;
            // Since we already iterated through the entire array
            // We can get the width by doing size of the array - index of the value
            maxArea = Math.max(maxArea,height * (heights.length - index));
        }
        return maxArea;
    }
}
