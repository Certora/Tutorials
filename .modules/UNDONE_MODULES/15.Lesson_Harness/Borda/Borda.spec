methods{
    getVoterHasRegistered(address) returns bool envfree
    getVoterHasVoted(address) returns bool envfree
    getVoterIsBlackListed(address) returns bool envfree
    getVoterVoteAttempts(address) returns uint256 envfree
    getContenderPoints(address) returns uint256 envfree
    getContenderHasRegistered(address) returns bool envfree
    vote(address, address, address) returns(bool)
}

////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////   Ghosts   /////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//

// Ghost that tracks sum of all points distributed
ghost points_Sum_Ghost() returns uint256{
    init_state axiom points_Sum_Ghost() == 0;
}

// Updates the total points counter
hook Sstore _contenders [KEY address contender].points uint256 current_points(uint256 old_points) STORAGE {
	havoc points_Sum_Ghost assuming current_points > 0 ? 
                                    points_Sum_Ghost@new() == points_Sum_Ghost@old() - old_points + current_points :
                                    points_Sum_Ghost@new() == points_Sum_Ghost@old();
} 

// Ghost that count the number of voters that has voted so far
ghost VotersVotedCounter() returns uint256{
    init_state axiom VotersVotedCounter() == 0;
}

// Updates the number of voters that exercised their right
hook Sstore _voters [KEY address voter].voted bool current_value(bool old_value) STORAGE {
	havoc VotersVotedCounter assuming (!old_value && current_value) ? 
                                    VotersVotedCounter@new() == VotersVotedCounter@old() + 1 : 
                                    VotersVotedCounter@new() == VotersVotedCounter@old();
}

// Ghost that count the number of voters that has voted so far
ghost VotersRegistrationCounter() returns uint256{
    init_state axiom VotersRegistrationCounter() == 0;
}

// Updates the number of voters that exercised their right
hook Sstore _voters [KEY address voter].registered bool current_value(bool old_value) STORAGE {
	havoc VotersRegistrationCounter assuming (!old_value && current_value) ? 
                                    VotersRegistrationCounter@new() == VotersRegistrationCounter@old() + 1 : 
                                    VotersRegistrationCounter@new() == VotersRegistrationCounter@old();
}

////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////   Properties   ///////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//


// The total number of points is non-decreasing with any action taken by the system
rule monotonicityOfPoints(){
    env e; calldataarg args; method f;

    uint256 tot_pts_before = points_Sum_Ghost();
    f(e, args);
    uint256 tot_pts_after = points_Sum_Ghost();
    
    assert tot_pts_after >= tot_pts_before, "Total count of points has decreased";
}

// The number of points of a single contender is non-decreasing with any action taken by the system
rule monotonicityOfPoints2(address contender){
    env e; calldataarg args; method f;
    requireInvariant pointsOfContenderNotZeroIfRegistered(contender);
    uint256 tot_pts_before = getContenderPoints(contender);
    f(e, args);
    uint256 tot_pts_after = getContenderPoints(contender);
    
    assert tot_pts_after >= tot_pts_before, "Total count of points has decreased";
}

// The total number of voters is non-decreasing with any action taken by the system
rule monotonicityOfVoter(){
    env e; calldataarg args; method f;

    uint256 voters_count_before = VotersVotedCounter();
    f(e, args);
    uint256 voters_count_after = VotersVotedCounter();
    
    assert voters_count_after >= voters_count_before, "Total count of voters has decreased";
}

// Casting a vote distributes exactly 6 points
rule sixPointsAddedInEachVoting(address first, address second, address third){
    env e;

    uint256 tot_pts_before = points_Sum_Ghost();
    vote(e, first, second, third);
    uint256 tot_pts_after = points_Sum_Ghost();
    
    assert tot_pts_after == tot_pts_before + 6, "Total points did not increase in exactly 6 points";
}

// Total number of registered voters cannot be smaller than total number of voters that has already voted
// Not violated. can it be proved?
// invariant registeredVotersGreaterOrEqualVotedVoters()
//     VotersRegistrationCounter() >= VotersVotedCounter()

// A single contender's point count is greater than the total point count
invariant singleContenderPointsLessOrEqualTotalPoints(address contender)
    getContenderPoints(contender) <= points_Sum_Ghost()

// Total points divided by 6 is exactly the number of voters that cased their vote 
invariant totalPointsDividedBy6IsNumberOfVoters()
    points_Sum_Ghost() / 6 == VotersVotedCounter()

// Contender's points are non-zero only if they are registered - needed for monotonicityOfPoints2
invariant pointsOfContenderNotZeroIfRegistered(address contender)
    getContenderPoints(contender) > 0 => getContenderHasRegistered(contender)

// Any voter that had cast his vote already is marked as registered
invariant voterIsRegisteredWhenVoted(address voter)
    getVoterHasVoted(voter) => getVoterHasRegistered(voter)

// Number of voting attempts is initialized (non-zero) together with hasVoted - needed for blackListedVoterVotedAtLeastThreeTimes
invariant voterHasVotedIffAttemptsNonZero(address voter)
    getVoterVoteAttempts(voter) == 0 <=> !getVoterHasVoted(voter)


// Blacklisted voter has voted at least 3 times
invariant blackListedVoterVotedAtLeastThreeTimes(address voter)
    getVoterIsBlackListed(voter) <=> getVoterVoteAttempts(voter) >= 3
    {
        preserved
        {
            requireInvariant voterHasVotedIffAttemptsNonZero(voter);
        }
    }