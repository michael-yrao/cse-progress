from typing import List

class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        # Pretty sure, we can just do l,r=0,len-1 and swap r and l values

        l,r=0,len(s)-1
        while r>l:
            temp=s[l]
            s[l] = s[r]
            s[r] = temp
            l+=1
            r-=1