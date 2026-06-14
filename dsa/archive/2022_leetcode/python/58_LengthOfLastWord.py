class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        # Trim ending spaces
        # Then iterate from end to first space

        strippedString = s.rstrip()
        counter = 0

        for index in range(len(strippedString)-1, -1, -1):
            if(strippedString[index] == ' '):
                return counter
            counter += 1
        
        return counter