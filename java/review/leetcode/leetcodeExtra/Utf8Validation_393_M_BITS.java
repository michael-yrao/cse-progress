package review.leetcode.leetcodeExtra;

public class Utf8Validation_393_M_BITS
{
    /*
    * https://leetcode.com/problems/utf-8-validation/
    * */


    /*
     * UTF-8 can be between 1 byte to 4 bytes
     * And we are given the restriction that data[i] is between 0-255 so that each index will occupy 1 byte only
     * So what we need to do is determine how many UTF-8 Characters are here and validate whether they follow
     * the correct format
     *
     *    Char. number range  |        UTF-8 octet sequence
     *       (hexadecimal)    |              (binary)
     *    --------------------+---------------------------------------------
     *    0000 0000-0000 007F | 0xxxxxxx
     *    0000 0080-0000 07FF | 110xxxxx 10xxxxxx
     *    0000 0800-0000 FFFF | 1110xxxx 10xxxxxx 10xxxxxx
     *    0001 0000-0010 FFFF | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
     *
     * We need to know what each of these mandatory values are so we can mask them and find out how many bytes we are dealing with
     *
     * */


    /*
    * Algorithm:
    *   1. Loop through the int array
    *   2. Check the index to see how many bytes we are dealing with and save this number into a variable
    *   3. Check to make sure every value in these bytes match what is expected
    *   4. Increment our loop accordingly to the next byte if passes
    * */

    public boolean validUtf8(int[] data)
    {
        if(data==null || data.length==0) return false;
        for(int i=0;i<data.length;i++)
        {
            if(data[i] > 255) return false;

            int numBytes = 0;

            // Mask against the bits so they can determine whether or not they start with those values
            // Always mask each mandatory bit with 1
            if((data[i] & 0b10000000) == 0b00000000) numBytes=1;
            else if((data[i] & 0b11100000) == 0b11000000) numBytes=2;
            else if((data[i] & 0b11110000) == 0b11100000) numBytes=3;
            else if((data[i] & 0b11111000) == 0b11110000) numBytes=4;
            else return false;

            // Now that we have the number of bytes, let's check to see if the next few characters match the sequence
            // We always jump out immediately if it's 1 byte, so we can ignore it
            for(int j=1;j<numBytes;j++)
            {
                // if we go out of bounds, return false
                if(i+j>= data.length) return false;
                // For 2,3,4 byte characters, all the rest of the bytes start with 0b10
                // Thus, check if this value starts with 10xxxxxx
                if((data[i+j] & 0b11000000) != 0b10000000) return false;
            }
            // Increment to the next UTF-8 character
            i=i+numBytes-1;
        }
        return true;
    }
}
