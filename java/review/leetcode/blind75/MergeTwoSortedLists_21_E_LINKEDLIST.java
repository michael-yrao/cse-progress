package review.leetcode.blind75;

import DataModel.ListNode;

public class MergeTwoSortedLists_21_E_LINKEDLIST
{
    /*
    * https://leetcode.com/problems/merge-two-sorted-lists/
    * */

    public ListNode mergeTwoLists(ListNode list1, ListNode list2)
    {
        final ListNode head = new ListNode(); // Dummy node
        ListNode traversal = head; // Will use this node to create the return list

        while(list1!=null && list2!=null)
        {
            if(list1.val < list2.val)
            {
                traversal.next = list1;
                list1 = list1.next;
            }
            else
            {
                traversal.next = list2;
                list2 = list2.next;
            }
            traversal = traversal.next;
        }

        // Since we only covered cases up to both list1 and list2 are same length
        // We need to add the rest to the end of traversal based on whichever is longer
        // Whichever one is longer will be non-null

        traversal.next = (list1 == null)?list2:list1;

        return head.next;
    }
}
