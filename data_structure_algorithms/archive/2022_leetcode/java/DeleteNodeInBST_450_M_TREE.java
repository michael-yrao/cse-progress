package review.leetcode.blind75;

import DataModel.TreeNode;

public class DeleteNodeInBST_450_M_TREE
{
    /*
    * https://leetcode.com/problems/delete-node-in-a-bst/
    * */

    /*
     * First we need to find the node
     * We need a reference of the node's parent
     * We also need a reference of the node's children
     *
     * Cases:
     *   1. Deleting a Leaf -> Remove it from the tree, parent's left/right = null
     *   2. Deleting node with 1 child -> replace node with its child, parent's left/right = child
     *   3. Deleting node with 2 child -> Use inorder traversal on the right side to get smallest right value to replace node with.
     * */

    public TreeNode deleteNode(TreeNode root,int key)
    {
        if(root==null || (isLeaf(root) && root.val == key)) return null;

        // Go left is key is smaller
        if(key < root.val) root.left = deleteNode(root.left, key);
        // Go right if key is greater
        else if(key > root.val) root.right = deleteNode(root.right, key);
        // Found the node with val=key
        else
        {
            // Case #1: node to be deleted is leaf

            if(isLeaf(root)) return null;

            // Case #2: Node to be deleted has 1 child

            else if((root.left!=null&&root.right==null)
                    ||(root.left==null&&root.right!=null))
            {
                root= (root.left==null)?root.right:root.left;
            }

            // Case #3: Node to be deleted has 2 child

            else
            {
                // Replace the curent node with the replacement's value

                TreeNode biggestLeftChild = maxValueBST(root.left);
                root.val = biggestLeftChild.val;

                // Recursively get rid of that replacement node

                root.left = deleteNode(root.left, biggestLeftChild.val);
            }
        }
        return root;
    }



    public TreeNode deleteNodeMethod2(TreeNode root, int key)
    {
        if(root==null || (isLeaf(root) && root.val == key)) return null;

        TreeNode currentNode = root; // Current Node
        TreeNode parent = null;      // Parent of current node (root's parent is null)

        // Look for the parent node of our node with value=key
        // The way we structured this loop means
        // We will have parent in our parent Node, we will also have our node with value=key in currentNode

        while(currentNode!=null && currentNode.val!=key)
        {
            parent = currentNode;
            if(key < currentNode.val) currentNode = currentNode.left;
            else currentNode = currentNode.right;
        }

        // If we didn't find the value, that means this value doesn't exist in our BST
        // Thus just return original Tree

        if(currentNode==null) return root;

        // If we did find the node, let's check our cases

        // Case #1: Leaf Node

        if(isLeaf(currentNode))
        {
            if(parent!=null)
            {
                if(parent.left==currentNode) parent.left = null;
                else parent.right = null;
            }
        }

        // Case #2: 1 Node Child

        else if((currentNode.left==null && currentNode.right!=null)
                || (currentNode.left!=null && currentNode.right==null))
        {
            TreeNode child = (currentNode.left==null)?currentNode.right:currentNode.left;

            // If current node is the root, we would want to replace root with child

            if(currentNode==root) root=child;
            else
            {

            // Otherwise assign similar to Case #1

                if(parent.left==currentNode) parent.left = child;
                else parent.right = child;
            }
        }

        // Case #3: 2 Node Child

        else
        {
            TreeNode smallestRightNode = minValueBST(currentNode.right);
            int value = smallestRightNode.val;

            deleteNodeMethod2(root,value);

            currentNode.val = value;
        }
        return root;
    }

    private TreeNode minValueBST(TreeNode node)
    {
        while(node.left!=null) node=node.left;
        return node;
    }

    private TreeNode maxValueBST(TreeNode node)
    {
        while(node.right!=null) node=node.right;
        return node;
    }

    private boolean isLeaf(TreeNode node)
    {
        return node.left==null && node.right==null;
    }

}
