pragma solidity ^0.7.0;

import "./BordaFixed.sol";

contract BordaHarness is Borda {

    function getFullVoterDetails(address voter) external view returns(uint8 age, bool registered, bool voted, uint256 vote_attempts, bool black_listed) {
        Voters memory voter_details = _voters[voter];
        return (voter_details.age, voter_details.registered, voter_details.voted, voter_details.vote_attempts, voter_details.black_listed);
    }

    function getFullContenderDetails(address contender) external view returns(uint8 age, bool registered, uint256 points) {
        Contenders memory contender_details = _contenders[contender];
        return (contender_details.age, contender_details.registered, contender_details.points);
    }

    // OR

    // returns the age of a voter
    function getVoterAge(address voter) public returns (uint8){
        return _voters[voter].age;
    }

    // returns whether the voter is registered
    function getVoterHasRegistered(address voter) public returns (bool){
        return _voters[voter].registered;
    }

    // returns whether the voter has voted
    function getVoterHasVoted(address voter) public returns (bool){
        return _voters[voter].voted;
    }

    // returns the number of times a voter attempted to vote
    function getVoterVoteAttempts(address voter) public returns (uint256){
        return _voters[voter].vote_attempts;
    }

    // returns whether the voter is black listed
    function getVoterIsBlackListed(address voter) public returns (bool){
        return _voters[voter].black_listed;
    }

    // returns the age of a voter
    function getContenderAge(address contender) public returns (uint8){
        return _contenders[contender].age;
    }

    // returns whether the voter is registered
    function getContenderHasRegistered(address contender) public returns (bool){
        return _contenders[contender].registered;
    }

    // returns whether the voter has voted
    function getContenderPoints(address contender) public returns (uint256){
        return _contenders[contender].points;
    }
}
