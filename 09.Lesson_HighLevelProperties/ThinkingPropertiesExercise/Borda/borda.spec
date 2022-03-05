definition Unregistered(address voter) 
    returns bool = !getVoterReg(voter) && !getVoterVoted(voter) && getVoterAttempts(voter) == 0 
    && !getVoterBlocked(voter) && getVoterAge(voter) == 0;

definition VoterNotVoted(address voter) 
    returns bool = getVoterReg(voter) && !getVoterVoted(voter) && getVoterAttempts(voter) == 0 
    && !getVoterBlocked(voter) && getVoterAge(voter) >= 18; // assuming this, not implemented

definition VoterVoted(address voter) 
    returns bool = getVoterReg(voter) && getVoterVoted(voter) && getVoterAttempts(voter) < 3 
    && getVoterAttempts(voter) > 0 && !getVoterBlocked(voter) && getVoterAge(voter) >= 18;

definition Blacklisted(address voter)
    returns bool = getVoterReg(voter) && getVoterVoted(voter) && getVoterAttempts(voter) >= 3 && getVoterBlocked(voter) && getVoterAge(voter) >= 18; 

definition Contender(address contender)
    returns bool = getContenderReg(contender) && Unregistered(contender);

definition ContenderVoterNotVoted(address contender)
    returns bool = getContenderReg(contender) && VoterNotVoted(contender);

definition ContenderVoterVoted(address contender)
    returns bool = getContenderReg(contender) && VoterVoted(contender);

definition Winner(address contender)
    returns bool = getContenderReg(contender) && getWinner() == contender;

function getContenderAge(address contender) returns bool {
    uint8 age; bool registered; uint256 points;
    age, registered, points = getFullContenderDetails(contender);
    return age;
}

function getContenderReg(address contender) returns bool {
    uint8 age; bool registered; uint256 points;
    age, registered, points = getFullContenderDetails(contender);
    return registered;
}

function getContenderPts(address contender) returns bool {
    uint8 age; bool registered; uint256 points;
    age, registered, points = getFullContenderDetails(contender);
    return points;
}

function getVoterAge(address voter) returns uint256 {
    uint8 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return age;
}

function getVoterReg(address voter) returns bool {
    uint8 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return registered;
}

function getVoterVoted(address voter) returns bool {
    uint8 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voted;
}

function getVoterAttempts(address voter) returns uint256 {
    uint8 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return vote_attempts;
}

function getVoterBlocked(address voter) returns bool {
    uint8 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return blocked;
}

rule unregisteredTo(address user, method f) {
    env e;
    calldataarg args;
    require Unregistered(user);
    f(e, args);
    assert Unregistered(user) || VoterNotVoted(user) || Contender(user), "improper transition";
}

rule voterNotVotedTo(address user, method f) {
    env e;
    calldataarg args;
    require VoterNotVoted(user);
    f(e, args);
    assert VoterNotVoted(user) || VoterVoted(user) || ContenderVoterNotVoted(user), "improper transition";
}

rule voterVotedTo(address user, method f) {
    env e;
    calldataarg args;
    require VoterVoted(user);
    f(e, args);
    assert VoterVoted(user) || ContenderVoterVoted(user) || Blacklisted(user), "improper transition";
}

rule blacklistedTo(address user, method f) {
    env e;
    calldataarg args;
    require Blacklisted(user);
    f(e, args);
    assert Blacklisted(user);
}

rule contenderTo(address user, method f) {
    env e;
    calldataarg args;
    require Contender(user);
    f(e, args);
    assert Contender(user) || ContenderVoterNotVoted(user) || Winner(user), "improper transition";
}