package review.leetcode.blind75;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ImplementTrie_208_M_TRIE
{
    /*
    * https://leetcode.com/problems/implement-trie-prefix-tree/
    * */

    class TrieNode
    {
        Map<Character, TrieNode> children;
        Boolean endOfWord = false;

        public TrieNode()
        {
            children = new HashMap<>();
        }
    }

    class Trie
    {

        TrieNode root;

        public Trie()
        {
            root = new TrieNode();
        }

        public void insert(String word)
        {
            TrieNode currentNode = root;
            for(int i=0;i<word.length();i++)
            {
                if(!currentNode.children.containsKey(word.charAt(i)))
                    currentNode.children.put(word.charAt(i), new TrieNode());
                currentNode = currentNode.children.get(word.charAt(i));
            }
            currentNode.endOfWord = true;
        }

        public boolean search(String word)
        {
            TrieNode currentNode = root;
            for(int i=0;i<word.length();i++)
            {
                if(!currentNode.children.containsKey(word.charAt(i))) return false;
                else currentNode = currentNode.children.get(word.charAt(i));
            }
            return currentNode.endOfWord;
        }

        public boolean startsWith(String prefix)
        {
            TrieNode currentNode = root;
            for(int i=0;i<prefix.length();i++)
            {
                if(!currentNode.children.containsKey(prefix.charAt(i))) return false;
                else currentNode = currentNode.children.get(prefix.charAt(i));
            }
            return true;
        }
    }
}
