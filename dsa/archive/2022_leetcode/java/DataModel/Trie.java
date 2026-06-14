package DataModel;

public class Trie
{ TrieNode root;

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
