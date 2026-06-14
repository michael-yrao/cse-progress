package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

public class ConvertSortedArrayToBST_108_E_TREE
{
    /*
    * https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/
    * */


    /*
     * Sorted array is inorder traversal of a BST
     * So let's assume middle element is the root
     *
     * Knowing middle element is root. We can apply the same to the left of middle and same to the right of middle recursively
     *
     * */

    public TreeNode sortedArrayToBST(int[] nums)
    {
        return bstConstruct(nums, 0, nums.length-1);
    }

    public TreeNode bstConstruct(int[] nums, int leftIndex, int rightIndex)
    {
        // base case
        if(leftIndex>rightIndex) return null;

        int middleIndex = (leftIndex+rightIndex)/2;
        TreeNode root = new TreeNode(nums[middleIndex]);
        root.left = bstConstruct(nums, leftIndex, middleIndex-1);
        root.right = bstConstruct(nums, middleIndex+1, rightIndex);
        return root;
    }
}
