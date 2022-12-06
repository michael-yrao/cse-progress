package review.leetcode.leetcodeExtra;

import java.util.ArrayDeque;
import java.util.Deque;

public class DecodeString_394_M_STACK
{
    /*
    * https://leetcode.com/problems/decode-string/
    * */


    /*
    Input: s = "3[a]2[bc]"
    Output: "aaabcbc"

    Input: s = "3[a2[c]]"
    Output: "accaccacc"

     */

    /*
    * This problem seems like it would benefit a lot from using a Stack
    *   1. Traverse through the list until we hit the first ]
    *   2. From there, we want to use a while loop to poll until we hit a [ to generate the String to be duplicated
    * */

    public String decodeString(String s)
    {
        Deque<Character> characterStack = new ArrayDeque<>();
        Deque<Integer> countStack = new ArrayDeque<>();
        return null;
    }
}
