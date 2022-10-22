# This doesn't render in .md yet; just a readme file

Welcome To Exercise 13!

Here, we'll try to write as few strong properties as possible - to get as much coverage as possible.
Then we'll have a small competetion with mutations :)

So we're going to work with a very very simple contract that implements an "English Auction".
(It's based on this code from SolidityByExample:
https://solidity-by-example.org/app/english-auction/ )

Go over the code provided in this folder (EnglishAuction.sol), and try to think of up to two rules/invariants that would get the best coverage*.

Then, Think of some mutation that would be hard to catch, and implement it into the GroupMutations folder under your group name (for example, "Mutation_GroupA.sol". Please note to commit only that file and not update the root of the exercise folder).
Note that the mutation:
* Should keep the same interface for the protocol (so the same spec for the normal code would work against this one, and so other groups' specs would work).
* Should be at least High (not a must, will affect scoring)

After this phase, we will test each group's specs against all the other groups mutation.
Each time your spec caught one of the other group's mutations, you'll get points.
You'll get extra points if other groups missed that mutation.

(Scoring - 4 points if only you found, 3 points for two groups, 2 for 3, 1 for 4, and 0 for 5.
    If the mutation is less than high severity, half the score rounding down)



After that period ends, we'll return to the groups to tweak their rules.
After that tweak, we'll run agian against a bunch of prepared mutations and see which of them are caught.
We'll have a similar scoring (but with less points rewarded since there are a lot).

We will conclude with some discussion about the findings, thoughts, methods, and other things that you've found together during this exercise. (For example, which kind of bugs were found by which kind of rules, which rules felt strong but actually weren't, and which rules were surprisingly strong, etc).

