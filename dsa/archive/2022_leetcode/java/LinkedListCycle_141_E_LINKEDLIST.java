package review.leetcode.blind75;

import DataModel.ListNode;

public class LinkedListCycle_141_E_LINKEDLIST
{
    /*
    * https://leetcode.com/problems/linked-list-cycle/
    * */

    public boolean hasCycle(ListNode head)
    {
        if(head==null) return false;
        ListNode fast = head;
        ListNode slow = head;

        while(fast!=null && fast.next!=null)
        {
            slow = slow.next;
            fast = fast.next.next;
            if(slow==fast) return true;
        }
        return false;
    }

}
