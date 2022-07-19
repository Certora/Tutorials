pragma solidity ^0.7.0;
library SafeMath {
	function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

	function safeSub(uint256 x, uint256 y) internal pure returns(uint256) {
		assert(x >= y);
		uint256 z = x - y;
		return z;
    }
}

import "./IBorda.sol";

contract Borda is IBorda {

    using SafeMath for uint256;
  
    // a list of voters with some data on them.
    mapping (address => Voters) _voters;
    // voters black list - true if a voter is blacklisted
    address[] _blackList;
    // a list of contenders and some data on them.
    mapping (address => Contenders) _contenders;
    // current winner
    address winner;
    // current max points 
    uint256 pointsOfWinner; 

    constructor() public {
        winner = address(0);
        pointsOfWinner = 0;
    }

    function getPointsOfContender(address contender) public view override returns(uint256) {
        uint256 contender_points = _contenders[contender].points;
        return contender_points;
    }

    function hasVoted(address voter) public view override returns(bool) {
        bool voter_voted = _voters[voter].voted;
        return voter_voted;
    }

    function getWinner() public view override returns(address, uint256) {
        return (winner, pointsOfWinner);
    }

    function getFullVoterDetails(address voter) external view override returns(uint8 age, bool registered, bool voted, uint256 vote_attempts, bool black_listed) {
        Voters memory voter_details = _voters[voter];
        return (voter_details.age, voter_details.registered, voter_details.voted, voter_details.vote_attempts, voter_details.black_listed);
    }

    function getFullContenderDetails(address contender) external view override returns(uint8 age, bool registered, uint256 points) {
        Contenders memory contender_details = _contenders[contender];
        return (contender_details.age, contender_details.registered, contender_details.points);
    }

    function registerVoter(uint8 age) external override returns (bool) {
        require (!_voters[msg.sender].registered, "you are already registered");
        _voters[msg.sender] = Voters({age: age, registered: true, voted: false, vote_attempts: 0, black_listed: false});
        return true;
    }

    function registerContender(uint8 age) external override returns (bool) {
        require (!_contenders[msg.sender].registered, "you are already registered");
        _contenders[msg.sender] = Contenders({age: age, registered: true, points: 0});
        return true;
    }

    function vote(address first, address second, address third) public override returns(bool) {
        require (_voters[msg.sender].registered, "you are not registered. before you vote you have to register yourself");
        require (_contenders[first].registered && _contenders[second].registered && _contenders[third].registered, "one or more of the specified addresses aren't registered as contenders");
        require ( first != second && first != third && second != third, "you've tried to vote for the same more than once");
        
        Voters memory voter_details = _voters[msg.sender];
        _voters[msg.sender].vote_attempts = voter_details.vote_attempts.safeAdd(1);
        if (voter_details.voted){
           require(voter_details.vote_attempts >= 3, "you've already voted. If you reach 3 attempts you will be black listed");
           if (!voter_details.black_listed){
                _blackList.push(msg.sender); 
                _voters[msg.sender].black_listed = true;
           }
           assert(false);
        }

        _voters[msg.sender].voted = true;
        voteTo(first, 3);
        voteTo(second, 2);
        voteTo(third, 1);
        
        return true;
    }

    function voteTo(address contender, uint256 points) private {
        uint256 contender_points = _contenders[contender].points.safeAdd(points);
        _contenders[contender].points = contender_points;
        if (contender_points > pointsOfWinner) {
            winner = contender;
            pointsOfWinner = contender_points;
        }
    }

}
