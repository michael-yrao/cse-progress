package review.leetcode.leetcodeExtra;

import DataStructure.Pair;

import java.util.Stack;

public class RemoveAllAdjacentDuplicatesInStringII_1209_M_STACK
{
    /*
    * https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/
    * */

    /*
    * Same idea as the first remove all adjacent problem
    * However, since we have k instead of just duplicate, it means that we can't just use a stack like how we did it last time
    * What we can try is keeping a counter while we are performing the stack pop
    *
    * With the above idea, what we should do is actually use a Stack of Pairs where Pair consist of <Value, Counter>
    *
    * If the next char is same as peek, increment count
    * If the next char is same as peek but count exceeds k, pop
    * If the next char is not same as peak, push it to the stack with count 1
    *
    * Construct string with rest of stack and return
    *
    * */

    public String removeDuplicates(String s, int k)
    {
        Stack<Pair<Character,Integer>> stack = new Stack<>();

        for(int i=0;i<s.length();i++)
        {
            if(!stack.isEmpty() && stack.peek().x == s.charAt(i))
            {
                if(stack.peek().y+1 == k) stack.pop();
                else stack.peek().y++;
            }
            else
            {
                stack.push(new Pair<Character,Integer>(s.charAt(i),1));
            }
        }

        StringBuilder sb = new StringBuilder();

        while(!stack.isEmpty())
        {
            if(stack.peek().y==1) sb.append(stack.pop().x);
            else
            {
                sb.append(stack.peek().x);
                stack.peek().y--;
            }
        }

        return sb.reverse().toString();
    }
}
