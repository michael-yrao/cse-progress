package review.leetcode.leetcodeExtra;

import DataModel.GeneralTreeNode;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;

public class LongestAbsoluteFilePath_388_M_TREE
{
    /*
    * https://leetcode.com/problems/longest-absolute-file-path/
    * */

    /*
    * Easiest way to look at this problem is to think of it as a tree instead of a long String, depicted below:
    *
    * String: "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"
    *
    *
    *                     dir
               .                       .
            subdir1                  subdir2
            .    .                   .     .
        file1    subsub1       subsub2     file2
    *
    * L0 -> L1 has 1 tab
    * L1 -> L2 has 2 tab, etc.
    * Thus we can maybe generate this as a Tree
    * Then perform maybe preorder traversal to get our directory path
    *
    * We have 2 files here and we want the longest absolute path
    *
    * */

    /*
    * However, there are much simpler implementations
    *
    * String: "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"
    *
    * First thing we do is split the string by \n and we get the below:
    *
        dir
        ⟶ subdir1
        ⟶ ⟶ file1.ext
        ⟶ ⟶ subsubdir1
        ⟶ subdir2
        ⟶ ⟶ subsubdir2
        ⟶ ⟶ ⟶ file2.ext
    *
    * If we think about how we would iterate through this manually, it would be as follows:
    *
    * dir -> subdir1 -> file1.ext. Once we hit subsubdir1, we need to remove file1.ext so we can go into subsubdir1
    * dir -> subdir1 -> subsubdir1. This is now the end of subdir1, and we need to remove both to get to subdir2
    * dir -> subdir2, etc...
    *
    * From here, we can see these actions are exactly that of a Stack, thus we will use a Stack to solve this problem
    *
    * */

    public int lengthLongestPath(String input)
    {
        // The stack will contain the length of the directory where the stack is currently at
        Deque<Integer> stack = new ArrayDeque<>();
        // Prior to starting, it has length of zero
        stack.push(0);

        int maxLength = 0;

        for(String x : input.split("\n"))
        {
            // For each String, if we are going deeper in the filepath, we want to push stack.peek() + length of dir/file + 1 to stack
            // Otherwise, pop (size of stack - current level - 1), we are doing - 1 here since we started with stack of size 1

            int level = x.lastIndexOf("\t") + 1;

            // Find the parent directory

            while(level + 1 < stack.size()) stack.pop();

            // stack.peek() gives us the parent directory's length
            // x.length() - level gives us the true directory length without the tabs

            int currentLength = stack.peek() + (x.length() - level) + 1;

            stack.push(currentLength);

            // If this is a file, we need to update max Length
            if(x.contains("."))  maxLength = Math.max(maxLength,currentLength-1);
        }
        return maxLength;
    }
}
