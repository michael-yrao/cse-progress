package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

public class FlattenBinaryTreeToLinkedList_114_M_LINKEDLIST_TODO
{
    /*
    * https://leetcode.com/problems/flatten-binary-tree-to-linked-list/
    * */

    /*
    * Idea here is to create a Queue of the TreeNodes in preorder traversal
    * Remove reference of left sub-tree from root so garbage collector can pick it up
    * Then run down the Queue and link the root to queue.pop()
    *
    * */

    public void flatten(TreeNode root)
    {

    }
}
