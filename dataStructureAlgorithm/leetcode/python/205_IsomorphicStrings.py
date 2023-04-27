import unittest

class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        # Isomorphism means 1-1 mapping from s to t and t to s
        # Therefore 2 maps are needed
        sMap = {}
        tMap = {}

        # We are given len(s) = len(t), so no need to check
        for i in range(len(s)):
            if s[i] in sMap and sMap.get(s[i]) != t[i]:
                return False
            elif t[i] in tMap and tMap.get(t[i]) != s[i]:
                return False
            else:
                sMap[s[i]] = t[i]
                tMap[t[i]] = s[i]
        return True
    
class UnitTest(unittest.TestCase):
    def testIsomprhic(self):
        s = "badc"
        t = "baba"
        expectedAnswer = False
        result = Solution().isIsomorphic(s,t)
        self.assertEquals(expectedAnswer,result)

unittest.main()