package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

public class SumOfSubarrayMinimums_907_M_STACK
{
    /*
    * https://leetcode.com/problems/sum-of-subarray-minimums/
    * */

    /*
    * */

    /*
    * We want the min of every contiguous subarray of arr, then sum them up
    * What this means is we want to track the minimum at each step of the way
    * For a normal min finding problem with a window size, I would normally use Sliding Window as it is easier to implement
    * But since we want every single contiguous subarray, we need a different approach: Monotone Stack
    *
    * Monotone Stack: A stack that is monotonically increasing/decreasing
    *
    * e.g. if a Mono-Decreasing Stack has [5,4,2,1] and we want to push in a 3
    * We would first want to pop every value that is less than 3 and then push in 3
    * Where we would then end up with a result of [5,4,3] in our Mono-Decreasing Stack
    *
    * */

    /*
    * Idea here is to go through every single element in the array
    * Find every single subarray where they are the minimum
    * Multiply that count by the minimum and add it to the total sum
    *
    * In order to find all the subarrays where a number is the minimum
    * We need to know the previous element that is smaller and the next element that is smaller
    * Since those 2 values would make the current value no longer the min
    *
    *
    * */

    public int sumSubarrayMins(int[] arr)
    {
        // problem tells us to return answer % (10^9 + 7) to prevent overflow of integer
        // thus declaring modulo variable
        long modulo=(int)1e9+7;

        long sum=0;

        // Since we want the minimum, we should use a mono-increasing stack
        Deque<Integer> stack = new ArrayDeque<>();

        // Since we need to find previous smaller element and next smaller element to generate our subarrays for each value
        // We need to track those data somewhere, thus we will create two arrays

        // previous smaller index will store index of previous smaller value compared to arr[i]
        int[] previousSmallerIndex = new int[arr.length];
        // next smaller index will store index of the next smaller value compared to arr[i]
        int[] nextSmallerIndex = new int[arr.length];

        // We need to fill our arrays for elements where they do not have next smaller elements
        Arrays.fill(nextSmallerIndex, arr.length);

        for(int i=0;i<arr.length;i++)
        {
            int currentValue = arr[i];

            // This loop is the generic Monotone Stack check that ensures we are always monotonously increasing
            // But it also helps us generate our Next Smaller Values
            while(!stack.isEmpty() && currentValue <= arr[stack.peekLast()])
            {
                // knowing current value < stack.peek
                // stack.peek's next smaller value is current value's index
                int index = stack.pollLast();

                // We know i stores the next smaller value
                nextSmallerIndex[index] = i;
            }

            // Now that we are here, it means our current value is for sure bigger than stack.peek
            // Therefore, we will assign our previous smaller element to stack.peek

            // If stack is currently empty, it's previous smaller element will be -1 for now
            previousSmallerIndex[i] = stack.isEmpty()?-1:stack.peekLast();

            stack.offer(i);
        }

        for(int i=0;i<arr.length;i++)
        {
            long leftBoundary  = i - previousSmallerIndex[i];
            long rightBoundary = nextSmallerIndex[i] - i;

            sum += arr[i] * leftBoundary * rightBoundary;
            sum%=modulo;
        }
        return (int)sum;
    }
}
