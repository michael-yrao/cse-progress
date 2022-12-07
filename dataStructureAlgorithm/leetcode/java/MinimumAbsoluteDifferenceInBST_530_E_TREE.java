package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;

import java.util.ArrayList;
import java.util.List;

public class MinimumAbsoluteDifferenceInBST_530_E_TREE
{
    /*
    * https://leetcode.com/problems/minimum-absolute-difference-in-bst/
    * */


    public int getMinimumDifference(TreeNode root)
    {
        /*
        * We can take advantage of the fact that it is a BST
        * So we can do inorder traversal to get a sorted list out of this tree
        * Then we can work on the sorted list for biggest difference
        * */

        List<Integer> list = new ArrayList<>();
        inorderTraversal(root,list);

        /*
        * Now we are looking for min difference in a sorted list
        * What we want to do is keep a min and a current min
        * We will keep updating the min until we finish the list
        *
        * Technically we can also use something like a two pointer technique
        * e.g. left=0, right=1, shift right until end of list, shift left if curMin > min which is always true
        * So it is kinda unnecessary, we can just start a loop at index 1 and do a[i] - a[i-1]
        * */

        int min = Integer.MAX_VALUE;
        for(int i=1;i<list.size();i++)
        {
            int curMin = list.get(i) - list.get(i-1);
            min = Math.min(min,curMin);
        }
        return min;
    }

    public void inorderTraversal(TreeNode root, List<Integer> list)
    {
        if(root.left!=null) inorderTraversal(root.left,list);
        list.add(root.val);
        if(root.right!=null) inorderTraversal(root.right,list);
    }
}
