package review.leetcode.blind75;

import DataModel.ListNode;

public class ReverseLinkedList_206_E_LINKEDLIST
{
    /*
    * https://leetcode.com/problems/reverse-linked-list/
    * */

    public ListNode reverseList(ListNode head)
    {
        ListNode previous=head;
        ListNode next=head;
        ListNode current=head;

        while(current!=null)
        {
            next = current.next;
            current.next = previous;
            previous = current;
            current = next;
        }
        if(head!=null) head.next = null;
        head=previous;
        return head;
    }
}
