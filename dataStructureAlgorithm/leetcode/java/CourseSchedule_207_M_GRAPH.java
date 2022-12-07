package review.leetcode.blind75;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class CourseSchedule_207_M_GRAPH
{
    /*
    * https://leetcode.com/problems/course-schedule/
    * */

    /*
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: true
    Explanation: To take course 1, we need to take course 0. Since course 0 has no pre-req, it is possible

    Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
    Output: false
    Explanation: Impossible since taking 1 requires 0 but taking 0 also requires 1. So cycle = not possible
     */

    public boolean canFinish(int numCourses, int[][] prerequisites)
    {
        /*
        * Put courses and their pre reqs into a Hash Map
        * We also need to have a Set to tell us whether the node in the graph has been visited
        * This way we can detect whether or not we have a cycle, e.g. not completable course schedule
        * */

        Map<Integer, List<Integer>> prereqMap = new ConcurrentHashMap<>();

        // Pre-populate the map with all the courses

        for(int i=0;i<numCourses;i++)
        {
            prereqMap.put(i,new ArrayList<>());
        }

        // Populate the pre-reqs into the map

        for (int[] prerequisite : prerequisites) {
            prereqMap.get(prerequisite[0]).add(prerequisite[1]);
        }

        Set<Integer> visitedSet = new HashSet<>();

        for (Integer currentCourse : prereqMap.keySet()) {
            if (!canCompleteCourseDFS(currentCourse, visitedSet, prereqMap)) return false;
        }

        return true;
    }

    private boolean canCompleteCourseDFS (Integer currentCourse, Set<Integer> visitedSet, Map<Integer, List<Integer>> prereqMap)
    {
        // If we have already visited this course, it means we are in a cycle, so return false immediately
        if(visitedSet.contains(currentCourse)) return false;

        // If there are no pre-req for this current course, we can return true immediately
        if(prereqMap.get(currentCourse) == null || prereqMap.get(currentCourse).isEmpty()) return true;

        // If neither condition is satisfied, we will mark this course as visited
        visitedSet.add(currentCourse);

        // Check the same conditions for all pre-reqs of this current course

        for(Integer preReqCourse : prereqMap.get(currentCourse))
        {
            // If for any reason, we get a false return from the pre-reqs, that means we are in a cycle
            // Therefore we should return false immediately
            if (!canCompleteCourseDFS(preReqCourse, visitedSet, prereqMap)) return false;
        }

        // At this point, we are certain we can complete this course.

        // Since we know we can finish this course, we can remove it from the Visited Set since we use the Visited Set
        // Purely for the purpose of finding cycles
        visitedSet.remove(currentCourse);

        // Since we know we can complete this course, we can just remove all pre-reqs of this course
        // And pretend we can complete it without issues
        prereqMap.remove(currentCourse);

        return true;
    }
}
