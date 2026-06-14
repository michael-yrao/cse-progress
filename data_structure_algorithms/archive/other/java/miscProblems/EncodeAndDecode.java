package review.miscProblems;

import java.util.ArrayList;
import java.util.List;

public class EncodeAndDecode
{
    /*
    * https://www.lintcode.com/problem/659/
    * */

    public String encode(String[] strs)
    {
        StringBuilder sb = new StringBuilder();

        for(String x : strs)
        {
            sb.append(x.length() + "#" + x);
        }

        return sb.toString();

    }

    public List<String> decode(String str)
    {
        // 4#neet5#co#de

        List<String> returnList = new ArrayList<>();
        StringBuffer sb = new StringBuffer();

        for(int i=0;i<str.length();i++)
        {
            int trueNumber = str.charAt(i)-'0';
            if(trueNumber >= 0 && trueNumber <= 9)
            {
                sb.append(str.charAt(i));
            }
            if(str.charAt(i)=='#')
            {
                // Add word to list
                // Skip to next word
                returnList.add(str.substring(i+1,i+1+Integer.parseInt(sb.toString())));
                i+=Integer.parseInt(sb.toString());
                sb.delete(0,sb.length());
            }
        }
        return returnList;
    }

}
