from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Since all anagrams are the same when sorted, we will take advantage of that
        # 1. Create a map of string -> List[string]
        # 2. Loop through the list of strings
        # 3. if map has string.sort(), we will add it to that map.get(sortedString)
        #    otherwise, add new map key and add the string to map.get(sortedString)
        # 4. Return map.values()

        map = {}

        for str in strs:
            sortedStr = ''.join(sorted(str))
            if sortedStr not in map:
                map[sortedStr] = []
            map.get(sortedStr).append(str)
        
        return list(map.values())