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

class TrieNode_20260711:
    def __init__(self):
        self.children = {}
        self.isWord = False

class WordDictionary_20260711:

    def __init__(self):
        self.root = TrieNode_20260711()

    def addWord(self, word: str) -> None:
        traversal = self.root
        for char in word:
            if char not in traversal.children:
                traversal.children[char] = TrieNode_20260711()
            traversal = traversal.children[char]
        traversal.isWord = True

    def search(self, word: str) -> bool:
        # main difficulty here is the wildcard character
        # but matching same character is no big deal
        
        def dfs(node,substr):
            for i in range(len(substr)):
                if substr[i] != '.' and substr[i] not in node.children:
                    return False
                if substr[i] == '.':
                    # we want to skip this letter and we also want to go through every child of node
                    for char, childNode in node.children.items():
                        # if we went all the way down a path and got a match, return true
                        if dfs(childNode, substr[i+1:]):
                            return True
                    # tried all children, did not find success
                    return False
                else:
                    # if not ., then check exact match
                    if substr[i] in node.children:
                        node = node.children[substr[i]]
            return node.isWord
        
        return dfs(self.root, word)


# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)