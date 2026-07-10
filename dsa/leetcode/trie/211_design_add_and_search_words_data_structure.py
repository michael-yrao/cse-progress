class TrieNode_20260709:
    def __init__(self):
        self.children = {}
        self.isWord = False

class WordDictionary_20260709:

    def __init__(self):
        self.root = TrieNode_20260709()

    def addWord(self, word: str) -> None:
        traversal = self.root
        for char in word:
            if char not in traversal.children:
                traversal.children[char] = TrieNode_20260709()
            traversal = traversal.children[char]
        traversal.isWord = True

    def search(self, word: str) -> bool:
        # so this is like a form of DFS
        # and what we are going to do is go down a route as far as we can
        # then when we hit a wildcard, we need to look at every single child of that node
        # so we loop for the characters we know (non-wildcards)
        # then we perform recursion for characters that we do not know (wildcards)
        def dfs(i, node):
            currentNode = node
            for j in range(i,len(word)):
                char = word[j]
                if char == '.':
                    # if wildcard, we need to check every child
                    for child in currentNode.children.values():
                        # but since it's wildcard, we need to skip this value
                        if dfs(j+1,child):
                            return True
                    # tried all children, no luck, thus return False
                    return False
                else:
                    # if not wildcard, check if not in children and immediately return False is bad
                    if char not in currentNode.children:
                        return False
                    # if no issues, continue to next node
                    currentNode = currentNode.children[char]
            return currentNode.isWord
        return dfs(0,self.root)

# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)