package DataModel;

public class TreeNode
{
    public int val;
    public TreeNode left;
    public TreeNode right;
    public TreeNode next; // Just added here for the adjacent nodes question
    public TreeNode() {}
    public TreeNode(int val)
    {
        this.val = val;
    }
    public TreeNode(int val, TreeNode left, TreeNode right)
    {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
