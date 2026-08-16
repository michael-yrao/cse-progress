"""
A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:

    Trie() Initializes the trie object.
    void insert(String word) Inserts the string word into the trie.
    boolean search(String word) Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.
    boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.

Example 1:

Input
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
Output
[null, null, true, false, true, null, true]

Explanation
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // return True
trie.search("app");     // return False
trie.startsWith("app"); // return True
trie.insert("app");
trie.search("app");     // return True

Constraints:

    1 <= word.length, prefix.length <= 2000
    word and prefix consist only of lowercase English letters.
    At most 3 * 104 calls in total will be made to insert, search, and startsWith.
"""


# ── Attempt · 2026-08-16 ──────────────
# NOTE: suffix any helper class you write (Node, TrieNode, …) with _20260816 too — an undated helper collides with the restored canonical one.
class TrieNode_20260816:
    
    def __init__(self):
        self.children = {}
        self.isWord = False
        
class Trie_20260816:

    def __init__(self):
        self.root = TrieNode_20260816()

    def insert(self, word: str) -> None:
        traversal = self.root
        for char in word:
            if char not in traversal.children:
                traversal.children[char] = TrieNode_20260816()
            traversal = traversal.children[char]
        traversal.isWord = True

    def search(self, word: str) -> bool:
        traversal = self.root
        for char in word:
            if char not in traversal.children:
                return False
            traversal = traversal.children[char]
        return traversal.isWord

    def startsWith(self, prefix: str) -> bool:
        traversal = self.root
        for char in prefix:
            if char not in traversal.children:
                return False
            traversal = traversal.children[char]
        return True

# ⤵ prior attempts stashed in dsa/leetcode/.history/208_implement_trie_prefix_tree.txt — restored at session end (python scripts/restore_history.py)
