package review.leetcode.leetcodeExtra;

public class SingleNumber_136_E_BITS
{
    /*
    * https://leetcode.com/problems/single-number/
    * */

    /*
    * Key things here to note is
    *   1. We must do this with O(1) memory
    *   2. We can manipulate the answer using XOR
    *       a. 0 XOR A = A
    *       b. A XOR A = 0       (even = 0)
     *      c. A XOR A XOR A = A (odd  = A)
    *       d. A XOR B XOR A = B
    *
    * What this means is we can start our answer initialized as 0 and just run XOR til end of the array
    *
    * */

    public int singleNumber(int[] nums)
    {
        int answer=0;
        for(Integer x : nums)
        {
            answer^=x;
        }
        return answer;
    }
}
