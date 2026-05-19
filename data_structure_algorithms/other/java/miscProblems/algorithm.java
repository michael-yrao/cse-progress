package review;

import DataModel.Node;

import java.math.BigInteger;
import java.text.DecimalFormat;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.Collectors;

public class algorithm
{
    //region Basic Algorithms

    public Node reverseLinkedList(Node head)
    {
        Stack<Node> stack = new Stack<>();
        Node traveller = head;
        Node returnNode;

        while(traveller.getNext() != null)
        {
            stack.push(traveller);
            traveller=traveller.getNext();
        }

        traveller = stack.peek(); // Set traveller to start at beginning of new list
        returnNode = traveller;

        while(!stack.isEmpty())
        {
            stack.pop();
            traveller.setNext(stack.peek());
            traveller = stack.peek();
        }

        return returnNode;
    }

    public Node reverseLinkedListInPlace(Node head)
    {

        Node prev = null;
        Node current = head;
        Node next;

        while (current != null) {
            next = current.getNext();
            current.setNext(prev);
            prev = current;
            current = next;
        }
        head = prev;
        return head;

    }

    /**
    * Alternative to Tortoise and hare algorithm is to use a HashSet/Set of Nodes
    * Add Nodes into the Set while checking to see if the Node already exist in Set
    * If exists in Set, return true
    * */

    public boolean isLinkedListLooped(Node head)
    {
        Node tortoise = head.getNext();
        Node hare = head.getNext().getNext();

        // We want to move hare 2 nodes at a time while moving tortoise 1 node at a time

        while(!tortoise.equals(hare))
        {
            if(hare == null) return false;

            tortoise = tortoise.getNext();
            hare = hare.getNext().getNext();
        }

        return true;
    }

    public boolean isLinkedListPalindrome(Node head)
    {
        // palindrome is a word where its the same from beginning or from the end

        Stack<Node> nodeStack = new Stack<>();

        Node cursor = head;

        while(cursor != null)
        {
            nodeStack.push(cursor);
            cursor = cursor.getNext();
        }

        cursor = head;

        while(cursor != null)
        {
            // Loop through the list again from beginning and compare with stack
            // If at any point, there is an inequality, we return false

            if(cursor.get() != nodeStack.pop().get()) return false;

            cursor = cursor.getNext();
        }

        return true;
    }

    public boolean isLinkedListPalindromeRecursion(Node head)
    {
        //TODO

        return isLinkedListPalindromeRecursion(head.getNext());
    }

    public int getLengthOfLinkedList(Node head)
    {
        if(head==null) return 0;

        return 1 + getLengthOfLinkedList(head.getNext());
    }

    public Node intersectionOfLinkedList(Node first, Node second)
    {
        Node head = null;
        Node returnCursor = null;
        Node cursor;
        Map<Node,Integer> longerLinkedList = new HashMap<>();

        int firstLength = getLengthOfLinkedList(first);
        int secondLength = getLengthOfLinkedList(second);

        // Put longer list into the map

        cursor=(firstLength>secondLength)?first:second;

        while(cursor != null)
        {
            longerLinkedList.put(cursor, cursor.get());
            cursor = cursor.getNext();
        }

        // Reset cursor to shorter list

        cursor=(firstLength<secondLength)?first:second;

        while(cursor != null)
        {
            if(longerLinkedList.containsValue(cursor.get()))
            {
                if(head == null)
                {
                    head = cursor;
                    returnCursor = head;
                }
                else
                {
                    head.setNext(cursor);
                    head = cursor;
                }
            }
            cursor = cursor.getNext();
        }

        return returnCursor;
    }

    //endregion

    //region Sorting Algorithms

    /**
     * Quick Sort ArrayList
     * */

    public void quickSort(int[] list, int lowerIndex, int upperIndex)
    {

        // Stop the recursion when lowerIndex and upperIndex meet

        // Quicksort and Mergesort are both Divide and Conquer algorithms

        // Quicksort's "dividing" portion is typically called "partitioning"
        // e.g. sorting smaller partitions based on pivot returned by the helper function

        int pivotIndex = quickSortPartition(list,lowerIndex,upperIndex);

        if(lowerIndex < upperIndex)
        {

            // Assuming pivot is already in the correct place, we want to sort all elements below it

            quickSortPartition(list,0,pivotIndex - 1);

            // Assuming pivot is already in the correct place, we want to sort all elements above it

            quickSortPartition(list,pivotIndex + 1, list.length+1);

        }

    }

    public int quickSortPartition(int[] list, int lowerIndex, int upperIndex)
    {
        /**
         * Returns the new pivot to be used for further partitioning
         * */
        // First thing to do is to select a pivot
        // A randomized pivot minimizes the possibility of worst case scenario of O(n^2)

        int pivotIndex = ThreadLocalRandom.current().nextInt(lowerIndex, upperIndex+1);

        int pivotValue = list[pivotIndex];

        int lowerIncrement = lowerIndex - 1;

        for(int parser=lowerIndex;parser<upperIndex;parser++)
        {
            if(list[parser] < pivotValue)
            {
                lowerIncrement++;
                quickSortSwap(list,lowerIncrement,parser);
            }
        }

        quickSortSwap(list,lowerIncrement+1,upperIndex);

        return lowerIncrement+1;

    }

    public void quickSortSwap(int[] list, int first, int second)
    {
        int temp = second;
        list[second] = list[first];
        list[first] = temp;
    }

    //endregion

    //region Search Algorithms



    //endregion

    //region Shortest Path Algorithm
    //endregion

    //region Generic Helpers

    /*
    * Initially had an issue where we did + ' '. This instead of concating actually ended up adding the ascii value of space to the variable, thus printing out constants
    * */

    public void printIntegerArrayIndices(int[] numbers)
    {
        for(int i=0;i<numbers.length;i++)
        {
            System.out.print(String.valueOf(i) + ", ");
        }
        System.out.println();
    }

    //endregion

    //region LeetCode Easy Questions

    //region Concatenation of Array

    /**
     * Given an integer array nums of length n,
     * you want to create an array ans of length 2n where ans[i] == nums[i] and ans[i + n] == nums[i]
     * for 0 <= i < n (0-indexed).
     *
     * Specifically, ans is the concatenation of two nums arrays.
     *
     * Return the array ans.
     * */

    public int[] getConcatenation(int[] nums)
    {
        int[] solution = new int[nums.length * 2];
        Map<Integer,Integer> numMap = new HashMap<>();

        for(int i=0;i<nums.length;i++)
        {
            numMap.put(i,nums[i]);
            numMap.put(i+nums.length,nums[i]);
        }

        for(int i=0;i<solution.length;i++)
        {
            solution[i] = numMap.get(i);
        }

        return solution;
    }

    //endregion



    //endregion

    //region Hacker Rank Questions

    public static void plusMinus(List<Integer> arr)
    {
        // Write your code here

        List<Integer> ratioElements = new ArrayList<>();
        // index 0 = positive
        // index 1 = negative
        // index 2 = zeroes

        ratioElements.add(0, 0);
        ratioElements.add(1, 0);
        ratioElements.add(2, 0);

        for(int index=0;index<arr.size();index++)
        {
            if( arr.get(index) > 0 )
            {
                ratioElements.set(0, ratioElements.get(0) + 1);
            }
            else if ( arr.get(index) < 0 )
            {
                ratioElements.set(1, ratioElements.get(1) + 1);
            }
            else
            {
                ratioElements.set(2, ratioElements.get(2) + 1);
            }
        }

        DecimalFormat format = new DecimalFormat("#.######");

        for(int index=0;index<ratioElements.size();index++)
        {
            System.out.println(format.format((double)ratioElements.get(index)/(double)arr.size()));
        }
    }

    public static void miniMaxSum(List<Integer> arr) {
        // Write your code here

        // Just sort and add

        Collections.sort(arr);

        long minSum=0;
        long maxSum=0;

        for(int i=0;i<arr.size()-1;i++)
        {
            minSum+=arr.get(i);
        }
        for(int i=arr.size()-1;i>0;i--)
        {
            maxSum+=arr.get(i);
        }
        System.out.print(Long.toString(minSum) + ' ' + Long.toString(maxSum));

    }

    public static String timeConversion(String s)
    {
        // Write your code here

        char timeOfDay=s.charAt(s.length()-2);

        if((timeOfDay=='A' && Integer.parseInt(s.substring(0, 2)) != 12) || (timeOfDay=='P' && Integer.parseInt(s.substring(0, 2)) == 12))
        {
            return s.substring(0, s.length()-2);
        }
        String substring = s.substring(2, s.length() - 2);
        if(timeOfDay=='A' && Integer.parseInt(s.substring(0, 2)) == 12)
        {
            return "00"+ substring;
        }
        else if(timeOfDay=='P')
        {
            return Integer.toString(Integer.parseInt(s.substring(0, 2))+12)+ substring;
        }
        else return "";
    }

    public static List<Integer> matchingStrings(List<String> strings, List<String> queries) {
        // Write your code here
        Map<String,Integer> queriesMap = new HashMap<>();

        List<Integer> returnList = new ArrayList<>();

        // put queries into map for easy counter

        for(int i=0;i<queries.size();i++)
        {
            queriesMap.put(queries.get(i),0);
        }

        for(int i=0;i<strings.size();i++)
        {
            if(queriesMap.containsKey(strings.get(i)))
            {
                queriesMap.put(strings.get(i), queriesMap.get(strings.get(i))+1);
            }
        }

        for(int i=0;i<queries.size();i++)
        {
            if(queriesMap.containsKey(queries.get(i)))
            {
                returnList.add(queriesMap.get(queries.get(i)));
            }
        }
        return returnList;
    }

    public static int lonelyinteger(List<Integer> a)
    {
        // Write your code here

        Map<Integer,Integer> intMap = new HashMap<>();

        for(int i=0;i<a.size();i++)
        {
            if(!intMap.containsKey(a.get(i)))
                intMap.put(a.get(i), 1);
            else
                intMap.put(a.get(i), intMap.get(a.get(i))+1);
        }

        for (Map.Entry<Integer,Integer> entry : intMap.entrySet())
        {
            if(entry.getValue() == 1)
                return entry.getKey();
        }

        return 0;

    }

    public static long flippingBits(long n)
    {
        // Write your code here
        // Knowing the number is 32-bit and unsigned, we can just use max value and subtract to get flipped value
        long maxNumber=4294967295L;
        return Math.abs(maxNumber - n);
    }

    public static int diagonalDifference(List<List<Integer>> arr)
    {
        // Write your code here

        int leftSum=0;
        int rightSum=0;

        // arr.size() gives total numbers of list in the list of list which is row size

        for(int i=0;i<arr.size();i++)
        {
            leftSum+=arr.get(i).get(i);
            rightSum+=arr.get(arr.get(0).size()-i-1).get(i);
        }

        return Math.abs(leftSum-rightSum);
    }

    public static List<Integer> countingSortMap(List<Integer> arr)
    {
        // Write your code here
        Map<Integer,Integer> intMap = new HashMap<>();

        for(int i=0;i<arr.size();i++)
        {
            if(intMap.containsKey(arr.get(i))){
                intMap.put(arr.get(i), intMap.get(arr.get(i))+1);
            }
            else{
                intMap.put(arr.get(i), 1);
            }
        }

        List<Integer> returnList = new ArrayList<>();

        for(int i=0;i<100;i++)
        {
            returnList.add(intMap.getOrDefault(i, 0));
        }

        return returnList;
    }

    // Knowing the value in the list are between 0-100, we can just use int array

    public static List<Integer> countingSort(List<Integer> arr)
    {
        // Write your code here

        int[] count = new int[100];

        for(int i=0;i<arr.size();i++)
        {
            count[arr.get(i)]++;
        }

        return Arrays.stream(count).boxed().collect(Collectors.toList());
    }

    public static String pangrams(String s)
    {
        // Write your code here

        // Space is decimal 32
        // upper case z is decimal 90
        // Inclusive space needed is 59

        char[] asciiArray = new char[59];

        for(int i=0;i<s.length();i++)
        {
            asciiArray[s.toUpperCase().charAt(i) - 32]++;
        }

        for(int i=0;i<asciiArray.length;i++)
        {
            if(( (i != 0 && i < 33)) && asciiArray[i] > 1)
            {
                return "not pangram";
            }
            else if(i == 0 || i >= 33)
            {
                if(asciiArray[i] == 0)
                {
                    return "not pangram";
                }
            }
        }

        return "pangram";

    }

    /*
     * Complete the 'twoArrays' function below.
     *
     * The function is expected to return a STRING.
     * The function accepts following parameters:
     *  1. INTEGER k
     *  2. INTEGER_ARRAY A
     *  3. INTEGER_ARRAY B
     */

    public static String twoArrays(int k, List<Integer> A, List<Integer> B)
    {
        // Write your code here
        Collections.sort(A);
        Collections.sort(B);
        Collections.reverse(B);

        for(int i=0;i<A.size();i++)
        {
            if(A.get(i)+B.get(i) < k)
            {
                return "NO";
            }
        }
        return "YES";
    }

    /*
     * Birthday Bar
     * Complete the 'birthday' function below.
     *
     * The function is expected to return an INTEGER.
     * The function accepts following parameters:
     *  1. INTEGER_ARRAY s
     *  2. INTEGER d
     *  3. INTEGER m
     */

    public static int birthday(List<Integer> s, int d, int m)
    {
        // Write your code here

        // Knowing m is the size of the array, we should create an array of size m
        // try to put numbers into array to sum up to d. repeat until we get number of solutions

        int length = s.size();

        int sum = 0, ways = 0;

        // Loop until i is less or equal to length - m so we don't get array out of bound. then check m size solutions

        for(int i=0;i<=(length - m);i++)
        {
            for(int j=0;j<m;j++)
            {
                sum+=s.get(j+i);
            }
            if(sum == d)
            {
                ways++;
            }
            sum=0;
        }

        return ways;

    }

    public static String stringsXOR(String s, String t)
    {
        String res = new String("");
        for(int i = 0; i < s.length(); i++) {
            if(s.charAt(i) == t.charAt(i))
                res+="0";
            else
                res+= "1";
        }

        return res;
    }

    public static int sockMerchant(int n, List<Integer> ar)
    {
        // Write your code here
        Map<Integer,Integer> pairMap = new HashMap<>();

        for(int i=0;i<n;i++)
        {
            if(pairMap.containsKey(ar.get(i)))
            {
                pairMap.put(ar.get(i),pairMap.get(ar.get(i))+1);
            }
            else
                pairMap.put(ar.get(i),1);
        }

        int totalPairs=0;

        for(Map.Entry<Integer,Integer> entry : pairMap.entrySet())
        {
            totalPairs+=(entry.getValue()/2);
        }

        return totalPairs;

    }

    /*
    * Solution using set is slightly more efficient. O(n) instead of O(2n).
    * However, no true difference in practice
    * */

    public static int sockMerchantSet(int n, List<Integer> ar)
    {
        // Write your code here
        Set<Integer> set = new HashSet<>();

        int pairCount=0;

        for(int i=0;i<n;i++)
        {
            if(set.contains(ar.get(i)))
            {
                pairCount++;
                set.remove(ar.get(i));
            }
            else
                set.add(ar.get(i));
        }

        return pairCount;
    }

    public static void findZigZagSequence(int [] a, int n)
    {
        // Idea is to sort entire list to get first half in correct position
        // Put max in middle position
        // Sort second half of array in descending order

        Arrays.sort(a); // Sort so first element is in correct position

        int midPosition=n/2;

        int temp = a[midPosition];

        a[midPosition] = a[n-1]; // Change mid to max value. It is now in correct position

        a[n-1] = temp; // Change end to mid value. It is now in correct position

        int midStart = midPosition+1;
        int endPosition = n-2;

        while(midStart <= endPosition)
        {
            temp = a[midStart];
            a[midStart] = a[endPosition];
            a[endPosition] = temp;
            midStart++;
            endPosition--;
        }

        for(int i=0;i<n;i++)
        {
            if(i>0) System.out.print(" ");

            System.out.print(a[i]);
        }

    }

    public static int pageCount(int n, int p)
    {
        // Write your code here
        // Apparently opening the book doesn't count as a flip

        int frontFlip = p/2;
        int backFlip = n%2==0?(n-p+1)/2:(n-p)/2;

        return Math.min(frontFlip, backFlip);
    }

    public static String caesarCipher(String s, int k)
    {
        StringBuilder sb = new StringBuilder();
        // Write your code here
        for(int i=0;i<s.length();i++)
        {
            sb.append(caesarCipherHelper(s.charAt(i), k));
        }
        return sb.toString();
    }

    public static char caesarCipherHelper(char currentChar, int k)
    {
        if(currentChar>=65 && currentChar<=90)
        {
            int originalPosition = currentChar-'A';
            return (char)((originalPosition+k)%26 + 'A');
        }

        else if(currentChar>=97 && currentChar<=122)
        {
            int originalPosition = currentChar-'a';
            return (char)((originalPosition+k)%26 + 'a');
        }

        else return currentChar;
    }

    public static int maxMin(int k, List<Integer> arr)
    {
        // Write your code here
        // We just want closest numbers k-1 distance apart

        Collections.sort(arr);
        int currentMin=Integer.MAX_VALUE;

        for(int i=0;i<arr.size()-(k-1);i++)
        {
            if(arr.get(i+k-1) - arr.get(i) < currentMin)
            {
                currentMin=arr.get(i+k-1) - arr.get(i);
            }
        }
        return currentMin;
    }

    //endregion

    public static String balancedSums(List<Integer> arr)
    {
        // Write your code here


        int totalSum=0;
        int runningSum=0;

        for(int i=0;i<arr.size();i++)
        {
            totalSum+=arr.get(i);
        }

        for(int i=0;i<arr.size();i++)
        {
            totalSum-=arr.get(i);
            if(runningSum==totalSum) return "YES";
            runningSum+=arr.get(i);
        }
        return "NO";

    }

    /*
     * Complete the 'superDigit' function below.
     *
     * The function is expected to return an INTEGER.
     * The function accepts following parameters:
     *  1. STRING n
     *  2. INTEGER k
     */

    public static int superDigit(String n, int k)
    {
        // Super Digit = Digital Root in Math
        // Digital Root Function:
        // dr(n) = 1 + ((n-1) mod 9)
        // Where n is all digits in the number. In this case, it is k*n
        int nTotal = sumOfChars(n);

        return 1+(k*nTotal-1)%9;

    }

    public static int sumOfChars(String n)
    {
        int sum=0;
        for(int i=0;i<n.length();i++)
        {
            sum+=Character.getNumericValue(n.charAt(i));
        }
        return sum;
    }

    // Previous solution would fail for total sum larger than word size

    public static int superDigitBigInteger(String n, int k)
    {
        // Super Digit = Digital Root in Math
        // Digital Root Function:
        // dr(n) = 1 + ((n-1) mod 9)
        // Where n is all digits in the number. In this case, it is k*n
        //int nTotal = sumOfChars(n);

        BigInteger n1 = new BigInteger(n);
        n1 = n1.multiply(new BigInteger(k + "")); // k+"" gives a String instead of the int value of k
        n1 = n1.remainder(new BigInteger("9"));
        return n1.intValue() == 0 ? 9 : n1.intValue();

        //return 1+(k*nTotal-1)%9;

    }

    public String counterGame(long n)
    {
        // Write your code here
        int counter = counterGameHelper(n);

        if(counter%2==0) return "Richard";
        else return "Louise";

    }

    // L goes first  ; wins on mod 2 != 0
    // R goes second ; wins on mod 2 == 0
    // This method should return number of times n is reduced
    // e.g. if n = 6, we reduce it twice to get to n = 1

    public int counterGameHelper(long n)
    {
        if(n==1) return 0;
        return 1+counterGameHelper(n-closestPowerOfTwo(n));
    }

    // Helper to return closest power of 2 in accordance to n

    public static long closestPowerOfTwo(long n)
    {
        long power=1L;
        while(power<n)
        {
            power*=2;
        }
        return power/2;
    }
}
