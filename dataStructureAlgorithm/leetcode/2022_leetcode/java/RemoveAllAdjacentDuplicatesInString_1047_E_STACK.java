package review.leetcode.leetcodeExtra;

import java.util.Stack;

public class RemoveAllAdjacentDuplicatesInString_1047_E_STACK
{
    /*
    * https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/
    * */

    public String removeDuplicates(String s)
    {
        if(s == null || s.length()==0) return s;

        Stack<Character> stack = new Stack<>();

        stack.push(s.charAt(0));

        for(int i=1;i<s.length();i++)
        {
            // If charAt(i) == stack.peek, it means we have a duplicate. Remove the duplicate by popping from the stack
            if(!stack.isEmpty() && s.charAt(i)==stack.peek()) stack.pop();
            // If it is not a duplicate, add to the stack
            else stack.push(s.charAt(i));
        }

        StringBuilder sb = new StringBuilder();

        while(!stack.isEmpty()) sb.append(stack.pop());

        return sb.reverse().toString();
    }
}
