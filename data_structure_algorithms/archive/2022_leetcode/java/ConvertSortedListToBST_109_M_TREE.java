package review.leetcode.leetcodeExtra;

import DataModel.ListNode;
import DataModel.TreeNode;

public class ConvertSortedListToBST_109_M_TREE
{
    /*
    * https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/
    * */


    /*
    * preorder = root -> left -> right
    * inorder = left -> root -> right
    *
    * Use inorder for BST, middle element is the root
    * Issue here is getting the middle of the List every time can be quite time-consuming
    * We can actually use the tortoise and hare algorithm to always get the middle node each time
    *
    * From here, we can do some type of binary search
    * Instead of using left and right, we will need to leverage middle a bit more
    * For left half, we can do head -> middle. From right side, we can do middle -> null
    *
    * Using Tortoise and Hare Algorithm is actually very time consuming and doesn't seem to get accepted by LC
    *
    * Think we can just iterate through the list and get the length of the list instead
    * Then just use the list length as a way to get middle and increment a counter as needed
    *
    * */

    ListNode globalCounter;

    public TreeNode sortedListToBST(ListNode head)
    {
        int listSize = getLengthOfList(head);
        globalCounter = head;
        return convertToBST(head,0,listSize);
    }

    public TreeNode convertToBST(ListNode head, int left, int right)
    {
        if(left>right) return null;
        int mid = (left+right)/2;
        TreeNode leftNode = convertToBST(head, left, mid-1);
        TreeNode root = new TreeNode(globalCounter.val);
        globalCounter = globalCounter.next;
        TreeNode rightNode = convertToBST(head, mid+1, right);
        root.left = leftNode;
        root.right = rightNode;
        return root;
    }

    public int getLengthOfList(ListNode head)
    {
        int counter=0;
        ListNode cursor = head;
        while(cursor!=null)
        {
            cursor=cursor.next;
            counter++;
        }
        return counter;
    }
}
