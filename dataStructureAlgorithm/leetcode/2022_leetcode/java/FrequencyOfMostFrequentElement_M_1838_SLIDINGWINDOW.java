package review.leetcode.leetcodeExtra;

public class FrequencyOfMostFrequentElement_M_1838_SLIDINGWINDOW
{
    /*
    * https://leetcode.com/problems/frequency-of-the-most-frequent-element/
    * */

    /*
    * This problem is actually a bit tricky to see how to do.
    * First we should note that we kind of need the array in an order that we can make some sense out of,
    * otherwise we would just do a trivial solution of O(n^2).
    *
    * Second, notice that we can only increment 1 through k positively and not downwards,
    * thus this means the larger values have some interesting impact on our solution and maybe we can try sorting first
    *
    *
    *
    * */

    public int maxFrequency(int[] nums, int k)
    {
        return -1;
    }
}
