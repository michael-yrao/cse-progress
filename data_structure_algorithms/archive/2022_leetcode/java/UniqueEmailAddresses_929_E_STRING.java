package review.leetcode.leetcodeExtra;

import java.util.HashSet;
import java.util.Set;

public class UniqueEmailAddresses_929_E_STRING
{
    /*
    * https://leetcode.com/problems/unique-email-addresses/
    * */

    public int numUniqueEmails(String[] emails)
    {
        Set<String> set = new HashSet<>();
        for(String x : emails)
        {
            set.add(trueEmail(x));
        }
        return set.size();
    }

    private String trueEmail(String email)
    {
        // True local name
        String local = email.split("@")[0];
        // Get first occurence of +
        int index = local.indexOf('+');
        if(index == -1) local = local.replace(".","");
        else local = local.substring(0,index).replace(".","");

        // True domain name
        String domain = email.split("@")[1];
        String domainName = domain.substring(0,domain.length()-4);

        return local+"@"+domainName+".com";
    }
}
