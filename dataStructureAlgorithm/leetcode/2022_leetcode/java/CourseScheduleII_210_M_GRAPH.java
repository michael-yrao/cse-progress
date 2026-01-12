package review.leetcode.leetcodeExtra;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class CourseScheduleII_210_M_GRAPH
{
    /*
    * https://leetcode.com/problems/course-schedule-ii/
    * */

    // Same problem as Course Schedule
    // Difference is we have to return an array with order we should take the course
    // Below is the slightly more optimized version of the code
    // Biggest difference is I use a Set to check if we have already added it to result
    // Thus saving us O(n) time, but still end up with result of O(V + E) where E = edges/pre-req and V = vertices/courses

    public int[] findOrderOptimized(int numCourses, int[][] prerequisites)
    {
        List<Integer> returnList = new ArrayList<>();

        // This will be the "adjacency list" we use for topological sort
        Map<Integer, List<Integer>> prereqMap = new ConcurrentHashMap<>();

        // Make sure we populate all courses onto the Map as Keys
        for(int i=0;i<numCourses;i++)
        {
            prereqMap.put(i,new ArrayList<>());
        }

        // Put all the pre-reqs into the values
        for(int[] prereq : prerequisites)
        {
            prereqMap.get(prereq[0]).add(prereq[1]);
        }

        // Create a Set to check cycle
        // Create another Set to check whether or not we have added to the result list, this save us a good amount of time

        Set<Integer> cycleDetection = new HashSet<>();
        Set<Integer> hasBeenAddedToResult = new HashSet<>();

        for(Integer currentCourse : prereqMap.keySet())
        {
            if(!optimizedDFS(currentCourse,returnList,prereqMap,cycleDetection,hasBeenAddedToResult)) return new int[0];
        }
        return returnList.stream().mapToInt(i->i).toArray();
    }

    private boolean optimizedDFS(Integer currentCourse, List<Integer> returnList, Map<Integer, List<Integer>> prereqMap, Set<Integer> cycleDetection, Set<Integer> hasBeenAddedToResult)
    {
        if(cycleDetection.contains(currentCourse)) return false;
        if(hasBeenAddedToResult.contains(currentCourse)) return true;

        // We add the course to cycle detection to say that we are currently visiting it
        cycleDetection.add(currentCourse);

        for(Integer prereq : prereqMap.get(currentCourse))
        {
            if(!optimizedDFS(prereq,returnList,prereqMap,cycleDetection,hasBeenAddedToResult)) return false;
        }
        cycleDetection.remove(currentCourse);
        returnList.add(currentCourse);
        hasBeenAddedToResult.add(currentCourse);
        return true;
    }

    // Below was my initial code
    // Practically identical to Course Schedule I

    public int[] findOrder(int numCourses, int[][] prerequisites)
    {
        /*
        * Similar to Course Schedule I, we need a HashMap of courses and their prereqs
        * We also need a Set again to check whether or not there is a cycle
        * Big difference here is we need the correct ordering of classes to take
        * This basically means we are doing Topological Sort
        *
        * For Topological Sort, we need node and its neighbors, normally it is an adjacency list
        * But for us, we will use the pre-req map to serve this purpose since it is a bit easier to read
        *
        * */

        List<Integer> courseOrder = new ArrayList<>();

        // This will be the "adjacency list" we use for topological sort
        Map<Integer, List<Integer>> prereqMap = new ConcurrentHashMap<>();

        // Keeps track of whether we are in a cycle or not
        Set<Integer> visitedSet = new HashSet<>();

        // Make sure we populate all courses onto the Map as Keys
        for(int i=0;i<numCourses;i++)
        {
            prereqMap.put(i,new ArrayList<>());
        }

        // Put all the pre-reqs into the values
        for(int[] prereq : prerequisites)
        {
            prereqMap.get(prereq[0]).add(prereq[1]);
        }

        for(Integer currentCourse : prereqMap.keySet())
        {
            if(!courseScheduleDFS(currentCourse,courseOrder,prereqMap,visitedSet)) return new int[0];
        }
        return courseOrder.stream().mapToInt(i->i).toArray();
    }

    private boolean courseScheduleDFS(Integer currentCourse, List<Integer> courseOrder, Map<Integer, List<Integer>> prereqMap, Set<Integer> visitedSet)
    {
        // If we are in a cycle, return false and return empty list
        if(visitedSet.contains(currentCourse)) return false;
        if(prereqMap.get(currentCourse) == null || prereqMap.get(currentCourse).isEmpty())
        {
            if(!courseOrder.contains(currentCourse)) courseOrder.add(currentCourse);
            return true;
        }
        // Mark currentCourse as visiting
        visitedSet.add(currentCourse);

        for(Integer prereq : prereqMap.get(currentCourse))
        {
            if(!courseScheduleDFS(prereq,courseOrder,prereqMap,visitedSet)) return false;
        }

        // Finished visiting, remove from Set
        visitedSet.remove(currentCourse);

        // Since we know we can complete this course, we can just remove all pre-reqs of this course
        // And pretend we can complete it without issues
        prereqMap.get(currentCourse).clear();

        // Finally now that we have went through all the pre-reqs of this course, we can add this course to the return list

        if(!courseOrder.contains(currentCourse)) courseOrder.add(currentCourse);

        return true;
    }
}
