from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        lcp = ""
        # Need to go through the list of Strings one by one
        # We do need to know which string is the shortest since determines the max length of the LCP
        # Once we have that, we can compare each string to the shortest and we can come up with the answer

        # We can also note that the shortest time complexity here shortest string multiplied by size of list
        # Thus we will be using a double for loop

        # Finds us the string with shortest len() in strs
        # key=len is a built-in lambda expression, we can pass in a custom function instead of len as well
        shortest = min(strs,key=len)

        # Go through each char in shortest string, check them against each string

        for i, value in enumerate(shortest):
            for str in strs:
                if value != str[i]:
                    return shortest[:i] # This is substring of shortest return first i characters
                            
        return shortest
