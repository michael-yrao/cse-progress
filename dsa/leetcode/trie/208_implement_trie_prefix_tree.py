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


# ── Attempt · 2026-07-17 ──────────────
class TrieNode:
    def __init__(self):
        self.children = {}
        self.isWord = False
        
class Trie_20260717:
# Tries are trees, they don't have values on nodes
# they have values on edges, thus we will have a children map of char -> TrieNode
# we also need to know if this is a word

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        traversal = self.root
        for char in word:
            if char not in traversal.children:
                newNode = TrieNode()
                traversal.children[char] = newNode
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

class TrieNode:
    def __init__(self):
        # char -> TrieNode map
        self.children = {}
        # does a word end here
        self.isEnd = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        inc = self.root
        for char in word:
            # if we haven't seen this char yet
            # append to inc.children as a new child
            if char not in inc.children:
                inc.children[char] = TrieNode()
            # when we are here, the char is guaranteed in the Trie so we go down the trie
            inc = inc.children[char]
        # when we finish, mark inc.isEnd as True
        inc.isEnd = True

    def search(self, word: str) -> bool:
        inc = self.root
        for char in word:
            if char not in inc.children:
                return False
            # if it is, we step down the inc
            inc = inc.children[char]
        return inc.isEnd

    def startsWith(self, prefix: str) -> bool:
        inc = self.root
        for char in prefix:
            if char not in inc.children:
                return False
            # if it is, we step down the inc
            inc = inc.children[char]
        return True

# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)

class TrieNode_20260708:
    
    def __init__(self):
        # string -> Node mapping
        self.children = {}
        self.isWord = False

class Trie_20260708:
    def __init__(self):
        self.root = TrieNode_20260708()

    def insert(self, word: str) -> None:
        traversal = self.root
        for char in word:
            # the way tries work is that the value technically lives on the edge not the node
            # so when we set the children[char] to new TrieNode, we are saying from this node
            # the value to the new node is char
            if char not in traversal.children:
                traversal.children[char] = TrieNode_20260708()
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


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
