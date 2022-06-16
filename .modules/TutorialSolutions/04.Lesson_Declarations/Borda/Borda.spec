

methods{
    getPointsOfContender(address) returns(uint256) envfree;
    hasVoted(address) returns(bool) envfree;
    getWinner() returns (address, uint256) envfree;
    getFullVoterDetails(address) returns(uint8, bool, bool, uint256, bool) envfree;
    getFullContenderDetails(address) returns(uint8, bool, uint256) envfree;

    registerVoter(uint8 ) returns (bool);
    registerContender(uint8 ) returns (bool);
    vote(address, address, address) returns(bool);
}

// returns the age of a voter
function getVoterAge(address voter) returns uint8{
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool black_listed;
    age, voterReg, voted, vote_attempts, black_listed = getFullVoterDetails(voter);
    return age;
}

// returns whether the voter is registered
function getVoterHasRegistered(address voter) returns bool{
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool black_listed;
    age, voterReg, voted, vote_attempts, black_listed = getFullVoterDetails(voter);
    return voterReg;
}

// returns whether the voter has voted
function getVoterHasVoted(address voter) returns bool{
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool black_listed;
    age, voterReg, voted, vote_attempts, black_listed = getFullVoterDetails(voter);
    return voted;
}

// returns the number of times a voter attempted to vote
function getVoterVoteAttempts(address voter) returns uint256{
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool black_listed;
    age, voterReg, voted, vote_attempts, black_listed = getFullVoterDetails(voter);
    return vote_attempts;
}

// returns whether the voter is black listed
function getVoterIsBlackListed(address voter) returns bool{
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool black_listed;
    age, voterReg, voted, vote_attempts, black_listed = getFullVoterDetails(voter);
    return black_listed;
}

// If a voter isn't registered every detail should return default value
definition unRegisteredVאoter(address voter) returns bool = 
        getVoterAge(voter) == 0 && !getVoterHasRegistered(voter) &&
        !getVoterHasVoted(voter) && getVoterVoteAttempts(voter) == 0 && 
        !getVoterIsBlackListed(voter);

// A registered voter that hasn't voted cannot be black listed, nor have any voting attempts.
// Note that the age is undetermained because we never demanded anything on the age in the implementation
definition registeredYetVotedVoter(address voter) returns bool = 
        getVoterHasRegistered(voter) && !getVoterHasVoted(voter) && 
        getVoterVoteAttempts(voter) == 0 && !getVoterIsBlackListed(voter);

// A registered voter that has already voted, but yet to be black listed
definition legitRegisteredVotedVoter(address voter) returns bool = 
        getVoterHasRegistered(voter) && getVoterHasVoted(voter) && 
        (getVoterVoteAttempts(voter) >= 1 && getVoterVoteAttempts(voter) <= 2) && 
        !getVoterIsBlackListed(voter);

// A registered voter that has already voted, and is black listed
definition BlackListedVoter(address voter) returns bool = 
        getVoterHasRegistered(voter) && getVoterHasVoted(voter) &&
        getVoterVoteAttempts(voter) >= 3 && getVoterIsBlackListed(voter);

// Checks that a voter's "registered" mark is changed correctly - 
// if it's false after a function call, it was false before
// if it's true after a function call it either started as true or changed from false to true via registerVoter()
rule registeredCannotChangeOnceSet(method f, address voter){
    env e; calldataarg args;
    uint256 age; bool voterRegBefore; bool voted; uint256 vote_attempts; bool black_listed;
    age, voterRegBefore, voted, vote_attempts, black_listed = getFullVoterDetails(voter);
    f(e, args);
    bool voterRegAfter;
    age, voterRegAfter, voted, vote_attempts, black_listed = getFullVoterDetails(voter);

    assert (!voterRegAfter => !voterRegBefore, "voter changed state from registered to not registered after a function call");
    assert (voterRegAfter => 
        ((!voterRegBefore && f.selector == registerVoter(uint8).selector) || voterRegBefore), 
            "voter was registered from an unregistered state, by other function then registerVoter()");
}

// Checks that a each voted contender's points receieved the correct amount of points
rule correctPointsIncreaseToContenders(address first, address second, address third){
    env e;
    uint256 firstPointsBefore = getPointsOfContender(first);
    uint256 secondPointsBefore = getPointsOfContender(second);
    uint256 thirdPointsBefore = getPointsOfContender(third);

    vote(e, first, second, third);
    uint256 firstPointsAfter = getPointsOfContender(first);
    uint256 secondPointsAfter = getPointsOfContender(second);
    uint256 thirdPointsAfter = getPointsOfContender(third);
    
    assert (firstPointsAfter - firstPointsBefore == 3, "first choice receieved other amount than 3 points");
    assert (secondPointsAfter - secondPointsBefore == 2, "second choice receieved other amount than 2 points");
    assert ( thirdPointsAfter- thirdPointsBefore == 1, "third choice receieved other amount than 1 points");

}

// Checks that a black listed voter cannaot get unlisted
rule onceBlackListedNotOut(method f, address voter){
    env e; calldataarg args;
    uint8 age; bool registeredBefore; bool voted; uint256 vote_attempts; bool black_listed_Before;
    age, registeredBefore, voted, vote_attempts, black_listed_Before = getFullVoterDetails(voter);
    require black_listed_Before => registeredBefore;
    f(e, args);
    bool registeredAfter; bool black_listed_After;
    age, registeredAfter, voted, vote_attempts, black_listed_After = getFullVoterDetails(voter);
    
    assert black_listed_Before => black_listed_After, "the specified user got out of the black list";
}

// Checks that a contender's point count is non-decreasing
rule contendersPointsNondecreasing(method f, address contender){
    env e; calldataarg args;
    uint8 age; bool registeredBefore; uint256 pointsBefore;
    age, registeredBefore, pointsBefore = getFullContenderDetails(contender);
    require pointsBefore > 0 => registeredBefore; 
    f(e,args);
    bool registeredAfter; uint256 pointsAfter;
    age, registeredAfter, pointsAfter = getFullContenderDetails(contender);

    assert (pointsAfter >= pointsBefore);
}

