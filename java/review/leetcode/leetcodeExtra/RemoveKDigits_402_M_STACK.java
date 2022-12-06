package review.leetcode.leetcodeExtra;

import java.util.ArrayDeque;
import java.util.Deque;

public class RemoveKDigits_402_M_STACK
{
    /*
    * https://leetcode.com/problems/remove-k-digits/
    * */

    /*
    * We want to remove k elements and return the smallest values we can get from this removal
    *
    * Monotone Stack Algorithm
    *
    * */

    /*
    * First thought is we should always try to remove the largest digits
    * If there are more than one largest digit, we want to remove the left (e.g. 9119, k=1. we would want to remove the first 9)
    *
    * Since we want the smallest value/subsequence we can get out of this, we want a mono-increasing stack
    *
    * */

    public String removeKdigits(String num, int k)
    {
        // This is a double-sided stack, so can be treated as a stack or queue
        // We are using this as a stack, so naming it as such
        Deque<Integer> stack = new ArrayDeque<>();

        for(int i=0;i<num.length();i++)
        {
            // Go through each value of the input String
            int currentValue = num.charAt(i) - '0';

            // We want to look at the top of the stack
            // Make sure our current value is INCREASING, e.g. >= stack.getLast()
            // If it's not greater, then we need to pop from stack until it is greater or until we reach k removals

            // Perform pop while current value < stack.getLast()
            // Since we are using a double-sided stack, peek defaults to Queue's peek, so we need to use getLast()
            while(!stack.isEmpty() && currentValue < stack.getLast() && k > 0)
            {
                // Since we are popping here, we need to decrement our k
                k--;
                stack.pollLast();
            }
            stack.offer(currentValue);
        }

        // Now that we are here, we are pretty much done
        // BUT we need to consider edge values such as when all the values in num are the same
        // e.g. num = "11111111", which would result in us removing absolutely nothing from our while loop above
        // In this case, we would want to remove the last k digits from our stack

        while(k>0 && !stack.isEmpty())
        {
            stack.pollLast();
            k--;
        }

        // Now we are truly done and we just want to convert our stack into a string for return

        StringBuilder sb = new StringBuilder();

        // Since we are using a double-sided stack, we can just use poll to read from beginning to end like a queue
        while(!stack.isEmpty())
        {
            sb.append(stack.pollFirst());
        }

        // Remember to remove all leading 0s in edge cases
        // e.g. input = 10200, k = 1 : result = 200. We need to remove the leading 0 to get 200

        while(sb.length()>1 && sb.charAt(0)=='0') sb.deleteCharAt(0);

        return sb.toString();
    }
}
