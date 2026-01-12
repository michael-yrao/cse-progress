class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if len(t) > len(s):
            return False
        
        sCur, tCur = 0, 0

        while sCur < len(s) and tCur < len(t):
            if s[sCur] == t[tCur]:
                sCur +=1
            tCur +=1
        
        return sCur == len(s)

    def isSubsequenceInitialSolution(self, s: str, t: str) -> bool:
        # first thought is to check if len(t) > len(s)
        # if not, we just return False
        # Otherwise, we can loop through t and then increment on s as we go through t

        if len(t) < len(s): 
            return False

        subIndex = 0

        for index, value in enumerate(t):
            if subIndex >= len(s):
                return True
            if s[subIndex] == value:
                subIndex += 1
                
        return subIndex >= len(s)