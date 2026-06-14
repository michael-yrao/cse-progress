package review.leetcode.leetcodeExtra;

import DataModel.TreeNode;
import DataStructure.Pair;

import java.util.LinkedList;
import java.util.Queue;

public class HouseRobberIII_337_M_TREE
{
    /*
    * https://leetcode.com/problems/house-robber-iii/
    * */

    /*
    * Idea is to decide at each point whether to include it or not to include root
    * So what we need to do is a DFS while using pairs to keep track of with and without root's values
    * */

    public int rob(TreeNode root)
    {
        Pair<Integer,Integer> pair = dfs(root);
        return Math.max(pair.x,pair.y);
    }

    // We want to return how much we can rob with and without root
    // So x will be with, y will be without
    private Pair<Integer,Integer> dfs(TreeNode root)
    {
        if(root==null) return new Pair<>(0,0);

        Pair<Integer,Integer> leftPair = dfs(root.left);
        Pair<Integer,Integer> rightPair = dfs(root.right);

        // Computing from bottom up
        int withRoot = root.val + leftPair.y + rightPair.y;
        // Since we are not including root, we don't have any restrictions on x oor y for our children nodes
        // Therefore, pick whichever is biggest, x or y
        int withoutRoot = Math.max(leftPair.x,leftPair.y) + Math.max(rightPair.x, rightPair.y);

        return new Pair<>(withRoot, withoutRoot);
    }


    /*
    * Understood question wrong, below was my initial wrong solution
    * */

    public int robWrongSolution(TreeNode root)
    {
        /*
        * First instinct is to do BFS and just add everything up that is on different levels
        * As such, we just need a variable to track which level we are currently on
        * if we start root as level 0, that means we can differentiate the 2 totals by doing modular
        * */
        int level=0;
        int oddLevelAmount=0;
        int evenLevelAmount=0;
        if(root==null) return 0;
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);

        while(!queue.isEmpty())
        {
            int levelSize = queue.size();
            int currentAmount = 0;
            for(int i=0;i<levelSize;i++)
            {
                TreeNode parent = queue.poll();
                if(parent!=null)
                {
                    currentAmount += parent.val;
                    if(parent.left!=null) queue.add(parent.left);
                    if(parent.right!=null) queue.add(parent.right);
                }
            }
            if(level%2==0) evenLevelAmount+=currentAmount;
            else oddLevelAmount+=currentAmount;
            level++;
        }
        return Math.max(evenLevelAmount,oddLevelAmount);
    }
}
