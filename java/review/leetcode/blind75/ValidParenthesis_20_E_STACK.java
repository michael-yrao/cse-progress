package review.leetcode.blind75;

import java.util.Stack;

public class ValidParenthesis_20_E_STACK
{
    /*
    * https://leetcode.com/problems/valid-parentheses/
    * */

    public boolean isValidParenthesis(String s)
    {
        Stack<Character> stack = new Stack<>();
        if(s.length()%2!=0) return false;
        for(int i=0;i<s.length();i++)
        {
            if(s.charAt(i)=='(' || s.charAt(i)=='[' || s.charAt(i)=='{') stack.push(s.charAt(i));
            else if(s.charAt(i)==')' && !stack.isEmpty() && stack.peek() == '(') stack.pop();
            else if(s.charAt(i)==']' && !stack.isEmpty() && stack.peek() == '[') stack.pop();
            else if(s.charAt(i)=='}' && !stack.isEmpty() && stack.peek() == '{') stack.pop();
            else return false;
        }
        return stack.isEmpty();
    }
}
