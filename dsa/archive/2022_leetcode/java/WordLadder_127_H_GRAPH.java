package review.leetcode.leetcodeExtra;

import java.util.*;

public class WordLadder_127_H_GRAPH
{
    /*
    * https://leetcode.com/problems/word-ladder/
    * */

    /*
    * Idea for this problem is that we want to transform one character at a time to get from beginWord to endWord
    * Using words from wordList but differing in only 1 letter. The endWord also must be in the wordList
    *
    * 1. So what we should do is using all words in word List, we should create multiple patterns
    *    e.g. hot -> *ot, h*t, ho*
    * 2. Using these patterns, we will map all the other words in the word List to these patterns as an adjacency list
    * 3. Since we want the smallest path from begin to end, we would want to use BFS with our adjacency list
    * */

    public int ladderLength(String beginWord, String endWord, List<String> wordList)
    {
        if(!wordList.contains(endWord)) return 0;

        // Assuming each word in wordList is unique so I can use Set. Not too much difference between using Set and List here
        Map<String, List<String>> adjacencyList = new HashMap<>();

        // Add beginWord to wordList so we can build
        wordList.add(beginWord);

        for(String word : wordList)
        {
            // Create a pattern for each character of word
            StringBuilder sb = null;
            for(int i=0;i<word.length();i++)
            {
                sb = new StringBuilder(word);
                sb.setCharAt(i,'*');
                adjacencyList.putIfAbsent(sb.toString(),new ArrayList<>());
                adjacencyList.get(sb.toString()).add(word);
            }
        }

        // Now that we have our adjacency list, we can just pretend this is a graph and do BFS as usual
        // Using a Queue and a Visited Set

        Set<String> visited = new HashSet<>();
        Queue<String> queue = new LinkedList<>();

        // Start our graph at beginWord

        visited.add(beginWord);
        queue.add(beginWord);

        // Since we know endWord exists, we are making at least 1 step to get to our result
        // Thus initialize as 1

        int pathLength = 1;

        while(!queue.isEmpty())
        {
            int queueSize = queue.size();

            for(int i=0;i<queueSize;i++)
            {
                String word = queue.poll();
                if(word.equals(endWord)) return pathLength;

                // Go through each pattern of the current word and visit the neighbors if unvisited

                StringBuilder pattern = null;
                for(int j=0;j<word.length();j++)
                {
                    pattern = new StringBuilder(word);
                    pattern.setCharAt(j,'*');
                    for(String neighborWord : adjacencyList.get(pattern.toString()))
                    {
                        if(visited.contains(neighborWord)) continue;

                        visited.add(neighborWord);
                        queue.offer(neighborWord);
                    }
                }
            }
            pathLength++;
        }

        // If we couldn't find a path to endWord, we have to return 0
        return 0;
    }
}
