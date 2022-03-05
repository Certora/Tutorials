# Properties

***Valid states***

1. Unregistered
2. VoterNotVoted
3. VoterVoted
4. Blacklisted
5. Contender
6. ContenderVoterNotVoted
7. ContenderVoterVoted
8. Winner

***State transitions***

9. all states can transition      to themselves
10. Unregistered                       to VoterNotVoted or Contender
11. VoterNotVoted                    to VoterVoted or ContenderVoterNotVoted
12. VoterVoted                          to Blacklisted or ContenderVoterNotVoted
13. Blacklisted                           to
14. Contender                            to ContenderVoterNotVoted or Winner
15. ContenderVoterNotVoted   to ContenderVoterVoted or Winner
16. ContenderVoterVoted         to Blacklisted or Winner
17. Winner                                  to Contender or ContenderVoterNotVoted or ContenderVoterVoted

***Variable transitions***

18. pointsOfWinner is non-decreasing
19. pointsOfWinner increases only because of non-reverting vote() call
20. _blackList.length is non-decreasing
21. if _blackList.length increased then vote() was called
22. non-reverting vote() called => pointsOfWinner increases or blacklist.length increases
23. winner changed => vote() called
24. Contenders points is non-decreasing
25. Vote attempts do not decrease, never greater than 3.

***High-level properties***

26. points of winner <= total votes
27. 1 vote per person(address)
28. Vote immutable
29. blacklisted cant win/vote/be voted for/register/register as contender
31. points of winner >= points anyone else

***Unit tests***
for all statechanging functions

# Priority

## High

1-8, important part of all definitions, building blocks
12, 13, most likely to lead to cheating if broken
18, 19, 23, 25 things that dont have a second layer (proper state transition)
26-31, overall idea maintained

## Medium

the rest, have a similar rule so theyre medium

## Low

none
