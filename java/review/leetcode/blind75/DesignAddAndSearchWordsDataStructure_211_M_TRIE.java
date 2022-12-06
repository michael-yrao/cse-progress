package review.leetcode.blind75;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class DesignAddAndSearchWordsDataStructure_211_M_TRIE
{
    /*
    * https://leetcode.com/problems/design-add-and-search-words-data-structure/
    * */

    /*
    *
    *  Any word searching and adding is Trie related
    *
    *  We need a TrieNode class and from there we can start looking at the problem
    *
    * */

    public class WordDictionary
    {

        TrieNode root;

        public WordDictionary()
        {
            root = new TrieNode();
        }

        public void addWord(String word)
        {
            TrieNode currentNode = root;
            for(int i=0;i<word.length();i++)
            {
                if(!currentNode.children.containsKey(word.charAt(i)))
                    currentNode.children.put(word.charAt(i), new TrieNode());

                currentNode = currentNode.children.get(word.charAt(i));
            }
            currentNode.endOfWord=true;
        }

        public boolean search(String word)
        {
            return searchDFS(word,0,root);
        }

        public boolean searchDFS(String word, int index, TrieNode currentNode)
        {
            for(int i=0;i<word.length();i++)
            {
                char currentChar = word.charAt(i);
                // Since . means any character, we should actually just skip it
                // Since we are looking for a word, we should DFS down and check if word exists
                if(currentChar-'.'==0)
                {
                    // Skip the dot, so pass i+1
                    for(TrieNode node : currentNode.children.values())
                    {
                        if(node!=null && searchDFS(word, i + 1, node)) return true;
                    }
                    return false;
                }
                else
                {
                    if (!currentNode.children.containsKey(currentChar)) return false;
                    currentNode = currentNode.children.get(currentChar);
                }
            }
            return currentNode.endOfWord;
        }
    }

    /*
    * Each node of the Trie should indicate whether this is the end of a word
    * Each node of the Trie should also be allowed to have list of children,
    * but since list has O(n) access, we should use Set or Map
    * Since we also need a way to store the Character at each Node, we should use Map instead of Set
    * */

    private class TrieNode
    {

        boolean endOfWord = false;
        Map<Character, TrieNode> children;

        public TrieNode()
        {
            children = new HashMap<>();
        }
    }
}
