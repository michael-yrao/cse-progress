package DataModel;

import java.util.HashMap;
import java.util.Map;

public class TrieNode
{
    Map<Character, TrieNode> children;
    Boolean endOfWord = false;

    public TrieNode()
    {
        children = new HashMap<>();
    }
}
