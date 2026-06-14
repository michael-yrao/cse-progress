package review.leetcode.leetcodeExtra;

import DataModel.ListNode;

public class AddTwoNumbers_2_M_LINKEDLIST
{
    /*
    * https://leetcode.com/problems/add-two-numbers/
    * */

    public ListNode addTwoNumbers(ListNode l1, ListNode l2)
    {
        /*
        * Numbers are stored in reverse order in the Linked Lists
        * Kinda works in our favor since for addition, we add from smallest digit place to largest (e.g. 10^0 -> 10^1, etc)
        * */

        ListNode dummyNode = new ListNode();

        ListNode pointer = dummyNode;

        int carry = 0;

        // The carry != 0 condition is needed in situations as below:
        // l1 = 7, l2 = 8 ; Sum = 15
        // We create a 5 with our logic but since there was only 1 node in each, we left out the 1 carry
        // Thus we need to add the carry != 0 condition in order to make sure the carry is added if it makes a new node

        while(l1 != null || l2 != null || carry != 0)
        {
            int l1Adder = (l1==null)?0:l1.val;
            int l2Adder = (l2==null)?0:l2.val;

            // Calculate new node to be inserted to the result list

            // Addition logic: a + b + carry from prior digit calculation
            int resultAmount = l1Adder + l2Adder + carry;

            // Calculate new carry if there are any. e.g. if resultAmount > 9, that means we got a carry
            // Therefore, we should do resultAmount/10 for carry
            carry = resultAmount/10;

            // Make sure our resultAmount is single digit

            resultAmount%=10;

            pointer.next = new ListNode(resultAmount);

            // Increment our pointers

            pointer = pointer.next;
            l1=(l1==null)?null:l1.next;
            l2=(l2==null)?null:l2.next;
        }
        return dummyNode.next;
    }
}
