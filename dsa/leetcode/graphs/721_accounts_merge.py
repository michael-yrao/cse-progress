"""
721. Accounts Merge   ·   https://leetcode.com/problems/accounts-merge/
Pattern: graphs

Given a list `accounts`, where `accounts[i]` is a list of strings:
`accounts[i][0]` is a name, and the rest of the elements are emails
belonging to that account.

Two accounts definitely belong to the same person if there is some email
common to both accounts. Note that even if two accounts have the same name,
they may belong to different people, since people could have the same name.
A person can have any number of accounts initially, but all of their accounts
definitely have the same name.

After merging the accounts, return the accounts in the following format:
the first element of each account is the name, and the rest of the elements
are emails **in sorted order**. The accounts themselves can be returned in
any order.

Example 1:

Input: accounts =
    [["John","johnsmith@mail.com","john_newyork@mail.com"],
     ["John","johnsmith@mail.com","john00@mail.com"],
     ["Mary","mary@mail.com"],
     ["John","johnnybravo@mail.com"]]
Output:
    [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
     ["Mary","mary@mail.com"],
     ["John","johnnybravo@mail.com"]]
Explanation:
    The first and second John's are the same person as they have the common
    email "johnsmith@mail.com". The third John and Mary are different people
    as none of their email addresses are used by other accounts.
    We could return these lists in any order.

Example 2:

Input: accounts =
    [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],
     ["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],
     ["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],
     ["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],
     ["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
Output:
    [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],
     ["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],
     ["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],
     ["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],
     ["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]

Constraints:

    1 <= accounts.length <= 1000
    2 <= accounts[i].length <= 10
    1 <= accounts[i][j].length <= 30
    accounts[i][0] consists of English letters.
    accounts[i][j] (for j > 0) is a valid email.
"""
# Write everything yourself from here — including any ListNode/TreeNode classes a
# problem needs. No shared data-model imports (whiteboard fidelity).
import collections
from typing import List, Optional


class Solution:

    # ── Attempt · 2026-08-09 ──────────────
    def accountsMerge_20260809(self, accounts: List[List[str]]) -> List[List[str]]:
        # this is an union find problem. we are saying names with one or more shared email is one component
        # so each email is a node, but we also need to know who the email belongs
        # which brings us to the question of union and find, if we are able to union two emails
        # we can consider everything under that account to be part of the same component
        # so find should return us the account, not the emails
        # since names can be the same, we can't use name as a key, we should use index
        # this would be the same for the union, we use the emails to find the components to join on, which will be based on the accounts and not the emails so we are using emails to find the accounts to union
        # so it seems like we need an email to account index map
        # this makes it easy for us to union
        # think we are good to begin with these details

        # email to indices list
        emailToAccountMap = collections.defaultdict(list)

        for i in range(len(accounts)):
            account = accounts[i][0]
            numOfEmails = len(accounts[i])
            for j in range(1,numOfEmails):
                email = accounts[i][j]
                emailToAccountMap[email].append(i)
        
        # now that we have the map constructed, let's do our union find
        rankMap = {}
        parentMap = {}

        # start each account as its own component
        # start each account with rank of 0
        for i in range(len(accounts)):
            rankMap[i] = 0
            parentMap[i] = i
        
        # path compression / union by rank
        def find(node):
            if parentMap[node] != node:
                parentMap[node] = find(parentMap[node])
            return parentMap[node]
        
        def union(n1,n2):
            n1p = find(n1)
            n2p = find(n2)
            # same parent, thus we form a cycle
            if n1p == n2p:
                return False
            if rankMap[n1p] > rankMap[n2p]:
                parentMap[n2p] = n1p
            elif rankMap[n1p] < rankMap[n2p]:
                parentMap[n1p] = n2p
            else:
                parentMap[n2p] = n1p
                rankMap[n1p]+=1
            return True
        
        # now let's go through the map we created and let's union the ones that have more than one value in the list
        for email in emailToAccountMap:
            # we will loop from 1 onwards to auto skip emails with only one parent
            for i in range(1,len(emailToAccountMap[email])):
                account1 = emailToAccountMap[email][i-1]
                account2 = emailToAccountMap[email][i]
                # if we haven't unioned them yet, let's union them
                union(account1,account2)
        
        # parentAccount -> list of emails
        resultMap = collections.defaultdict(set)
        # now that all the accounts that need to be unioned are unioned, we generate the list of results to a map first
        for i in range(len(accounts)):
            parentAccount = find(i)
            for j in range(1,len(accounts[i])):
                email = accounts[i][j]
                resultMap[parentAccount].add(email)

        result = []
        # now let's create the result from resultMap
        for accountIndex, emails in resultMap.items():
            resultArray = []
            # create account, email1, email2 result array
            account = accounts[accountIndex][0]
            resultArray.append(account)
            sortedEmails = list(emails)
            sortedEmails.sort()
            resultArray.extend(sortedEmails)
            # add resultArray to result
            result.append(resultArray)
        
        return result

    # ── Attempt 1 · 2026-07-30 ────────────────────────────────────────────
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        # ok, we are looking for components here
        # so if accounts[i][2] == accounts[j][3], that means i and j are connected components
        # since they can have same names, we can track the components via indices
        # nodes are indices' other values that are not 0 and we need a way to track that
        # so first question is what do we rank/union, that should be the indices
        # main difference here is how we do the find and union algorithms
        
        rankMap = {}
        parentMap = {}

        for i in range(len(accounts)):
            rankMap[i] = 0
            parentMap[i] = i
        
        def find(node):
            # if we are the root parent, no need to continue
            if parentMap[node] == node:
                return parentMap[node]
            # otherwise, find the root parent
            parentMap[node] = find(parentMap[node])
            return parentMap[node]
        
        def union(n1,n2):
            n1p = find(n1)
            n2p = find(n2)
            # have the same parent
            if n1p == n2p:
                return False
            if rankMap[n1p] > rankMap[n2p]:
                parentMap[n2p] = n1p
            elif rankMap[n1p] < rankMap[n2p]:
                parentMap[n1p] = n2p
            else:
                rankMap[n1p]+=1
                parentMap[n2p] = n1p
            return True
        
        # so we got the basic union find written, let's figure out the logic for performing union
        # what if we do map of node to indices then we walk through all keys and just do union of indices in each
        
        nodeMap = collections.defaultdict(list)
        
        for i in range(len(accounts)):
            for j in range(1,len(accounts[i])):
                node = accounts[i][j]
                nodeMap[node].append(i)

        # with nodeMap, we can now tell what goes where
        # go through all values of nodeMap

        for node, accts in nodeMap.items():
            for i in range(1,len(accts)):
                acct1 = accts[i-1]
                acct2 = accts[i]
                union(acct1,acct2)

        # so now our parentMap is set and we know who is connected to whom via find
        # so let's build the root parent -> nodes mapping
        # we need a set to remove duplicates within an union
        parentEmailMap = collections.defaultdict(set)
        for i in range(len(accounts)):
            parent = find(i)
            for j in range(1, len(accounts[i])):
                parentEmailMap[parent].add(accounts[i][j])

        # now we convert parentEmailMap to a list each and add to result
        result = []
        for parent, emails in parentEmailMap.items():
            emailList = list(emails)
            emailList.sort()
            resultArray = []
            resultArray.append(accounts[parent][0])
            resultArray+=emailList
            result.append(resultArray)

        return result
