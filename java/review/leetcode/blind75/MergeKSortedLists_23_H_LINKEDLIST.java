package review.leetcode.blind75;

import DataModel.ListNode;

import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Queue;

public class MergeKSortedLists_23_H_LINKEDLIST
{
    /*
    * https://leetcode.com/problems/merge-k-sorted-lists/
    * */

    public ListNode mergeKLists(ListNode[] lists)
    {
        // Easiest way to implement this is probably just use a Min Heap
        // Put everything from lists into a Min Heap
        // Create a new list and poll from heap until heap is empty

        Queue<Integer> minHeap = new PriorityQueue<>();

        for(ListNode node : lists)
        {
            ListNode current = node;
            while(current!=null)
            {
                minHeap.offer(current.val);
                current = current.next;
            }
        }

        final ListNode returnNode = new ListNode();
        ListNode traversal = returnNode;

        while(!minHeap.isEmpty())
        {
            traversal.next = new ListNode(minHeap.poll());
            traversal = traversal.next;
        }
        return returnNode.next;
    }

    // One way to do this is to do 2 at a time similar to Merge Sort
    // Not sure if this is the most efficient method but we should implement it anyways for practice

    public ListNode mergeKListsMergeSort(ListNode[] lists)
    {
        if(lists == null || lists.length == 0) return null;

        List<ListNode> mergedList = new ArrayList<>();

        while(lists.length>1)
        {
            for(int i=0;i<lists.length;i+=2)
            {
                ListNode list1 = lists[i];
                ListNode list2 = null;
                if(i+1 < lists.length) list2 = lists[i+1];
                mergedList.add(mergeTwoList(list1,list2));
            }
            lists = mergedList.toArray(new ListNode[mergedList.size()]);
        }
        return lists[0];
    }

    public ListNode mergeTwoList(ListNode list1, ListNode list2)
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
