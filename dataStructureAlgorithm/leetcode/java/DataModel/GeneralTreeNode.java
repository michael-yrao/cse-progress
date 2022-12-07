package DataModel;

import java.util.List;

public class GeneralTreeNode
{
    String content;                 // content in case we are dealing with Strings
    int value;                      // value in case we are dealing with numbers
    GeneralTreeNode parent;         // Keeps track of this node's parent
    List<GeneralTreeNode> children; // Keeps track of this node's children
    int level;                      // level this node belongs to on the tree

    public GeneralTreeNode(String content, GeneralTreeNode parent, List<GeneralTreeNode> children, int level)
    {
        this.content = content;
        this.parent = parent;
        this.children = children;
        this.level = level;
    }
}
